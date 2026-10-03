"""Scope: Prove upload completion, immutable retries and quote capability checks."""

import base64
import io
import json
from unittest.mock import Mock
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile

import pytest

from quote_delivery_session import QuoteDeliverySession
from quote_object_store import QuoteDeliveryError


class MemoryQuoteStore:
    def __init__(self):
        self.objects = {}
        self.calls = []
        self.fail_on = None

    def put(self, key, content, content_type):
        self.calls.append(key)
        if key.endswith(self.fail_on or "never-fail"):
            raise QuoteDeliveryError("Synthetic upload failure")
        if key in self.objects:
            assert self.objects[key] == content
        self.objects[key] = content


class TestQuoteDelivery:
    def setup_method(self):
        output = io.BytesIO()
        with ZipFile(output, "w") as archive:
            archive.writestr("source-manifest.json", "{}")
            archive.writestr("repository/assemblies/test/builder.py", "WIDTH=600")
        self.store = MemoryQuoteStore()
        self.delivery = QuoteDeliverySession(output.getvalue(), "a" * 64, self.store)
        self.body = {"selected": {"machining": True, "painting": True, "installation": True},
                     "title": "Synthetic wardrobe", "finish": "discuss", "colour": "", "postcode": "", "timing": "flexible",
                     "notes": "Test request", "preview": "data:image/png;base64," + base64.b64encode(b"\x89PNG\r\n\x1a\n").decode()}

    def test_completed_source_only_package_triggers_once_on_retry(self):
        receipt = self.delivery.submit(self.body, self.delivery.token)
        assert self.store.calls[-1].endswith("/ready.json")
        assert len(self.store.calls) == 4
        assert receipt["services_sent"] == ["machining"]
        assert receipt["notification"] == "pending"
        assert self.delivery.submit(self.body, self.delivery.token) == receipt
        assert len(self.store.calls) == 4
        assert not any(key.endswith(".step") for key in self.store.objects)

    def test_failure_never_creates_ready_and_retry_uses_same_id(self):
        self.store.fail_on = "/request.json"
        with pytest.raises(QuoteDeliveryError):
            self.delivery.submit(self.body, self.delivery.token)
        assert not any(key.endswith("/ready.json") for key in self.store.objects)
        self.store.fail_on = None
        receipt = self.delivery.submit(self.body, self.delivery.token)
        assert receipt["request_id"] == self.delivery.request_id

    def test_concurrent_double_clicks_are_one_submission(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            receipts = list(pool.map(lambda _: self.delivery.submit(self.body, self.delivery.token), range(2)))
        assert receipts[0] == receipts[1]
        assert len(self.store.calls) == 4

    def test_token_and_cnc_selection_are_required_before_upload(self):
        with pytest.raises(PermissionError):
            self.delivery.submit(self.body, "wrong")
        self.body["selected"]["machining"] = False
        with pytest.raises(ValueError):
            self.delivery.submit(self.body, self.delivery.token)
        assert not self.store.calls

    def test_changed_retry_cannot_replace_an_existing_request(self):
        self.delivery.submit(self.body, self.delivery.token)
        self.body["notes"] = "different"
        with pytest.raises(ValueError, match="started"):
            self.delivery.submit(self.body, self.delivery.token)

    def test_step_archive_is_rejected(self):
        output = io.BytesIO()
        with ZipFile(output, "w") as archive:
            archive.writestr("source-manifest.json", "{}")
            archive.writestr("part.STEP", "export")
        with pytest.raises(ValueError, match="not STEP"):
            QuoteDeliverySession(output.getvalue(), "a" * 64, self.store)

    def test_environment_requires_explicit_trusted_host_target(self, monkeypatch, tmp_path):
        monkeypatch.setenv("AIKEA_CNC_SOURCE_REPO", str(tmp_path))
        (tmp_path / "design").mkdir()
        monkeypatch.setenv("AIKEA_CNC_PROJECT_PATH", "design")
        monkeypatch.delenv("AIKEA_CNC_GATEWAY_CONFIG", raising=False)
        monkeypatch.delenv("AIKEA_CNC_DEPLOYMENT_CONFIG", raising=False)
        monkeypatch.setattr("quote_delivery_session.QuoteSourceRepository.build", Mock(return_value=self.delivery.package))
        store = Mock(return_value=self.store)
        monkeypatch.setattr("quote_delivery_session.QuoteObjectStore", store)
        with pytest.raises(ValueError, match="AIKEA_CNC_DEPLOYMENT_CONFIG"):
            QuoteDeliverySession.from_environment("a" * 64)
        store.assert_not_called()
        config = tmp_path / "target.json"
        config.write_text(json.dumps({"AccountId": "222222222222", "Region": "eu-west-1",
                                     "AcceptedBucket": "test-private-cnc-bucket"}))
        monkeypatch.setenv("AIKEA_CNC_DEPLOYMENT_CONFIG", str(config))
        monkeypatch.setenv("AIKEA_CNC_AWS_PROFILE", "test-profile")
        delivery = QuoteDeliverySession.from_environment("a" * 64)
        assert delivery.store is self.store
        store.assert_called_once_with("test-private-cnc-bucket", "eu-west-1", "test-profile")
