"""Scope: Snapshot editable repository code and one design, excluding CAD exports."""

import hashlib
import io
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

from source_package_rules import SourcePackageRules


class QuoteSourceRepository:
    def __init__(self, root: Path, project: Path) -> None:
        self.root = root.resolve()
        self.project = project.resolve().relative_to(self.root)
        if self.project == Path(".") or not (self.root / self.project).is_dir():
            raise ValueError("Choose the design subdirectory inside its source repository.")

    def build(self) -> bytes:
        repo_root = Path(self._git("rev-parse", "--show-toplevel").strip()).resolve()
        if repo_root != self.root:
            raise ValueError("Source root must be the repository root.")
        revision = self._git("rev-parse", "HEAD").strip()
        source = [Path(name) for name in self._git(
            "ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0") if name]
        project_files = [path.relative_to(self.root) for path in (self.root / self.project).rglob("*")
                         if path.is_file()]
        docs = [path.relative_to(self.root) for path in (self.root / "docs").rglob("*.md") if path.is_file()]
        names = sorted(set(source + project_files + docs))
        contents = {}
        total = 0
        for relative in names:
            if not self._include(relative):
                continue
            path = self.root / relative
            if not path.exists():  # Preserve tracked deletions in this working-copy snapshot.
                continue
            if path.is_symlink() or path.resolve() != path.absolute():
                raise ValueError(f"Source package cannot follow symlinks: {relative}")
            total += path.stat().st_size
            if total > 64_000_000:
                raise ValueError("Editable source exceeds the 64 MB request limit.")
            contents[relative.as_posix()] = path.read_bytes()
        design_python = [name for name in contents if Path(name).is_relative_to(self.project) and name.endswith(".py")]
        if not design_python:
            raise ValueError("The selected design has no editable Python source to send.")
        manifest = {"format": "aikea-source-repository-v1", "base_revision": revision,
                    "snapshot": "working_copy_including_uncommitted_design_source",
                    "project_path": self.project.as_posix(),
                    "excluded": "Git history, credentials, generated CAD and render exports",
                    "files": {name: hashlib.sha256(data).hexdigest() for name, data in contents.items()}}
        output = io.BytesIO()
        with ZipFile(output, "w", ZIP_DEFLATED) as archive:
            for name, data in contents.items():
                archive.writestr("repository/" + name, data)
            archive.writestr("source-manifest.json", json.dumps(manifest, indent=2))
        return output.getvalue()

    def _include(self, path: Path) -> bool:
        if not SourcePackageRules.allows(path.as_posix()):
            return False
        # Other designs in a shared skill checkout do not belong to this request.
        if path.parts[0] == "assemblies" and not path.is_relative_to(self.project):
            return len(path.parts) == 2 and path.suffix == ".py"
        return True

    def _git(self, *arguments: str) -> str:
        return subprocess.check_output(["git", "-C", str(self.root), *arguments], text=True)
