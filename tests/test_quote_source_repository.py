"""Scope: Prove source packaging preserves editable work and excludes heavy exports."""

import io
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile

import pytest

from quote_source_repository import QuoteSourceRepository


class TestQuoteSourceRepository:
    def repository(self, root):
        subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
        self.write(root, "requirements.txt", "cadquery==2.7.0")
        self.write(root, "assemblies/wardrobe/builder.py", "WIDTH = 600")
        self.write(root, "assemblies/another-customer/builder.py", "PRIVATE = True")
        self.write(root, ".env", "EXAMPLE_SECRET=must-not-leave")
        self.write(root, "assemblies/wardrobe/panel.step", "heavy generated STEP")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "fixture"], check=True)
        return QuoteSourceRepository(root, root / "assemblies/wardrobe")

    def write(self, root, name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_keeps_dirty_code_and_new_design_files_but_no_step_or_secrets(self, tmp_path):
        repository = self.repository(tmp_path)
        self.write(tmp_path, "assemblies/wardrobe/builder.py", "WIDTH = 700")
        self.write(tmp_path, "assemblies/wardrobe/new_part.py", "THICKNESS = 18")
        self.write(tmp_path, "assemblies/wardrobe/output.glb", "generated model")
        self.write(tmp_path, "assemblies/wardrobe/.env", "OTHER_SECRET=do-not-send")
        with ZipFile(io.BytesIO(repository.build())) as archive:
            names = archive.namelist()
            assert archive.read("repository/assemblies/wardrobe/builder.py") == b"WIDTH = 700"
            assert archive.read("repository/assemblies/wardrobe/new_part.py") == b"THICKNESS = 18"
            assert "repository/requirements.txt" in names
            assert not any(name.endswith((".step", ".glb", ".env")) for name in names)
            assert not any("another-customer" in name for name in names)
            manifest = json.loads(archive.read("source-manifest.json"))
            assert len(manifest["base_revision"]) == 40
            assert "assemblies/wardrobe/new_part.py" in manifest["files"]

    def test_refuses_symlink_to_outside_source(self, tmp_path):
        repository = self.repository(tmp_path)
        (tmp_path / "assemblies/wardrobe/escape.py").symlink_to(tmp_path / "requirements.txt")
        with pytest.raises(ValueError, match="symlinks"):
            repository.build()

    def test_deleted_source_is_not_resurrected_from_git(self, tmp_path):
        repository = self.repository(tmp_path)
        (tmp_path / "requirements.txt").unlink()
        with ZipFile(io.BytesIO(repository.build())) as archive:
            assert "repository/requirements.txt" not in archive.namelist()

    def test_includes_untracked_branch_documentation(self, tmp_path):
        repository = self.repository(tmp_path)
        self.write(tmp_path, "docs/new-branch.md", "Current branch plan and audit log")
        with ZipFile(io.BytesIO(repository.build())) as archive:
            assert archive.read("repository/docs/new-branch.md") == b"Current branch plan and audit log"

    def test_new_shared_dependencies_are_included_without_exports_or_other_designs(self, tmp_path):
        repository = self.repository(tmp_path)
        self.write(tmp_path, "assemblies/wardrobe/builder.py", "from shared_dimensions import WIDTH")
        self.write(tmp_path, "shared_dimensions.py", "WIDTH = 720")
        self.write(tmp_path, "lib/materials.py", "THICKNESS = 18")
        self.write(tmp_path, "assemblies/another-customer/new.py", "PRIVATE = True")
        self.write(tmp_path, "credentials.json", "not for upload")
        self.write(tmp_path, "lib/export.step", "not for upload")
        self.write(tmp_path, ".gitignore", "scratch/\n")
        self.write(tmp_path, "scratch/notes.txt", "ignored scratch data")
        with ZipFile(io.BytesIO(repository.build())) as archive:
            assert archive.read("repository/shared_dimensions.py") == b"WIDTH = 720"
            assert archive.read("repository/lib/materials.py") == b"THICKNESS = 18"
            names = archive.namelist()
            assert not any("another-customer" in name or "scratch/" in name for name in names)
            assert not any(name.endswith(("credentials.json", ".step")) for name in names)
