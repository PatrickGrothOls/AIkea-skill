"""Scope: Load and validate immutable bytes for one GLB v2 artifact."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import struct

from unit_mockup import UnitMockupInputError


@dataclass(frozen=True, slots=True)
class GlbArtifactSnapshot:
    """Bind a resolved path, validated GLB bytes, and their SHA-256 digest."""

    path: Path
    content: bytes
    sha256: str

    @classmethod
    def load(cls, path: Path) -> "GlbArtifactSnapshot":
        resolved = path.resolve()
        try:
            content = resolved.read_bytes()
        except OSError as error:
            raise UnitMockupInputError([f"GLB cannot be read: {resolved}"]) from error
        header = content[:12]
        if len(header) != 12:
            raise UnitMockupInputError([f"GLB has an invalid header: {resolved}"])
        magic, version, declared_length = struct.unpack("<4sII", header)
        if magic != b"glTF" or version != 2 or declared_length != len(content):
            raise UnitMockupInputError([f"GLB has an invalid header: {resolved}"])
        return cls(resolved, content, sha256(content).hexdigest())


__all__ = ["GlbArtifactSnapshot"]
