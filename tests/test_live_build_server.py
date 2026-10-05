"""Scope: Verify the draft transport cannot expose source, decisions or upload routes."""

from http.client import HTTPConnection
import json

from live_build_server import LiveBuildServer
from live_build_store import LiveBuildStore


class TestLiveBuildServer:
    def request(self, server, path, method="GET", headers=None):
        connection = HTTPConnection("127.0.0.1", server.http.server_port)
        connection.request(method, path, headers=headers or {})
        response = connection.getresponse()
        result = response.status, response.read()
        connection.close()
        return result

    def test_read_only_bounded_routes_and_local_host(self, tmp_path):
        ui = tmp_path / "ui"
        ui.mkdir()
        (ui / "index.html").write_text("live viewer")
        (tmp_path / "private.py").write_text("private source")
        store = LiveBuildStore(tmp_path / "live")
        store.status("waiting")
        server = LiveBuildServer(ui, store.directory)
        server.start()
        try:
            assert self.request(server, "/")[1] == b"live viewer"
            status, content = self.request(server, "/live-build.json")
            assert status == 200 and json.loads(content)["fabrication_ready"] is False
            for path in ("/../private.py", "/%252e%252e/private.py", "/review-data.json", "/parts/../private.py"):
                assert self.request(server, path)[0] == 404
            assert self.request(server, "/api/review-decision", "POST")[0] == 405
            assert self.request(server, "/live-build.json", headers={"Host": "attacker.example"})[0] == 403
        finally:
            server.close()
