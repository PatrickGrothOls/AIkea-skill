"""Scope: Verify portable archive reproducibility, scope and integrity rejection."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "portable")]
from build_portable_package import PortablePackage
from package_integrity import PackageIntegrity


class PortablePackageTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        self.package = PortablePackage(self.root)
        self.git("init", "-q")
        for name, content in {"aikea/SKILL.md": "# Skill", "portable/setup.sh": "true\n",
                              "portable/start-prompt.txt": "{download_url} {sha256}",
                              "requirements.txt": "cadquery==2.7.0\n",
                              "private.txt": "must not be packaged"}.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-qm", "fixture")
        (self.root / "aikea/untracked-secret.txt").write_text("never package")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def test_reproducible_archive_only_contains_distributable_tracked_members(self):
        outputs = [Path(self.temp.name) / name for name in ("first", "second")]
        for output in outputs:
            self.package.build(output, "0.1.0-desktop.1")
        archives = [(path / "aikea-skill.zip").read_bytes() for path in outputs]
        self.assertEqual(archives[0], archives[1])
        with zipfile.ZipFile(outputs[0] / "aikea-skill.zip") as bundle:
            self.assertEqual(set(bundle.namelist()), {"aikea/skills/aikea/SKILL.md",
                             "aikea/setup.sh", "aikea/requirements.txt", "aikea/package-manifest.json"})
            bundle.extractall(Path(self.temp.name) / "extract")
        extracted = Path(self.temp.name) / "extract/aikea"
        self.assertEqual(PackageIntegrity().verify(extracted)["version"], "0.1.0-desktop.1")
        (extracted / "setup.sh").write_text("tampered")
        with self.assertRaisesRegex(ValueError, "integrity failed"):
            PackageIntegrity().verify(extracted)

    def test_no_prompt_without_url_and_exact_hash_with_explicit_url(self):
        local = Path(self.temp.name) / "local"
        self.package.build(local, "0.1.0-desktop.1")
        self.assertFalse((local / "START_PROMPT.txt").exists())
        remote = Path(self.temp.name) / "remote"
        self.package.build(remote, "0.1.0-desktop.1", "https://example.invalid/candidate.zip")
        digest = hashlib.sha256((remote / "aikea-skill.zip").read_bytes()).hexdigest()
        self.assertIn(digest, (remote / "START_PROMPT.txt").read_text())
        self.assertEqual(json.loads((remote / "distribution.json").read_text())["status"],
                         "CANDIDATE_URL_UNVERIFIED")

    def test_dirty_tracked_files_and_existing_candidate_are_rejected(self):
        output = Path(self.temp.name) / "candidate"
        self.package.build(output, "0.1.0-desktop.1")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            self.package.build(output, "0.1.0-desktop.1")
        (self.root / "aikea/SKILL.md").write_text("uncommitted change")
        with self.assertRaisesRegex(ValueError, "Commit tracked changes"):
            self.package.build(Path(self.temp.name) / "dirty", "0.1.0-desktop.1")

    def test_manifest_cannot_read_outside_extraction(self):
        (self.root / "package-manifest.json").write_text(json.dumps({
            "version": "test", "source_revision": "test", "files": {"../outside": "hash"}}))
        with self.assertRaisesRegex(ValueError, "Unsafe package member"):
            PackageIntegrity().verify(self.root)

    def test_symlink_member_is_rejected(self):
        link = self.root / "aikea/link"
        link.symlink_to(self.root / "private.txt")
        self.git("add", "aikea/link")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.package.members()

    def test_corrupt_bootstrap_download_stops_before_extract_or_python_install(self):
        runtime = Path(self.temp.name) / "runtime"
        (runtime / "tools").mkdir(parents=True)
        (runtime / "tools/uv.tar.gz").write_bytes(b"corrupt cached download")
        result = subprocess.run(["bash", str(ROOT / "portable/setup.sh"), str(runtime)],
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKED stage=verify_uv", result.stderr)
        self.assertFalse((runtime / "tools/uv").exists())
        self.assertFalse((runtime / "cad").exists())


if __name__ == "__main__":
    unittest.main()
