#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Decode the classic Python 2.7 GUI as data using isolated research dependencies."""

import argparse
import copy
import io
import json
from pathlib import Path
import re
import sys
from importlib.metadata import version as package_version

from analyze_installer import MAX_INPUT, parse_archive, parse_pyz, sha
from xdis import iscode
from xdis.bytecode import Bytecode
from xdis.magics import magic2int
from xdis.op_imports import get_opcode_module
from xdis.unmarshal import load_code
from uncompyle6.main import decompile
from Crypto.Cipher import AES

ROOTS = {"DeviceInfoQuery", "DeviceUpgrade", "FetchFiles", "LoadingSpin",
         "RunInWorker", "env_settings", "misc", "pyconf", "pypic", "updater"}
OPC = get_opcode_module((2, 7))
SENSITIVE = re.compile(r"password|username|secret|api_?key|auth_?token", re.I)


def sensitive_literals(code):
    found = set()
    instructions = list(Bytecode(code, OPC))
    for i, ins in enumerate(instructions):
        if ins.opname.startswith("STORE_") and SENSITIVE.search(str(ins.argval)) and i:
            prev = instructions[i - 1]
            if prev.opname == "LOAD_CONST" and isinstance(prev.argval, (str, bytes)) and prev.argval:
                found.add(prev.argval)
    for value in code.co_consts:
        if iscode(value):
            found.update(sensitive_literals(value))
    return found


def normalize(code, secrets, module):
    def clean(value):
        if iscode(value):
            return normalize(value, secrets, module)
        if isinstance(value, (str, bytes)):
            for secret in sorted(secrets, key=len, reverse=True):
                if type(secret) is type(value):
                    if value == secret:
                        value = b"[REDACTED]" if isinstance(value, bytes) else "[REDACTED]"
            text = value.decode("utf-8", "replace") if isinstance(value, bytes) else value
            if re.search(r"-----BEGIN [A-Z ]+-----", text) or re.search(r"[a-z]+://[^/\s]+:[^/\s]+@", text):
                return b"[REDACTED]" if isinstance(value, bytes) else "[REDACTED]"
        if isinstance(value, tuple):
            return tuple(clean(v) for v in value)
        return value
    result = copy.copy(code)
    result.co_filename = module + ".py"
    result.co_consts = tuple(clean(v) for v in code.co_consts)
    return result


def walk(code, symbol):
    yield symbol, code
    for value in code.co_consts:
        if iscode(value):
            yield from walk(value, symbol + "." + value.co_name)


def inspect(executable, output):
    if executable.stat().st_size > MAX_INPUT:
        raise ValueError("Input exceeds inspection size limit")
    data = executable.read_bytes()
    version, archive, extracted = parse_archive(data)
    if version != 27:
        raise ValueError("This research decoder expects Python 2.7")
    pyzs = [e["name"] for e in archive if e["type"] == "z"]
    if len(pyzs) != 1 or "pycom_fwtool" not in extracted:
        raise ValueError("Expected classic GUI entry and one PYZ archive")
    pyz = extracted[pyzs[0]]
    magic = magic2int(pyz[4:8])
    decrypt = None
    if "pyimod00_crypto_key" in extracted:
        key_blob = extracted["pyimod00_crypto_key"]
        if key_blob[:4] != pyz[4:8]:
            raise ValueError("Unexpected embedded archive-key header")
        key_code = load_code(key_blob[8:], magic, code_objects={})
        values = [v for v in key_code.co_consts if isinstance(v, (str, bytes))]
        if len(values) != 1 or tuple(key_code.co_names) != ("key",):
            raise ValueError("Unexpected embedded archive-key layout")
        key = values[0].encode("utf-8") if isinstance(values[0], str) else values[0]
        key = key[:16].zfill(16)
        # Historical PyInstaller CFB8 format: IV prefix followed by ciphertext.
        # Decode the key as data; do not import the embedded module or publish it.
        def decrypt(blob):
            if len(blob) < 16:
                raise ValueError("Truncated encrypted PYZ entry")
            return AES.new(key, AES.MODE_CFB, iv=blob[:16], segment_size=8).decrypt(blob[16:])
    modules, raw = parse_pyz(pyz, decrypt=decrypt,
                            table_loader=lambda blob: load_code(blob, magic, code_objects={}))
    selected = {n: b for n, b in raw.items() if n.split(".")[0] in ROOTS and b}
    selected["pycom_fwtool"] = extracted["pycom_fwtool"]
    codes = {n: load_code(b, magic, code_objects={}) for n, b in selected.items()}
    if not all(iscode(c) for c in codes.values()):
        raise ValueError("Selected entry is not a code object")
    if len({name.casefold() for name in codes}) != len(codes):
        raise ValueError("Case-insensitive module output collision")
    secrets = set().union(*(sensitive_literals(c) for c in codes.values()))
    output.mkdir(parents=True, exist_ok=False)
    recovered = output / "recovered"
    recovered.mkdir()
    results = []
    for name, code in sorted(codes.items()):
        code = normalize(code, secrets, name)
        assembly, records = [], []
        for symbol, nested in walk(code, name):
            assembly.append(f"Symbol: {symbol}\n" + Bytecode(nested, OPC).dis())
            records.append({"symbol": symbol, "line": nested.co_firstlineno,
                            "arguments": list(nested.co_varnames[:nested.co_argcount]),
                            "names": list(nested.co_names), "bytecode_bytes": len(nested.co_code)})
        disassembly = re.sub(r"0x[0-9a-f]+(?=, file)", "<address omitted>", "\n".join(assembly))
        (recovered / (name + ".dis.txt")).write_text(disassembly, encoding="utf-8")
        stream = io.StringIO()
        result = {"module": name, "original_marshaled_sha256": sha(selected[name]), "symbols": records}
        try:
            decompile(code, bytecode_version=(2, 7), out=stream, magic_int=magic, code_objects={})
            result["decompiler_completed"] = True
        except Exception as error:
            result["decompiler_completed"] = False
            # Do not publish exception contents, which may contain source literals.
            result["error_type"] = type(error).__name__
        # Portable-code decompilation can emit an invalid module-level bare return.
        lines = stream.getvalue().splitlines()
        removed = 0
        while lines and (not lines[-1] or lines[-1] == "return"):
            if lines.pop() == "return":
                removed += 1
        lines = ["# Decompiled from: research decoder (version recorded in manifest)"
                 if line.startswith("# Decompiled from:") else line for line in lines]
        source = "\n".join(lines) + "\n"
        (recovered / (name + ".py.txt")).write_text(source, encoding="utf-8")
        result["source_preview_bytes"] = len(source.encode())
        result["terminal_module_returns_omitted"] = removed
        results.append(result)
    manifest = {"schema_version": 1, "python_version": 27,
                "executable_sha256": sha(data),
                "executable_bytes": len(data),
                "archive_entries": archive, "pyz_modules": modules,
                "redacted_literal_count": len(secrets), "application_analysis": results,
                "archive_encryption": "Embedded PyInstaller CFB8 key decoded as data; key not exported",
                "normalizations": ["Module-level bare return emitted by decoder omitted",
                                   "Source paths normalized; secret/PEM/userinfo literals redacted if found",
                                   "Host build string in source-preview header normalized; literal whitespace preserved"],
                "decoder_versions": {"uncompyle6": package_version("uncompyle6"),
                                     "xdis": package_version("xdis"),
                                     "pycryptodome": package_version("pycryptodome"),
                                     "python": sys.version},
                "scope": "Static classic-GUI research; no recovered application code executed",
                "rights": "Pycom-derived reference artifacts: license/reuse unresolved; not MIT"}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = inspect(args.executable, args.output)
    except Exception as error:
        parser.exit(1, f"Static decoding failed ({type(error).__name__}); inspect local inputs privately.\n")
    print(f"Statically recovered {len(manifest['application_analysis'])} classic GUI/core candidates; "
          f"redacted {manifest['redacted_literal_count']} literal values.")
