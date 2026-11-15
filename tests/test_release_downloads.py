"""Scope: Verify download counts exclude other assets and include every release page."""

import io
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from release_downloads import ReleaseDownloads


class TestReleaseDownloads:
    def test_counts_zip_assets_without_treating_downloads_as_users(self, monkeypatch):
        release = {"tag_name": "v0.1.0", "assets": [
            {"name": "skill.zip", "download_count": 5},
            {"name": "SHA256SUMS", "download_count": 2}]}
        monkeypatch.setattr("release_downloads.urlopen", lambda *args, **kwargs:
                            io.StringIO(json.dumps([release])))
        result = ReleaseDownloads("example/furniture").read()
        assert result["total_downloads"] == 5
        assert result["releases"][0]["assets"] == [{"name": "skill.zip", "downloads": 5}]
        assert "not unique users" in result["metric"]

    def test_reads_the_next_page_without_credentials_or_request_body(self, monkeypatch):
        requests = []
        release = {"tag_name": "v0.1.0", "assets": [{"name": "skill.zip", "download_count": 1}]}

        # A small callback models the external API boundary without making network requests.
        def respond(request, timeout):
            requests.append(request)
            assert request.get_method() == "GET"
            assert request.data is None
            assert not request.has_header("Authorization")
            return io.StringIO(json.dumps([release] * 100 if len(requests) == 1 else [release]))

        monkeypatch.setattr("release_downloads.urlopen", respond)
        result = ReleaseDownloads("example/furniture").read()
        assert result["total_downloads"] == 101
        assert requests[1].full_url.endswith("page=2")
