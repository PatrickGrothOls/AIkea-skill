"""Scope: Verify update advice never silently installs, downgrades or claims an offline version current."""

import json
from urllib.error import URLError

import pytest

from skill_release_check import SkillReleaseCheck
from skill_release_version import SkillReleaseVersion


class TestSkillReleaseCheck:
    def _installed(self, version="v0.1.0-alpha.2"):
        return {"repository": SkillReleaseCheck.REPOSITORY, "distribution": "release", "version": version}

    def _release(self, tag="v0.1.0-alpha.3", **changes):
        prefix = f"https://github.com/{SkillReleaseCheck.REPOSITORY}/releases/download/{tag}/"
        return dict({"tag_name": tag, "draft": False, "prerelease": True,
            "published_at": "2026-09-16T10:00:00Z", "assets": [
                {"name": name, "browser_download_url": prefix+name}
                for name in ("aikea-skill.zip", "SHA256SUMS")]}, **changes)

    @pytest.mark.parametrize("installed,available,status", (
        ("v0.1.0-alpha.2", "v0.1.0-alpha.10", "update_available"),
        ("v0.1.0-alpha.2", "v0.1.0-alpha.2", "current"),
        ("v0.2.0", "v0.1.0-alpha.3", "ahead"),
        ("v0.1.0-alpha.3", "v0.1.0", "update_available"),
        ("v0.1.0", "v0.1.0-alpha.3", "ahead")))
    def test_semantic_comparison(self, installed, available, status):
        result = SkillReleaseCheck().compare(self._installed(installed), [self._release(available)])
        assert result["status"] == status

    def test_highest_complete_published_release_not_list_order(self):
        releases = [self._release("v0.1.0-alpha.2"), self._release("v9.0.0", draft=True),
                    self._release("v0.1.0-alpha.10"), self._release("v10.0.0", assets=[]),
                    self._release("vendor-snapshot"), self._release("v11.0.0", published_at=None)]
        result = SkillReleaseCheck().compare(self._installed(), releases)
        assert result["status"] == "update_available"
        assert result["available_version"] == "v0.1.0-alpha.10"

    @pytest.mark.parametrize("identity,status", (
        ({}, "unknown"), ({"distribution": "release", "version": "v0.1.0"}, "unknown"),
        ({"distribution": "development", "version": None}, "development")))
    def test_no_invented_installed_release(self, identity, status):
        assert SkillReleaseCheck().compare(identity, [self._release()])["status"] == status

    def test_nonofficial_assets_not_offered(self):
        release = self._release()
        release["assets"][0]["browser_download_url"] = "https://unrelated.example/skill.zip"
        assert SkillReleaseCheck().compare(self._installed(), [release])["status"] == "unavailable"

    def test_offline_continues_without_current_claim(self, tmp_path, monkeypatch):
        path = tmp_path/"release.json"
        path.write_text(json.dumps(self._installed()))
        monkeypatch.setattr("skill_release_check.urlopen", self._offline)
        result = SkillReleaseCheck().check(path)
        assert result["status"] == "unavailable"
        assert "Continue" in result["action"]
        assert list(tmp_path.iterdir()) == [path]

    def _offline(self, request, timeout):
        assert request.full_url == SkillReleaseCheck.API_URL
        assert 0 < timeout <= 8
        raise URLError("offline")

    def test_missing_identity_with_available_release(self, tmp_path, monkeypatch):
        response = FakeResponse(json.dumps([self._release()]).encode())
        monkeypatch.setattr("skill_release_check.urlopen", lambda *args, **kwargs: response)
        assert SkillReleaseCheck().check(tmp_path/"missing.json")["status"] == "unknown"
        assert not list(tmp_path.iterdir())

    @pytest.mark.parametrize(
        "raw", (b"bad-json", b'{"message":"rate limited"}', b"[null]", b"x"*1_000_001),
        ids=("invalid-json", "api-error", "null-release", "oversized-response"),
    )
    def test_invalid_response_does_not_block_intake(self, tmp_path, monkeypatch, raw):
        monkeypatch.setattr("skill_release_check.urlopen", lambda *args, **kwargs: FakeResponse(raw))
        assert SkillReleaseCheck().check(tmp_path/"missing.json")["status"] == "unavailable"

    @pytest.mark.parametrize("tag", ("v1.02.0", "v1.0.0-alpha.01", "latest", "", "v1.0"))
    def test_invalid_version_rejected(self, tag):
        with pytest.raises(ValueError):
            SkillReleaseVersion.parse(tag)


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, maximum):
        return self.data[:maximum]
