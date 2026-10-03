"""Scope: Preserve preference acceptance and normalization across both request transports."""

import base64
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-intake"))
from intake_contract import IntakeContract
from quote_request_payload import QuoteRequestPayload


class TestQuotePreferences:
    def preferences(self):
        return {"selected": {"machining": True, "painting": False, "installation": True},
                "title": "  Wardrobe  ", "finish": "discuss", "timing": "flexible", "notes": "  Hall  "}

    def local(self, preferences):
        preview = "data:image/png;base64," + base64.b64encode(b"\x89PNG\r\n\x1a\n").decode()
        return QuoteRequestPayload({**preferences, "preview": preview}).preferences

    def hosted(self, preferences):
        body = {"request_id": "12345678-1234-4234-8234-123456789012", "model_sha256": "b" * 64,
                "preferences": preferences, "files": {
                    name: {"size": 100, "sha256": "a" * 64} for name in IntakeContract.FILES}}
        return IntakeContract().validate(body)["preferences"]

    def test_same_preferences_without_hosted_inline_preview(self):
        preferences = self.preferences()
        assert self.local(preferences) == self.hosted(preferences)
        assert self.hosted(preferences)["title"] == "Wardrobe"
        assert self.hosted(preferences)["notes"] == "Hall"
        assert self.hosted(preferences)["postcode"] == ""

    @pytest.mark.parametrize("field,value", [
        ("finish", "unknown"), ("timing", "tomorrow"), ("notes", "x" * 2001),
        ("title", 123), ("selected", {"machining": False, "painting": True, "installation": True}),
        ("selected", {"machining": 1, "painting": False, "installation": True}),
    ])
    def test_both_transports_reject_invalid_preferences(self, field, value):
        preferences = {**self.preferences(), field: value}
        for validate in (self.local, self.hosted):
            with pytest.raises(ValueError):
                validate(preferences)

    def test_local_transport_still_requires_real_preview_representation(self):
        with pytest.raises(ValueError, match="preview"):
            QuoteRequestPayload(self.preferences())
