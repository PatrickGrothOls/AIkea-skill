"""Scope: Write a rendered assembly taxonomy without overwriting local work."""

from __future__ import annotations

from pathlib import Path


class AssemblyTaxonomyConflict(ValueError):
    """Report generated paths that contain differing existing content."""

    def __init__(self, paths: tuple[Path, ...]) -> None:
        self.paths = paths
        super().__init__(
            "existing local files differ: " + ", ".join(str(path) for path in paths)
        )


class AssemblyTaxonomyWriter:
    """Check the complete write set before creating any missing files."""

    def write(self, project_root: Path, files: dict[Path, str]) -> tuple[Path, ...]:
        conflicts = tuple(
            relative
            for relative, content in files.items()
            if self._differs(project_root / relative, content)
        )
        if conflicts:
            raise AssemblyTaxonomyConflict(conflicts)
        written: list[Path] = []
        for relative, content in files.items():
            path = project_root / relative
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(relative)
        return tuple(written)

    def _differs(self, path: Path, content: str) -> bool:
        return path.exists() and (
            not path.is_file() or path.read_text(encoding="utf-8") != content
        )
