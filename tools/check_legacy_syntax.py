#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline grammar-only check with CPython 3.9 lib2to3; never execute previews."""

import argparse
import json
from pathlib import Path
import sys


def main():
    if sys.version_info[:2] != (3, 9):
        raise SystemExit("Use isolated Python 3.9 for the documented lib2to3 check")
    from lib2to3.refactor import RefactoringTool
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    grammar = RefactoringTool([])
    results = {}
    for path in sorted((args.snapshot / "recovered").glob("*.py.txt")):
        try:
            grammar.refactor_string(path.read_text(encoding="utf-8"), path.name)
            results[path.name] = "passed"
        except Exception as error:
            results[path.name] = type(error).__name__
    report = {"method": "CPython 3.9 lib2to3 permissive Python-2-compatible grammar",
              "scope": "Grammar only; not compilation, equivalence, or execution", "results": results}
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if not results or any(value != "passed" for value in results.values()):
        raise SystemExit("Legacy preview grammar check failed")
    print(f"Legacy grammar check passed for {len(results)} previews; no code executed.")


if __name__ == "__main__":
    main()
