"""Scope: Validate the browser's bounded CNC preferences and PNG preview."""

import base64
import binascii

from quote_preferences import QuotePreferences


class QuoteRequestPayload:
    def __init__(self, body: dict) -> None:
        self.preferences = QuotePreferences(body).values
        preview = body.get("preview", "")
        if not isinstance(preview, str) or not preview.startswith("data:image/png;base64,"):
            raise ValueError("A current design preview is required.")
        try:
            self.preview = base64.b64decode(preview.partition(",")[2], validate=True)
        except binascii.Error as error:
            raise ValueError("Invalid design preview.") from error
        if len(self.preview) > 4_000_000 or not self.preview.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Invalid or oversized design preview.")
