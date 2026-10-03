"""Scope: Record generator-owned door feature files without claiming reviews."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from generated_file_record import GeneratedFileRecord, GeneratedFileRecordError


class DoorGeneratedFileRecordError(GeneratedFileRecordError):
    """Report an unreadable or unsupported door ownership record."""


@dataclass(frozen=True)
class DoorGeneratedFileRecord(GeneratedFileRecord):
    """Prove which unchanged door files remain owned by their generator."""

    assembly_id: str

    SCHEMA_VERSION = 1

    @classmethod
    def load(cls, project_root: Path, assembly_id: str) -> "DoorGeneratedFileRecord":
        relative = cls.path_for(assembly_id)
        path = project_root / relative
        if not path.exists():
            return cls({}, assembly_id)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise DoorGeneratedFileRecordError(
                f"cannot read {relative}: {error}"
            ) from error
        if not isinstance(data, dict) or data.get("schema_version") != cls.SCHEMA_VERSION:
            raise DoorGeneratedFileRecordError(f"unsupported record: {relative}")
        files = data.get("files")
        if not isinstance(files, dict) or not all(
            isinstance(file_path, str) and isinstance(digest, str)
            for file_path, digest in files.items()
        ):
            raise DoorGeneratedFileRecordError(f"invalid files in {relative}")
        return cls(
            {Path(file_path): digest for file_path, digest in files.items()},
            assembly_id,
        )

    @classmethod
    def from_rendered(
        cls,
        assembly_id: str,
        files: dict[Path, str],
    ) -> "DoorGeneratedFileRecord":
        return cls(
            {
                relative: cls._digest(content.encode("utf-8"))
                for relative, content in files.items()
            },
            assembly_id,
        )

    @classmethod
    def path_for(cls, assembly_id: str) -> Path:
        return Path("assemblies") / assembly_id / "door_hinges/generated-files.json"

    def save(self, project_root: Path) -> None:
        path = project_root / self.path_for(self.assembly_id)
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


__all__ = ["DoorGeneratedFileRecord", "DoorGeneratedFileRecordError"]
