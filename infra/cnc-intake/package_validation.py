"""Scope: Inspect bounded source ZIPs without extraction or execution."""

import hashlib
import io
import json
from pathlib import PurePosixPath
import re
import stat
from zipfile import BadZipFile, ZipFile, ZIP_STORED, ZIP_DEFLATED
import zlib

from source_package_rules import SourcePackageRules


class PackageValidation:
    MAX_ZIP = 16_000_000
    MAX_EXPANDED = 64_000_000
    MAX_FILE = 8_000_000
    MAX_ENTRIES = 4000

    def validate(self, content):
        if len(content) > self.MAX_ZIP:
            raise ValueError("Source ZIP exceeds 16 MB.")
        # ZIP parsing is an untrusted input boundary; no file is extracted or imported.
        try:
            with ZipFile(io.BytesIO(content)) as archive:
                return self._archive(archive)
        except (BadZipFile, UnicodeDecodeError, EOFError, zlib.error) as error:
            raise ValueError("Invalid source ZIP.") from error

    def _archive(self, archive):
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if (len(entries) > self.MAX_ENTRIES or len(set(n.casefold() for n in names)) != len(names)
                or sum(e.file_size for e in entries) > self.MAX_EXPANDED):
            raise ValueError("Archive contains duplicates or exceeds expanded limits.")
        for entry in entries:
            mode = stat.S_IFMT(entry.external_attr >> 16)
            if (entry.orig_filename != entry.filename or entry.file_size > self.MAX_FILE or entry.flag_bits & 1
                    or entry.compress_type not in {ZIP_STORED, ZIP_DEFLATED}
                    or mode not in {0, stat.S_IFREG}):
                raise ValueError("Unsupported archive entry.")
            if entry.filename != "source-manifest.json":
                if not entry.filename.startswith("repository/") or not SourcePackageRules.allows(entry.filename[11:]):
                    raise ValueError("Archive contains forbidden source paths or exports.")
        if "source-manifest.json" not in names:
            raise ValueError("Missing source manifest.")
        if archive.getinfo("source-manifest.json").file_size > 1_000_000:
            raise ValueError("Oversized source manifest.")
        manifest = json.loads(archive.read("source-manifest.json"))
        if not isinstance(manifest, dict) or manifest.get("format") != "aikea-source-repository-v1":
            raise ValueError("Unsupported source manifest.")
        files = manifest.get("files")
        if not isinstance(files, dict) or set(names) != {"source-manifest.json", *("repository/" + n for n in files)}:
            raise ValueError("Manifest must list exactly the archived sources.")
        project = manifest.get("project_path", "")
        if not isinstance(project, str) or not SourcePackageRules.allows(project + "/builder.py"):
            raise ValueError("Invalid design directory.")
        if not re.fullmatch(r"[0-9a-f]{40,64}", str(manifest.get("base_revision", ""))):
            raise ValueError("Missing source revision.")
        for name, expected in files.items():
            if hashlib.sha256(archive.read("repository/" + name)).hexdigest() != expected:
                raise ValueError("Source manifest checksum mismatch.")
        if not any(PurePosixPath(n).is_relative_to(project) and n.endswith(".py") for n in files):
            raise ValueError("Missing editable design source.")
        return manifest
