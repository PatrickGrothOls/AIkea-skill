"""Scope: Verify indexed privacy checks and ensure diagnostics never echo matched secrets."""

import importlib.util
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("private_check", ROOT / "scripts/check_private_files.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
PrivateFileCheck = MODULE.PrivateFileCheck


class TestPrivateFiles:
    @pytest.mark.parametrize("name", [
        "local-evidence/report.md", "nested/local-evidence/picture.png", ".env", "nested/.env.production",
        ".aws/config", ".ssh/config", ".direnv/cache", ".worktrees/task/source.py",
        "infra/deployment.local.json", "infra/cnc-intake/deployment.local/outputs.json",
        "signing.pem", "private.key", "credentials.json",
    ])
    def test_private_paths_rejected(self, name):
        assert PrivateFileCheck().inspect(name, b"") == [(name, 0, "private-path")]

    @pytest.mark.parametrize("name", [".envrc", ".env.example", "nested/.env.template", "infra/deployment.example.json"])
    def test_safe_configuration_examples_allowed(self, name):
        assert PrivateFileCheck().inspect(name, b"REGION=eu-west-1\n") == []

    @pytest.mark.parametrize("content,rule", [
        (b"AKIA" + b"A" * 16, "aws-access-key"),
        (b"ghp_" + b"a" * 36, "github-token"),
        (b"-----BEGIN " + b"PRIVATE KEY-----", "private-key"),
        (b"sk-proj-" + b"a" * 30, "service-token"),
        (b"export AWS_SECRET_ACCESS_KEY=" + b"AbCd" * 10, "credential-assignment"),
        (b'"password": "' + b"random" * 4 + b'"', "credential-assignment"),
        (b"private.user@" + b"gmail.com", "personal-email"),
    ])
    def test_obvious_credentials_blocked_even_in_example_files(self, content, rule):
        assert (".env.example", 1, rule) in PrivateFileCheck().inspect(".env.example", content)

    def test_scan_uses_index_including_force_added_ignored_files(self, tmp_path, monkeypatch, capsys):
        subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
        secret = "AKIA" + "Z" * 16
        (tmp_path / "public.txt").write_text(secret)
        (tmp_path / ".gitignore").write_text(".env\n")
        (tmp_path / ".env").write_text("REGION=eu-west-1\n")
        subprocess.run(["git", "add", "public.txt", ".gitignore"], cwd=tmp_path, check=True)
        subprocess.run(["git", "add", "-f", ".env"], cwd=tmp_path, check=True)
        (tmp_path / "public.txt").write_text("Clean working copy, still private in the index.")
        monkeypatch.chdir(tmp_path)
        assert PrivateFileCheck().run() == 1
        output = capsys.readouterr().out
        assert "aws-access-key" in output and "private-path" in output
        assert secret not in output
        subprocess.run(["git", "rm", "--cached", "--quiet", ".env"], check=True)
        subprocess.run(["git", "add", "public.txt"], check=True)
        assert PrivateFileCheck().run() == 0
        assert (tmp_path / ".env").is_file()
