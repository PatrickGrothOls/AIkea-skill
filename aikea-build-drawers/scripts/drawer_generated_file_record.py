"""Scope: Record generator-owned drawer files without claiming cabinet taxonomy files."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from generated_file_record import GeneratedFileRecord, GeneratedFileRecordError


class DrawerGeneratedFileRecordError(GeneratedFileRecordError):
    """Report an unreadable or unsupported drawer ownership record."""


@dataclass(frozen=True)
class DrawerGeneratedFileRecord(GeneratedFileRecord):
    """Prove which unchanged drawer files remain owned by their generator."""

    parent_assembly_id: str

    SCHEMA_VERSION = 1

    @classmethod
    def load(
        cls,
        project_root: Path,
        parent_assembly_id: str,
    ) -> "DrawerGeneratedFileRecord":
        relative = cls.path_for(parent_assembly_id)
        path = project_root / relative
        if not path.exists():
            return cls({}, parent_assembly_id)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise DrawerGeneratedFileRecordError(
                f"cannot read {relative}: {error}"
            ) from error
        if not isinstance(data, dict):
            raise DrawerGeneratedFileRecordError(f"invalid object in {relative}")
        if data.get("schema_version") != cls.SCHEMA_VERSION:
            raise DrawerGeneratedFileRecordError(
                f"unsupported {relative} schema version"
            )
        files = data.get("files")
        if not isinstance(files, dict) or not all(
            isinstance(file_path, str) and isinstance(digest, str)
            for file_path, digest in files.items()
        ):
            raise DrawerGeneratedFileRecordError(f"invalid files in {relative}")
        return cls(
            {Path(file_path): digest for file_path, digest in files.items()},
            parent_assembly_id,
        )

    @classmethod
    def from_rendered(
        cls,
        parent_assembly_id: str,
        files: dict[Path, str],
    ) -> "DrawerGeneratedFileRecord":
        return cls(
            {
                relative: cls._digest(content.encode("utf-8"))
                for relative, content in files.items()
            },
            parent_assembly_id,
        )

    @classmethod
    def path_for(cls, parent_assembly_id: str) -> Path:
        return (
            Path("assemblies")
            / parent_assembly_id
            / "drawers/generated-files.json"
        )

    def save(self, project_root: Path) -> None:
        path = project_root / self.path_for(self.parent_assembly_id)
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


__all__ = ["DrawerGeneratedFileRecord", "DrawerGeneratedFileRecordError"]
