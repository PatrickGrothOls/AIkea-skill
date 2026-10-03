"""Scope: Verify the local quote route rejects foreign origins and missing capabilities."""

from http.server import ThreadingHTTPServer
import json
from threading import Thread
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from quote_review_request_handler import QuoteReviewRequestHandler
from test_quote_delivery import TestQuoteDelivery as QuoteDeliveryFixture


class TestQuoteHttp:
    def setup_method(self):
        self.fixture = QuoteDeliveryFixture()
        self.fixture.setup_method()
        handler = type("QuoteTestHandler", (QuoteReviewRequestHandler,),
                       {"delivery": self.fixture.delivery, "origin": ""})
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        handler.origin = self.origin
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, body=None, **headers):
        encoded = json.dumps(body).encode() if body is not None else None
        request = Request(self.origin + "/api/cnc-request", data=encoded, headers=headers)
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            return error.code, json.load(error)

    def headers(self):
        return {"Origin": self.origin, "Content-Type": "application/json",
                "X-AIkea-Quote-Token": self.fixture.delivery.token}

    def test_real_http_submission_and_duplicate_retry(self):
        status, available = self.request()
        assert status == 200 and available["token"] == self.fixture.delivery.token
        status, receipt = self.request(self.fixture.body, **self.headers())
        assert status == 200 and receipt["status"] == "submitted"
        assert self.request(self.fixture.body, **self.headers()) == (status, receipt)
        assert len(self.fixture.store.calls) == 4

    def test_cross_origin_and_wrong_host_cannot_send_or_read_token(self):
        headers = self.headers() | {"Origin": "https://unrelated.invalid"}
        assert self.request(self.fixture.body, **headers)[0] == 403
        assert self.request(Host="unrelated.invalid")[0] == 403
        assert not self.fixture.store.calls

    def test_token_is_required_even_on_same_origin(self):
        headers = self.headers() | {"X-AIkea-Quote-Token": "incorrect"}
        assert self.request(self.fixture.body, **headers)[0] == 403
        assert not self.fixture.store.calls

    def test_delivery_failure_is_not_reported_as_success(self):
        self.fixture.store.fail_on = "/source-repository.zip"
        assert self.request(self.fixture.body, **self.headers())[0] == 502
        assert not self.fixture.delivery.receipt

    def test_viewer_html_and_api_responses_block_cross_site_framing(self, tmp_path):
        from review_file_resolver import ReviewFileResolver

        class StaticSession:
            # Synthetic session keeps this HTTP test independent of CAD generation.
            def display_artifact(self, _path):
                return None

        (tmp_path / "index.html").write_text("<!doctype html><title>Quote test</title>")
        self.server.RequestHandlerClass.resolver = ReviewFileResolver(tmp_path)
        self.server.RequestHandlerClass.session = StaticSession()
        for path in ("/", "/api/cnc-request"):
            with urlopen(self.origin + path, timeout=3) as response:
                assert response.status == 200
                assert response.headers["Content-Security-Policy"] == "frame-ancestors 'self'"
                assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
