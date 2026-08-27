"""Scope: Record exact generated project files for safe later regeneration."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path


class GeneratedFileRecordError(ValueError):
    """Report an unreadable or unsupported generated-file record."""


@dataclass(frozen=True)
class GeneratedFileRecord:
    """Prove which unchanged project files remain owned by the generator."""

    files: dict[Path, str]

    PATH = Path("assemblies/generated-files.json")
    SCHEMA_VERSION = 1

    @classmethod
    def load(cls, project_root: Path) -> "GeneratedFileRecord":
        path = project_root / cls.PATH
        if not path.exists():
            return cls({})
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise GeneratedFileRecordError(
                f"cannot read {cls.PATH}: {error}"
            ) from error
        if not isinstance(data, dict):
            raise GeneratedFileRecordError(f"invalid object in {cls.PATH}")
        if data.get("schema_version") != cls.SCHEMA_VERSION:
            raise GeneratedFileRecordError(
                f"unsupported {cls.PATH} schema version"
            )
        files = data.get("files")
        if not isinstance(files, dict) or not all(
            isinstance(path, str) and isinstance(digest, str)
            for path, digest in files.items()
        ):
            raise GeneratedFileRecordError(f"invalid files in {cls.PATH}")
        return cls({Path(path): digest for path, digest in files.items()})

    @classmethod
    def from_rendered(cls, files: dict[Path, str]) -> "GeneratedFileRecord":
        return cls(
            {
                relative: cls._digest(content.encode("utf-8"))
                for relative, content in files.items()
            }
        )

    def matches(self, relative: Path, path: Path) -> bool:
        expected = self.files.get(relative)
        return bool(
            expected
            and path.is_file()
            and self._digest(path.read_bytes()) == expected
        )

    def save(self, project_root: Path) -> None:
        path = project_root / self.PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "schema_version": self.SCHEMA_VERSION,
            "files": {
                relative.as_posix(): digest
                for relative, digest in sorted(
                    self.files.items(), key=lambda item: item[0].as_posix()
                )
            },
        }
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def _digest(content: bytes) -> str:
        return sha256(content).hexdigest()
