"""Scope: Verify portable downloads survive relocation and exclude local project data."""

import hashlib
from pathlib import Path
import re
import subprocess
import sys
import zipfile

import yaml


class TestPortablePackage:
    """Exercise release artifacts through their public entrypoints."""

    root = Path(__file__).resolve().parents[1]

    def build(self, output: Path) -> None:
        subprocess.run(
            [sys.executable, str(self.root / "scripts/build_portable_package.py"), "--check", "--output", str(output)],
            cwd=self.root,
            check=True,
        )

    def test_reproducible_archive_runs_after_extraction(self, tmp_path: Path) -> None:
        first, second = tmp_path / "first", tmp_path / "second"
        for output in (first, second):
            self.build(output)
        for name in ("aikea-skill.zip", "AIKEA_CHAT.md", "SHA256SUMS"):
            assert (first / name).read_bytes() == (second / name).read_bytes()
        for entry in (first / "SHA256SUMS").read_text().splitlines():
            digest, name = entry.split()
            assert hashlib.sha256((first / name).read_bytes()).hexdigest() == digest
        source_url = "https://raw.githubusercontent.com/PatrickGrothOls/AIkea-skill/v0.1.0-alpha.2/"
        for target in re.findall(r"\]\(([^)]+)\)", (first / "AIKEA_CHAT.md").read_text()):
            assert "://" in target, f"A standalone guide cannot resolve a relative link: {target}"
            if target.startswith(source_url):
                assert (self.root / target.removeprefix(source_url).split("#", 1)[0]).is_file()
        with zipfile.ZipFile(first / "aikea-skill.zip") as bundle:
            assert bundle.testzip() is None
            assert all(Path(name).parts[0] == "aikea" for name in bundle.namelist())
            bundle.extractall(tmp_path / "extracted")
        package = tmp_path / "extracted/aikea"
        metadata = yaml.safe_load((package / "SKILL.md").read_text().split("---", 2)[1])
        assert metadata["name"] == package.name
        assert len(list((package / "skills").glob("*/SKILL.md"))) == 9
        for name in ("THIRD_PARTY_LICENSES.md", "THIRD_PARTY_NOTICES.txt", "SUPPLEMENTAL_LICENSES.md"):
            assert (package / "skills/aikea-review-unit/assets/viewer" / name).is_file()
        for command in (
            ["setup_aikea.py"],
            ["skills/aikea/scripts/calculate_overall_wardrobe.py", "--help"],
            ["skills/aikea-review-unit/scripts/check_fabrication_readiness.py", "--help"],
        ):
            subprocess.run([sys.executable, *command], cwd=package, check=True)

    def test_untracked_client_data_never_enters_the_archive(self, tmp_path: Path) -> None:
        repository = tmp_path / "source"
        repository.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
        inputs = (
            "scripts/build_portable_package.py", "portable/chat-introduction.md",
            "portable/SKILL.md", "portable/setup_aikea.py", "LICENSE.md", "requirements.txt",
            "aikea/SKILL.md", "aikea/references/client-conversation.md",
            "aikea/references/overall-wardrobe-measurements-and-settings.md",
            "aikea/assets/wardrobe-measurement-sheet.md", "aikea/assets/aikea.yaml",
        )
        for name in inputs:
            target = repository / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((self.root / name).read_bytes())
        subprocess.run(["git", "add", "--", *inputs], cwd=repository, check=True)
        private = repository / "aikea/client-project.txt"
        private.write_text("Private project sentinel: never distribute")
        output = tmp_path / "downloads"
        subprocess.run(
            [sys.executable, "scripts/build_portable_package.py", "--output", str(output)],
            cwd=repository,
            check=True,
        )
        with zipfile.ZipFile(output / "aikea-skill.zip") as bundle:
            assert not any("client-project" in name for name in bundle.namelist())
            assert not any(b"Private project sentinel" in bundle.read(name) for name in bundle.namelist())
