"""Scope: Add host- and token-protected CNC delivery routes to the local viewer."""

import json

from quote_object_store import QuoteDeliveryError
from review_request_handler import ReviewRequestHandler


class QuoteReviewRequestHandler(ReviewRequestHandler):
    delivery = None

    def do_GET(self) -> None:
        if self._decoded_path() != "/api/cnc-request":
            return super().do_GET()
        if self.headers.get("Host") != self.origin.removeprefix("http://"):
            self._send_json(403, {"error": "Invalid viewer host."})
            return
        status = self.delivery.status() if self.delivery else {"enabled": False}
        self._send_json(200, status)

    def do_POST(self) -> None:
        if self._decoded_path() != "/api/cnc-request":
            return super().do_POST()
        if not self.delivery:
            self._send_json(503, {"error": "CNC delivery is not configured on this viewer."})
            return
        if (self.headers.get("Host") != self.origin.removeprefix("http://")
                or self.headers.get("Origin") != self.origin):
            self._send_json(403, {"error": "Invalid quote request origin."})
            return
        if self.headers.get("Content-Type", "").partition(";")[0].lower() != "application/json":
            self._send_json(415, {"error": "Quote requests must be JSON."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 5_500_000:
                raise ValueError("Invalid quote request size.")
            body = json.loads(self.rfile.read(length))
            response = self.delivery.submit(body, self.headers.get("X-AIkea-Quote-Token"))
        except PermissionError as error:
            self._send_json(403, {"error": str(error)})
            return
        except (ValueError, UnicodeDecodeError) as error:
            self._send_json(400, {"error": str(error)})
            return
        except QuoteDeliveryError as error:
            self._send_json(502, {"error": str(error)})
            return
        self._send_json(200, response)
