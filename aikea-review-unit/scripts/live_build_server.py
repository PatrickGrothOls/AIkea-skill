"""Scope: Serve only bundled UI and disposable live assets on the loopback interface."""

from http.server import ThreadingHTTPServer
import re
from threading import Thread

from review_file_resolver import ReviewFileResolver
from review_request_handler import ReviewRequestHandler


class LiveBuildRequestHandler(ReviewRequestHandler):
    """Read-only draft transport; no project browsing, approvals or uploads."""

    def do_GET(self):
        if self.headers.get("Host") != self.server.server_name_header:
            self.send_error(403)
            return
        path = self._decoded_path()
        if path == "/live-build.json":
            target = self.directory / "revision.json"
            content_type = "application/json"
        elif re.fullmatch(r"/parts/[a-f0-9]{64}\.glb", path):
            target = self.directory / path.rsplit("/", 1)[-1]
            content_type = "model/gltf-binary"
        else:
            target = self.resolver.resolve(path)
            import mimetypes
            content_type = mimetypes.guess_type(path)[0] or "text/html"
        if target is None or not target.is_file():
            self.send_error(404)
            return
        self._send_bytes(200, target.read_bytes(), content_type, no_store=True)

    def do_POST(self):
        self.send_error(405)


class LiveBuildServer:
    def __init__(self, viewer_root, directory, port=0):
        handler = type("BoundLiveBuildHandler", (LiveBuildRequestHandler,), {
            "directory": directory, "resolver": ReviewFileResolver(viewer_root),
        })
        self.http = ThreadingHTTPServer(("127.0.0.1", port), handler)
        self.http.server_name_header = f"127.0.0.1:{self.http.server_port}"
        self.url = f"http://{self.http.server_name_header}/?live=1"

    def start(self):
        self.thread = Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
