#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify committed research provenance without loading recovered code."""

import hashlib
import json
from pathlib import Path
import re

RESEARCH = Path(__file__).resolve().parents[1] / "research"


def check_snapshot(ROOT):
    manifest = json.loads((ROOT / "manifest.json").read_text())
    expected = set()
    for entry in manifest["published_files"]:
        path = (ROOT / entry["path"]).resolve()
        if not path.is_relative_to((ROOT / "recovered").resolve()) or path.suffix != ".txt":
            raise ValueError("Reference manifest path escapes recovered text scope")
        if entry["path"] in expected:
            raise ValueError("Duplicate reference manifest path")
        expected.add(entry["path"])
        content = path.read_bytes()
        if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise ValueError(f"Reference artifact changed: {entry['path']}")
        if not content or b"SPDX-License-Identifier: LicenseRef-Pycom-Unresolved" not in content.splitlines()[0]:
            raise ValueError(f"Missing reference rights notice: {entry['path']}")
        if re.search(rb"-----BEGIN [A-Z ]+-----", content):
            raise ValueError(f"Unexpected PEM content: {entry['path']}")
        if re.search(rb"[a-z]+://[^/\s]+:[^/\s]+@", content):
            raise ValueError(f"Unexpected URL credentials: {entry['path']}")
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / "recovered").rglob("*") if p.is_file()}
    if actual != expected:
        raise ValueError("Unlisted or missing recovered files")
    for module in manifest["application_analysis"]:
        if f"recovered/{module['module']}.dis.txt" not in expected:
            raise ValueError("Missing candidate module disassembly")
    if manifest["redacted_literal_count"] and not any(
            b"[REDACTED]" in (ROOT / name).read_bytes() for name in expected):
        raise ValueError("Redaction metadata has no matching marker in reference texts")
    print(f"Recovery provenance passed: {ROOT.name}, {len(expected)} reference texts and hashes; PEM scan passed.")


def main():
    for root in sorted(RESEARCH.iterdir()):
        if (root / "manifest.json").exists():
            check_snapshot(root)


if __name__ == "__main__":
    main()
