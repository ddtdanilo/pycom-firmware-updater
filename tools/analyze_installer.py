#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Static PyInstaller inspection; never import or execute recovered application code.

Input is the executable from an already expanded installer, not a .pkg file.
Python must match the archive version when decoding code objects.
"""

from __future__ import annotations

import argparse
import ast
import dis
import hashlib
import io
import json
import marshal
from pathlib import Path
import re
import struct
import subprocess
import sys
import types
import zlib

MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"
COOKIE = struct.Struct("!8sIIII64s")
ENTRY = struct.Struct("!IIIIBc")
MAX_INPUT = 128 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024
MAX_TOTAL_EXPANDED = 256 * 1024 * 1024
APPLICATION_ROOTS = {
    "classes", "errors_lib", "npy_programmer", "programmer", "pypic",
    "server", "settings", "tray", "updater", "utils",
}
SENSITIVE = re.compile(r"password|username|secret|token|api_?key", re.I)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def region(data: bytes, offset: int, size: int) -> bytes:
    if offset < 0 or size < 0 or offset + size > len(data):
        raise ValueError("Archive entry is outside its containing buffer")
    return data[offset:offset + size]


def inflate(data: bytes, expected: int | None = None) -> bytes:
    dec = zlib.decompressobj()
    out = dec.decompress(data, MAX_EXPANDED + 1)
    if len(out) > MAX_EXPANDED or not dec.eof or dec.unused_data:
        raise ValueError("Invalid or oversized compressed entry")
    if expected is not None and len(out) != expected:
        raise ValueError("Expanded entry size mismatch")
    return out


def parse_archive(data: bytes) -> tuple[int, list[dict], dict[str, bytes]]:
    if len(data) > MAX_INPUT:
        raise ValueError("Input exceeds inspection size limit")
    pos = data.rfind(MAGIC)
    if pos < 0:
        raise ValueError("PyInstaller cookie not found")
    _, length, offset, size, version, _ = COOKIE.unpack(region(data, pos, COOKIE.size))
    start = pos + COOKIE.size - length
    payload = region(data, start, length - COOKIE.size)
    toc = region(payload, offset, size)
    entries, extracted, cursor, total = [], {}, 0, 0
    while cursor < len(toc):
        n, p, length, expanded, compressed, kind = ENTRY.unpack(region(toc, cursor, ENTRY.size))
        if n <= ENTRY.size or expanded > MAX_EXPANDED or compressed not in (0, 1):
            raise ValueError("Invalid archive entry header")
        total += expanded
        if total > MAX_TOTAL_EXPANDED:
            raise ValueError("Archive exceeds total expansion budget")
        name = region(toc, cursor + ENTRY.size, n - ENTRY.size).rstrip(b"\0").decode("utf-8")
        cursor += n
        if not name or name.startswith(("/", "\\")) or ".." in name.replace("\\", "/").split("/"):
            raise ValueError("Unsafe archive entry name")
        if name in extracted:
            raise ValueError("Duplicate archive entry name")
        raw = region(payload, p, length)
        raw = inflate(raw, expanded) if compressed else raw
        if len(raw) != expanded:
            raise ValueError("Archive entry size mismatch")
        entries.append({"name": name, "type": kind.decode("ascii"),
                        "compressed_bytes": length, "bytes": expanded, "sha256": sha(raw)})
        extracted[name] = raw
    return version, entries, extracted


def parse_pyz(data: bytes, decrypt=None, table_loader=marshal.loads) -> tuple[list[dict], dict[str, bytes]]:
    if data[:4] != b"PYZ\0":
        raise ValueError("PYZ magic mismatch")
    offset, = struct.unpack("!i", region(data, 8, 4))
    if offset < 12:
        raise ValueError("Invalid PYZ table offset")
    # Expected input is a primitive table; marshal itself is not a hardened parser.
    table = table_loader(region(data, offset, len(data) - offset))
    if not isinstance(table, (list, dict)):
        raise ValueError("Invalid PYZ table")
    entries, extracted, total = [], {}, 0
    pairs = table.items() if isinstance(table, dict) else table
    for name, value in pairs:
        if isinstance(name, bytes):
            name = name.decode("utf-8")
        if not isinstance(name, str) or not re.fullmatch(r"[\w.]+", name) or name in extracted:
            raise ValueError("Invalid PYZ module name")
        if not isinstance(value, tuple) or len(value) != 3 or not all(type(n) is int for n in value):
            raise ValueError("Invalid PYZ module entry")
        kind, pos, size = value
        if kind not in (0, 1, 3):
            raise ValueError("Unsupported PYZ entry type")
        compressed = region(data, pos, size)
        if decrypt and kind != 3:
            compressed = decrypt(compressed)
        raw = b"" if kind == 3 else inflate(compressed)
        total += len(raw)
        if total > MAX_TOTAL_EXPANDED:
            raise ValueError("PYZ exceeds total expansion budget")
        entries.append({"name": name, "kind": kind, "compressed_bytes": size,
                        "bytes": len(raw), "sha256": sha(raw)})
        extracted[name] = raw
    return entries, extracted


def secret_literals(code: types.CodeType) -> set[str]:
    found = set()
    instructions = list(dis.get_instructions(code))
    for i, ins in enumerate(instructions):
        if ins.opname.startswith("STORE_") and SENSITIVE.search(str(ins.argval)) and i:
            previous = instructions[i - 1]
            if previous.opname == "LOAD_CONST" and isinstance(previous.argval, (str, bytes)) and previous.argval:
                found.add(previous.argval)
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            found.update(secret_literals(value))
    return found


def sanitized(code: types.CodeType, secrets: set[str], module: str) -> types.CodeType:
    def clean(value):
        if isinstance(value, types.CodeType):
            return sanitized(value, secrets, module)
        if isinstance(value, (str, bytes)):
            for secret in sorted(secrets, key=len, reverse=True):
                if value == secret:
                    value = b"[REDACTED]" if isinstance(value, bytes) else "[REDACTED]"
            text = value.decode("utf-8", "replace") if isinstance(value, bytes) else value
            if re.search(r"-----BEGIN [A-Z ]+-----", text) or re.search(r"[a-z]+://[^/\s]+:[^/\s]+@", text):
                return b"[REDACTED]" if isinstance(value, bytes) else "[REDACTED]"
        if isinstance(value, tuple):
            return tuple(clean(item) for item in value)
        return value
    return code.replace(co_filename=module.replace(".", "/") + ".py",
                        co_consts=tuple(clean(value) for value in code.co_consts))


def symbols(code: types.CodeType, name: str) -> list[dict]:
    result = [{"symbol": name, "line": code.co_firstlineno,
               "arguments": list(code.co_varnames[:code.co_argcount + code.co_kwonlyargcount]),
               "names": list(code.co_names), "bytecode_bytes": len(code.co_code)}]
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            result.extend(symbols(value, name + "." + value.co_name))
    return result


def inspect(executable: Path, output: Path, decompiler: Path | None = None) -> dict:
    if decompiler and decompiler.resolve() == executable.resolve():
        raise ValueError("The analyzed application cannot be used as a decompiler")
    if executable.stat().st_size > MAX_INPUT:
        raise ValueError("Input exceeds inspection size limit")
    data = executable.read_bytes()
    version, archive, extracted = parse_archive(data)
    if version != sys.version_info.major * 100 + sys.version_info.minor:
        raise ValueError(f"Use Python {version // 100}.{version % 100} for this archive")
    pyzs = [e["name"] for e in archive if e["type"] == "z"]
    if len(pyzs) != 1:
        raise ValueError("Expected exactly one PYZ archive")
    modules, raw_modules = parse_pyz(extracted[pyzs[0]])
    selected = {n: b for n, b in raw_modules.items() if n.split(".")[0] in APPLICATION_ROOTS and b}
    if "start" in extracted:
        selected["start"] = extracted["start"]
    codes = {n: marshal.loads(b) for n, b in selected.items()}
    if not all(isinstance(c, types.CodeType) for c in codes.values()):
        raise ValueError("Selected module is not a Python code object")
    secrets = set().union(*(secret_literals(c) for c in codes.values()))
    if len({name.casefold() for name in codes}) != len(codes):
        raise ValueError("Case-insensitive module output collision")
    # Caller chooses a new local directory and reviews any intended publication.
    output.mkdir(parents=True, exist_ok=False)
    recovery = output / "recovered"
    recovery.mkdir()
    results = []
    for name, code in sorted(codes.items()):
        code = sanitized(code, secrets, name)
        stream = io.StringIO()
        dis.dis(code, file=stream)
        assembly = re.sub(r" at 0x[0-9a-f]+,", " at <address omitted>,", stream.getvalue())
        (recovery / (name + ".dis.txt")).write_text(assembly, encoding="utf-8")
        result = {"module": name, "original_marshaled_sha256": sha(selected[name]),
                  "symbols": symbols(code, name)}
        if decompiler:
            intermediate = recovery / (name + ".marshal")
            intermediate.write_bytes(marshal.dumps(code))
            try:
                proc = subprocess.run([str(decompiler.resolve()), "-c", "-v",
                                       f"{version // 100}.{version % 100}", str(intermediate)],
                                      capture_output=True, text=True, errors="replace", timeout=30)
                source = proc.stdout
                try:
                    ast.parse(source)
                    syntax = bool(proc.stdout.strip())
                except (SyntaxError, ValueError):
                    syntax = False
                result.update(decompiler_exit=proc.returncode, syntax_valid=syntax,
                              diagnostic_lines=len(proc.stderr.splitlines()),
                              incomplete_marker="Decompyle incomplete" in source)
                # Syntactic validity is not semantic or completeness validation.
                (recovery / (name + ".py.txt")).write_text(source, encoding="utf-8")
                (recovery / (name + ".diagnostics.txt")).write_text(proc.stderr, encoding="utf-8")
            except subprocess.TimeoutExpired:
                result["decompiler_timeout"] = True
            finally:
                intermediate.unlink()
        results.append(result)
    manifest = {"schema_version": 1, "executable_sha256": sha(data), "executable_bytes": len(data),
                "python_version": version, "archive_entries": archive, "pyz_modules": modules,
                "redacted_literal_count": len(secrets), "application_analysis": results,
                "scope": "Static reference analysis; no recovered application code executed",
                "rights": "Pycom-derived reference artifacts: redistribution/license unresolved; not MIT"}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="New local directory; inspect before publishing")
    parser.add_argument("--decompiler", type=Path, help="Explicit local pycdc executable; never the analyzed app")
    args = parser.parse_args()
    try:
        result = inspect(args.executable, args.output, args.decompiler)
    except (ValueError, TypeError, RecursionError, OSError, EOFError, struct.error, zlib.error) as error:
        parser.exit(1, f"Inspection failed: {error}\n")
    print(f"Inspected {len(result['archive_entries'])} archive entries, "
          f"{len(result['pyz_modules'])} PYZ modules, "
          f"{len(result['application_analysis'])} candidate application modules.")
    print(f"Redacted {result['redacted_literal_count']} credential literals; review output before publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
