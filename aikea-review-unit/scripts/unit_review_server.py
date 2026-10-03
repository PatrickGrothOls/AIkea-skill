"""Scope: Own the loopback viewer lifecycle and bind its immutable session."""

from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Type
import webbrowser

from review_file_resolver import ReviewFileResolver
from quote_review_request_handler import QuoteReviewRequestHandler
from quote_delivery_session import QuoteDeliverySession
from review_server_session import ReviewServerSession


class UnitReviewServer:
    """Own the short-lived loopback server used for one visual decision."""

    def __init__(
        self,
        viewer_root: Path,
        model_path: Path,
        port: int = 0,
        review_data_path: Path | None = None,
        inspection_model_path: Path | None = None,
    ) -> None:
        resolver = ReviewFileResolver(viewer_root)
        session = ReviewServerSession(model_path, review_data_path, inspection_model_path)
        delivery = QuoteDeliverySession.from_environment(session.artifact.sha256)
        handler: Type[QuoteReviewRequestHandler] = type(
            "BoundReviewRequestHandler",
            (QuoteReviewRequestHandler,),
            {"resolver": resolver, "session": session, "origin": "", "delivery": delivery},
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
        handler.origin = f"http://127.0.0.1:{self.httpd.server_port}"

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.httpd.server_port}/"

    def open_browser(self) -> None:
        webbrowser.open(self.url)

    def serve(self) -> None:
        self.httpd.serve_forever()

    def close(self) -> None:
        self.httpd.server_close()


__all__ = ["UnitReviewServer"]
