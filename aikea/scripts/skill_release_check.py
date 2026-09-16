"""Scope: Read public release metadata and report availability without downloading or executing code."""

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from skill_release_version import SkillReleaseVersion


class SkillReleaseCheck:
    REPOSITORY = "PatrickGrothOls/AIkea-skill"
    API_URL = f"https://api.github.com/repos/{REPOSITORY}/releases?per_page=100"
    RELEASES_URL = f"https://github.com/{REPOSITORY}/releases"

    def check(self, metadata_path):
        # File/network/JSON errors are handled once at this external read boundary.
        try:
            installed = json.loads(Path(metadata_path).read_text()) if Path(metadata_path).exists() else {}
            request = Request(self.API_URL, headers={"Accept": "application/vnd.github+json", "User-Agent": "AIkea-version-check"})
            with urlopen(request, timeout=8) as response:
                raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                raise ValueError("release metadata exceeds the supported response size")
            return self.compare(installed, json.loads(raw))
        except (OSError, URLError, ValueError, TypeError, KeyError) as error:
            return {"status": "unavailable", "reason": str(error), "releases_url": self.RELEASES_URL,
                    "action": "Continue with the installed package; do not claim it is current."}

    def compare(self, installed, releases):
        if not isinstance(installed, dict) or not isinstance(releases, list):
            raise ValueError("unexpected package or release metadata")
        candidates = []
        for release in releases:
            if not isinstance(release, dict):
                raise ValueError("unexpected release entry")
            if release.get("draft") or not release.get("published_at"):
                continue
            tag = release["tag_name"]
            # Other tags may be vendor snapshots, not versions of the skill.
            try:
                version = SkillReleaseVersion.parse(tag)
            except ValueError:
                continue
            prefix = f"https://github.com/{self.REPOSITORY}/releases/download/{tag}/"
            assets = {asset["name"]: asset["browser_download_url"] for asset in release["assets"]}
            if any(assets.get(name) != prefix+name for name in ("aikea-skill.zip", "SHA256SUMS")):
                continue
            candidates.append((version, tag, assets))
        if not candidates:
            return {"status": "unavailable", "reason": "No complete supported release was found.",
                    "releases_url": self.RELEASES_URL}
        newest, tag, assets = max(candidates, key=lambda item: item[0])
        result = {"installed_version": installed.get("version"), "available_version": tag,
                  "release_url": f"{self.RELEASES_URL}/tag/{tag}",
                  "download_url": assets["aikea-skill.zip"], "checksums_url": assets["SHA256SUMS"]}
        distribution = installed.get("distribution")
        if distribution == "development":
            return dict(result, status="development", action="Keep this development checkout; do not offer a release as an upgrade.")
        if (distribution != "release" or installed.get("repository") != self.REPOSITORY
                or not isinstance(installed.get("version"), str)):
            return dict(result, status="unknown", action="Installed release identity is unknown; do not claim an update or current status.")
        current = SkillReleaseVersion.parse(installed["version"])
        status = "update_available" if newest > current else "current" if newest == current else "ahead"
        return dict(result, status=status)
