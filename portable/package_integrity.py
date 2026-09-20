"""Scope: Check extracted package members against its release manifest before setup."""

import hashlib
import json
from pathlib import Path


class PackageIntegrity:
    def verify(self, directory):
        root = Path(directory).resolve()
        manifest = json.loads((root / "package-manifest.json").read_text())
        for name, expected in manifest["files"].items():
            path = root / name
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError(f"Unsafe package member: {name}")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"Package integrity failed: {name}")
        return {key: manifest[key] for key in ("version", "source_revision")}
