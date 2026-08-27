"""Scope: Write a rendered assembly taxonomy without overwriting local work."""

from __future__ import annotations

from pathlib import Path

from generated_file_record import GeneratedFileRecord


class AssemblyTaxonomyConflict(ValueError):
    """Report generated paths that contain differing existing content."""

    def __init__(self, paths: tuple[Path, ...]) -> None:
        self.paths = paths
        super().__init__(
            "existing local files differ: " + ", ".join(str(path) for path in paths)
        )


class AssemblyTaxonomyWriter:
    """Check the complete write set before creating any missing files."""

    def write(
        self,
        project_root: Path,
        files: dict[Path, str],
        replaceable: dict[Path, tuple[str, ...]] | None = None,
        recorded: GeneratedFileRecord | None = None,
    ) -> tuple[Path, ...]:
        replaceable = replaceable or {}
        conflicts = tuple(
            relative
            for relative, content in files.items()
            if self._differs(project_root / relative, content)
            and not self._matches(project_root / relative, replaceable.get(relative))
            and not (
                recorded
                and recorded.matches(relative, project_root / relative)
            )
        )
        if conflicts:
            raise AssemblyTaxonomyConflict(conflicts)
        written: list[Path] = []
        for relative, content in files.items():
            path = project_root / relative
            if path.is_file() and path.read_text(encoding="utf-8") == content:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(relative)
        return tuple(written)

    def _differs(self, path: Path, content: str) -> bool:
        return path.exists() and (
            not path.is_file() or path.read_text(encoding="utf-8") != content
        )

    def _matches(self, path: Path, contents: tuple[str, ...] | None) -> bool:
        return bool(
            contents
            and path.is_file()
            and path.read_text(encoding="utf-8") in contents
        )
