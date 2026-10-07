#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Apply the documented reference-text transform; does not establish source rights."""

import argparse
import hashlib
import json
from pathlib import Path

NOTICE = (
    "# Pycom-derived reference artifact. SPDX-License-Identifier: LicenseRef-Pycom-Unresolved\n"
    "# Historical static recovery; not a community runtime or MIT source.\n"
    "# Source paths normalized. See ../README.md and ../../../LICENSE.md.\n"
    "# Automatic decompilation may omit or mistranslate code, even when syntax is valid.\n\n"
)


def publish(source, output, provenance):
    manifest = json.loads((source / "manifest.json").read_text())
    metadata = json.loads(provenance.read_text())
    if set(metadata) - {"artifact", "tools", "validation", "normalizations"}:
        raise ValueError("Provenance cannot override generated analysis or input identity")
    output.mkdir(parents=True, exist_ok=False)
    (output / "recovered").mkdir()
    for path in sorted((source / "recovered").iterdir()):
        if path.is_symlink() or not path.is_file() or path.suffix != ".txt":
            raise ValueError("Only recovered text artifacts may be published")
        content = path.read_text(encoding="utf-8")
        if content.strip():
            (output / "recovered" / path.name).write_text(NOTICE + content.rstrip("\n") + "\n", encoding="utf-8")
    additional_normalizations = metadata.pop("normalizations", [])
    manifest.update(metadata)
    manifest["normalizations"] = manifest.get("normalizations", []) + additional_normalizations
    manifest["schema_version"] = 2
    manifest["publication_transform"] = "tools/publish_reference.py: prepend NOTICE, omit empty text, normalize final newline, hash final bytes"
    manifest["rights"] = {
        "community_authorship": "MIT for original manifest structure, hashes, prose, tools and tests",
        "derived_references": "Recovered text and derived symbol/name inventory: LicenseRef-Pycom-Unresolved",
    }
    manifest["published_files"] = [
        {"path": str(p.relative_to(output)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
         "bytes": p.stat().st_size}
        for p in sorted((output / "recovered").iterdir())
    ]
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    args = parser.parse_args()
    publish(args.source, args.output, args.provenance)
