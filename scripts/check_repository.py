#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline documentation/link/provenance checks, with no device or network I/O."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "LICENSE.md", "LICENSES/MIT.txt", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "AGENTS.md", "package-lock.json",
    "docs/MAINTENANCE_PLAN.md", "docs/ARCHITECTURE.md", "docs/SUPPORT_MATRIX.md",
    "docs/SOURCE_PROVENANCE.md", "docs/GOVERNANCE.md", ".github/CODEOWNERS",
    ".github/FUNDING.yml", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/repository-checks.yml", ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/hardware_report.yml",
)
INHERITED = {
    "docs/UPSTREAM_README.md": "a1b948b190f5f34591f66baea4e1970f58178e207c6f26f5440e3eb4528bc26e",
    "CHANGELOG.md": "b996d7271cb251f0866f4436daa5ddeece739b7ca12b78c968412afd855e101b",
}
LINK = re.compile(r"!?\[[^\]\n]+\]\(([^\s()]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
ERRORS: list[str] = []


def unfenced(text: str) -> str:
    """Keep prose; links/headings inside fenced examples are not navigation."""
    lines = []
    fence = ""
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if not fence:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = ""
            continue
        if not fence:
            lines.append(line)
    return "\n".join(lines)


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    result = set()
    for title in HEADING.findall(unfenced(path.read_text(encoding="utf-8"))):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f"{slug}-{count}")
    return result


def fail(message: str) -> None:
    ERRORS.append(message)


def check_links(path: Path, text: str) -> None:
    for match in LINK.finditer(unfenced(text)):
        target = urlsplit(match[1])
        if target.scheme or target.netloc:
            continue
        destination = (path.parent / unquote(target.path)).resolve() if target.path else path
        if not destination.is_relative_to(ROOT):
            fail(f"{path.relative_to(ROOT)}: link escapes the repository: {match[1]}")
        elif not destination.exists():
            fail(f"{path.relative_to(ROOT)}: missing local link: {match[1]}")
        elif target.fragment and destination.suffix == ".md":
            if unquote(target.fragment) not in anchors(destination):
                fail(f"{path.relative_to(ROOT)}: missing heading: {match[1]}")


def main() -> int:
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            fail(f"Required file missing: {name}")
    for name, expected in INHERITED.items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            fail(f"Inherited provenance artifact changed: {name}")

    documents = [p for p in ROOT.rglob("*.md") if not any(
        part in {"node_modules", ".git", ".venv"} for part in p.relative_to(ROOT).parts
    ) and str(p.relative_to(ROOT)) not in INHERITED]
    for path in documents:
        text = path.read_text(encoding="utf-8")
        check_links(path, text)
        if not text.endswith("\n"):
            fail(f"{path.relative_to(ROOT)}: missing final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(f"{path.relative_to(ROOT)}:{number}: trailing whitespace")

    for path in (ROOT / ".github/workflows").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for action in re.findall(r"^\s*uses:\s*(\S+)", text, re.MULTILINE):
            if not action.startswith("./") and not re.fullmatch(r"[^@]+@[0-9a-f]{40}", action):
                fail(f"{path.relative_to(ROOT)}: action is not pinned to a full SHA: {action}")
        if re.search(r"\bpull_request_target\s*:", text):
            fail(f"{path.relative_to(ROOT)}: review privileged PR triggers before adding them")

    title = os.environ.get("PR_TITLE", "")
    conventional = r"(?:feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?:\([\w./-]+\))?!?: \S.+"
    if title and (not re.fullmatch(conventional, title) or len(title) > 120 or title.endswith(".")):
        fail("PR title must be a Conventional Commit title, at most 120 characters, without a trailing period")

    for message in ERRORS:
        print(f"ERROR: {message}", file=sys.stderr)
    if ERRORS:
        return 1
    print(f"Repository checks passed: {len(documents)} community documents, local links, provenance, action pins, and PR title.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
