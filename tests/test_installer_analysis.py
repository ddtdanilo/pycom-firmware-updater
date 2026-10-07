# SPDX-License-Identifier: MIT
"""Synthetic archive failures, credential redaction, and non-execution checks."""

import importlib.util
import json
import marshal
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zlib

SPEC = importlib.util.spec_from_file_location(
    "analysis", Path(__file__).resolve().parents[1] / "tools/analyze_installer.py")
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)
PUBLISH_SPEC = importlib.util.spec_from_file_location(
    "publication", Path(__file__).resolve().parents[1] / "tools/publish_reference.py")
publication = importlib.util.module_from_spec(PUBLISH_SPEC)
PUBLISH_SPEC.loader.exec_module(publication)


def pyz(name, raw):
    compressed = zlib.compress(raw)
    offset = 12 + len(compressed)
    return b"PYZ\0" + b"TEST" + struct.pack("!i", offset) + compressed + marshal.dumps(
        [(name, (0, 12, len(compressed)))])


def archive(name, raw, compressed=False):
    data = zlib.compress(raw) if compressed else raw
    encoded = name.encode() + b"\0"
    toc = analysis.ENTRY.pack(analysis.ENTRY.size + len(encoded), 0, len(data),
                              len(raw), int(compressed), b"z") + encoded
    length = len(data) + len(toc) + analysis.COOKIE.size
    version = sys.version_info.major * 100 + sys.version_info.minor
    return b"synthetic-bootloader" + data + toc + analysis.COOKIE.pack(
        analysis.MAGIC, length, len(data), len(toc), version, b"Python")


class InspectionTests(unittest.TestCase):
    def test_publication_cannot_override_analyzed_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "manifest.json").write_text(json.dumps({"executable_sha256": "actual"}))
            provenance = root / "provenance.json"
            provenance.write_text(json.dumps({"executable_sha256": "replacement"}))
            with self.assertRaises(ValueError):
                publication.publish(source, root / "output", provenance)
            self.assertFalse((root / "output").exists())

    def test_archive_bounds_and_compression(self):
        _, entries, files = analysis.parse_archive(archive("PYZ-00.pyz", b"example", True))
        self.assertEqual(files["PYZ-00.pyz"], b"example")
        self.assertEqual(entries[0]["bytes"], 7)
        with self.assertRaises(ValueError):
            analysis.region(b"abc", -1, 1)
        with self.assertRaises(ValueError):
            analysis.region(b"abc", 1, 10)

    def test_missing_or_truncated_cookie(self):
        for data in (b"not-an-archive", analysis.MAGIC):
            with self.subTest(data=data), self.assertRaises(ValueError):
                analysis.parse_archive(data)

    def test_path_traversal_is_rejected(self):
        for name in ("../escaped", "/absolute", "safe/../../bad", "safe\\..\\bad"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                analysis.parse_archive(archive(name, b"data"))

    def test_compression_size_mismatch_and_junk(self):
        with self.assertRaises(ValueError):
            analysis.inflate(zlib.compress(b"data"), 99)
        with self.assertRaises(ValueError):
            analysis.inflate(zlib.compress(b"data") + b"junk")
        with self.assertRaises(ValueError):
            analysis.inflate(zlib.compress(b"data")[:-1])

    def test_cumulative_expansion_budget(self):
        with patch.object(analysis, "MAX_TOTAL_EXPANDED", 3):
            with self.assertRaises(ValueError):
                analysis.parse_archive(archive("PYZ-00.pyz", b"data"))
            with self.assertRaises(ValueError):
                analysis.parse_pyz(pyz("module", b"data"))

    def test_bytes_pem_and_url_redaction_keeps_unrelated_substrings(self):
        code = compile("PASSWORD = b'example'\nURL = 'wss://u:p@localhost'\nCERT = '-----BEGIN CERTIFICATE-----x'\nMESSAGE = 'example of a message'\n", "fixture", "exec")
        clean = analysis.sanitized(code, analysis.secret_literals(code), "fixture")
        self.assertNotIn(b"example", clean.co_consts)
        self.assertIn(b"[REDACTED]", clean.co_consts)
        self.assertNotIn("wss://u:p@localhost", clean.co_consts)
        self.assertNotIn("-----BEGIN CERTIFICATE-----x", clean.co_consts)
        self.assertIn("example of a message", clean.co_consts)

    def test_invalid_pyz_offset_and_name(self):
        with self.assertRaises(ValueError):
            analysis.parse_pyz(b"PYZ\0TEST" + struct.pack("!i", 999))
        with self.assertRaises(ValueError):
            analysis.parse_pyz(pyz("../bad", b"unused"))

    def test_static_inspection_redacts_and_does_not_execute(self):
        source = "CERT_PEM_USERNAME = 'synthetic-user'\nCERT_PEM_PASSWORD = 'synthetic-password'\nraise RuntimeError('MUST_NOT_EXECUTE')\n"
        raw = marshal.dumps(compile(source, "/private/build/settings.py", "exec"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "fixture"
            executable.write_bytes(archive("PYZ-00.pyz", pyz("settings", raw)))
            result = analysis.inspect(executable, root / "output")
            self.assertEqual(result["redacted_literal_count"], 2)
            output = (root / "output/recovered/settings.dis.txt").read_text()
            for excluded in ("synthetic-user", "synthetic-password", "/private/build/"):
                self.assertNotIn(excluded, output)
            self.assertIn("[REDACTED]", output)
            self.assertIn("MUST_NOT_EXECUTE", output)
            manifest = json.loads((root / "output/manifest.json").read_text())
            self.assertEqual(manifest["application_analysis"][0]["module"], "settings")
            with self.assertRaises(ValueError):
                analysis.inspect(executable, root / "bad", decompiler=executable)
            with self.assertRaises(FileExistsError):
                analysis.inspect(executable, root / "output")


if __name__ == "__main__":
    unittest.main()
