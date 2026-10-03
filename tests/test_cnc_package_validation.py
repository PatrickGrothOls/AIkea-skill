"""Scope: Exercise hostile archive boundaries and source/document preservation."""

import hashlib
import io
import json
from pathlib import Path
import stat
import struct
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import zlib

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-intake"))
from package_validation import PackageValidation
from preview_validation import PreviewValidation


class TestPackageValidation:
    def archive(self, extra=None, manifest_change=None):
        files = {"assemblies/test/builder.py": b"raise RuntimeError('must never execute')", "docs/branch.md": b"Plan"}
        files.update(extra or {})
        manifest = {"format": "aikea-source-repository-v1", "base_revision": "a" * 40,
                    "project_path": "assemblies/test", "files": {n: hashlib.sha256(v).hexdigest() for n, v in files.items()}}
        manifest.update(manifest_change or {})
        output = io.BytesIO()
        with ZipFile(output, "w", ZIP_DEFLATED) as archive:
            for name, value in files.items():
                archive.writestr("repository/" + name, value)
            archive.writestr("source-manifest.json", json.dumps(manifest))
        return output.getvalue()

    def test_accepts_code_and_docs_without_executing(self):
        manifest = PackageValidation().validate(self.archive())
        assert "docs/branch.md" in manifest["files"]

    @pytest.mark.parametrize("name", ["../escape.py", "/absolute.py", "docs/../../bad.py", "a\\bad.py",
                                      ".git/config", ".env", "panel.STEP", "panel.glb", "secrets.json", "a:stream.py"])
    def test_rejects_forbidden_paths(self, name):
        with pytest.raises(ValueError, match="forbidden"):
            PackageValidation().validate(self.archive({name: b"bad"}))

    def test_rejects_hash_mismatch(self):
        with pytest.raises(ValueError, match="checksum"):
            PackageValidation().validate(self.archive(manifest_change={"files": {
                "assemblies/test/builder.py": "0" * 64, "docs/branch.md": "0" * 64}}))

    def test_rejects_missing_manifest_entries(self):
        with pytest.raises(ValueError, match="exactly"):
            PackageValidation().validate(self.archive(manifest_change={"files": {}}))

    def test_rejects_duplicate_and_symlink_entries(self):
        for symlink in [False, True]:
            output = io.BytesIO(self.archive())
            with ZipFile(output, "a") as archive:
                entry = ZipInfo("repository/link.py" if symlink else "repository/DOCS/BRANCH.md")
                entry.external_attr = (stat.S_IFLNK | 0o777) << 16 if symlink else 0
                archive.writestr(entry, b"target")
            with pytest.raises(ValueError):
                PackageValidation().validate(output.getvalue())

    def test_rejects_zip_bomb_before_reading_content(self):
        with pytest.raises(ValueError, match="entry"):
            PackageValidation().validate(self.archive({"big.txt": b"x" * 8_000_001}))

    def test_rejects_filename_truncation_at_embedded_nul(self):
        content = self.archive({"nul.pyXignored": b"untrusted"}).replace(b"nul.pyXignored", b"nul.py\x00ignored")
        with pytest.raises(ValueError, match="entry"):
            PackageValidation().validate(content)


class TestPreviewValidation:
    def png(self, width=1, height=1):
        chunks = [(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
                  (b"IDAT", zlib.compress(b"\x00\x00\x00\x00")), (b"IEND", b"")]
        return b"\x89PNG\r\n\x1a\n" + b"".join(struct.pack(">I", len(data)) + kind + data
                                                    + struct.pack(">I", zlib.crc32(kind + data)) for kind, data in chunks)

    def test_valid_preview(self):
        PreviewValidation().validate(self.png())

    @pytest.mark.parametrize("kind", ["huge", "truncated", "trailing", "checksum"])
    def test_invalid_preview(self, kind):
        png = {"huge": self.png(10000), "truncated": self.png()[:-4],
               "trailing": self.png() + b"extra", "checksum": self.png()[:-1] + b"x"}[kind]
        with pytest.raises(ValueError):
            PreviewValidation().validate(png)
