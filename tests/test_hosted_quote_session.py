"""Scope: Exercise the customer client through real gateway logic with synthetic network transport."""

import base64
from email.parser import BytesParser
from email.policy import default
import hashlib
import io
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-intake"))
from gateway import IntakeGateway
from intake_storage import IntakeStorage
from hosted_quote_session import HostedQuoteSession
from quote_object_store import QuoteDeliveryError
from cnc_intake_fakes import IntakeS3, IntakeDirectory
from test_cnc_package_validation import TestPackageValidation as PackageFixture, TestPreviewValidation as PreviewFixture


class FakeLogin:
    def __init__(self):
        self.calls = 0

    def authenticate(self):
        self.calls += 1
        return "synthetic-token"


class GatewayTransport:
    def __init__(self):
        self.s3 = IntakeS3()
        self.gateway = IntakeGateway(IntakeStorage(self.s3, "aikea-cnc-intake-123456789012-eu-north-1", "accepted"), IntakeDirectory(), "pool")
        self.uploads, self.fail_completion, self.reject_token = 0, False, False

    def json(self, url, body, token):
        if self.reject_token:
            self.reject_token = False
            raise HTTPError(url, 401, "Expired", {}, io.BytesIO())
        complete = url.endswith("/complete")
        if complete and self.fail_completion:
            self.fail_completion = False
            raise URLError("Synthetic lost connection")
        event = {"routeKey": "POST /requests/{request_id}/complete" if complete else "POST /requests",
                 "body": json.dumps(body), "pathParameters": {"request_id": url.split("/")[-2]},
                 "requestContext": {"authorizer": {"jwt": {"claims": {
                     "sub": "customer", "username": "customer", "token_use": "access"}}}}}
        result = self.gateway.handle(event)
        if result["statusCode"] != 200:
            raise HTTPError(url, result["statusCode"], "Rejected", {}, io.BytesIO(result["body"].encode()))
        return json.loads(result["body"])

    def post(self, url, data, headers):
        message = BytesParser(policy=default).parsebytes(("Content-Type: " + headers["Content-Type"] + "\r\n\r\n").encode() + data)
        fields = {part.get_param("name", header="content-disposition"): part.get_payload(decode=True) for part in message.iter_parts()}
        assert base64.b64encode(hashlib.sha256(fields["file"]).digest()) == fields["x-amz-checksum-sha256"]
        self.s3.objects["aikea-cnc-intake-123456789012-eu-north-1", fields["key"].decode()] = fields["file"]
        self.uploads += 1
        return b""


class TestHostedQuoteSession:
    def setup_method(self):
        self.transport, self.login = GatewayTransport(), FakeLogin()
        self.config = {"AccountId": "123456789012", "Region": "eu-north-1",
                       "QuarantineBucket": "aikea-cnc-intake-123456789012-eu-north-1",
                       "GatewayUrl": "https://test.execute-api.eu-north-1.amazonaws.com",
                       "LoginUrl": "https://aikea-cnc-123456789012.auth.eu-north-1.amazoncognito.com", "ClientId": "testclient"}
        self.session = HostedQuoteSession(PackageFixture().archive(), "b" * 64, self.config, self.transport, self.login)
        self.body = {"title": "Synthetic test", "finish": "discuss", "timing": "flexible",
                     "selected": {"machining": True, "painting": False, "installation": False},
                     "preview": "data:image/png;base64," + base64.b64encode(PreviewFixture().png()).decode()}

    def test_customer_send_signs_in_and_publishes_source_with_docs(self):
        receipt = self.session.submit(self.body, self.session.token)
        assert receipt["status"] == "submitted"
        assert self.transport.uploads == 2 and self.login.calls == 1
        assert self.session.submit(self.body, self.session.token) == receipt
        assert self.transport.uploads == 2
        assert self.session.status()["sign_in_required"]

    def test_failed_completion_retries_without_reupload_or_new_reservation(self):
        self.transport.fail_completion = True
        with pytest.raises(QuoteDeliveryError, match="connection"):
            self.session.submit(self.body, self.session.token)
        assert self.session.receipt is None
        assert self.session.submit(self.body, self.session.token)["status"] == "submitted"
        assert self.transport.uploads == 2

    def test_expired_access_token_reauthenticates_once(self):
        self.transport.reject_token = True
        assert self.session.submit(self.body, self.session.token)["status"] == "submitted"
        assert self.login.calls == 2

    def test_unexpected_upload_host_never_receives_source(self):
        with pytest.raises(ValueError, match="destination"):
            self.session._upload({"url": "https://attacker.invalid/", "fields": {}}, "source.zip", b"source")
        assert self.transport.uploads == 0

    def test_bad_viewer_token_never_opens_login(self):
        with pytest.raises(PermissionError):
            self.session.submit(self.body, "wrong")
        assert self.login.calls == 0
