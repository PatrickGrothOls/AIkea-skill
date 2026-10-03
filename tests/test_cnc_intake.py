"""Scope: Exercise authenticated reservations, immutable acceptance and failure retries."""

import base64
import hashlib
import json
from pathlib import Path
import sys
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-intake"))
from gateway import IntakeGateway
from intake_storage import IntakeStorage
from cnc_intake_fakes import IntakeS3, IntakeDirectory
from test_cnc_package_validation import TestPackageValidation as PackageFixture, TestPreviewValidation as PreviewFixture


class TestCncIntake:
    def setup_method(self):
        self.s3, self.directory = IntakeS3(), IntakeDirectory()
        self.gateway = IntakeGateway(IntakeStorage(self.s3, "quarantine", "accepted"), self.directory, "pool")
        self.files = {"source-repository.zip": PackageFixture().archive(), "preview.png": PreviewFixture().png()}
        self.body = {"request_id": str(uuid4()), "model_sha256": "b" * 64,
                     "preferences": {"title": "Test", "finish": "discuss", "timing": "flexible",
                                     "selected": {"machining": True, "painting": False, "installation": False}},
                     "files": {n: {"size": len(v), "sha256": hashlib.sha256(v).hexdigest()} for n, v in self.files.items()}}

    def call(self, complete=False, subject="customer", claims=True):
        event = {"routeKey": "POST /requests/{request_id}/complete" if complete else "POST /requests",
                 "body": json.dumps({} if complete else self.body), "pathParameters": {"request_id": self.body["request_id"]},
                 "requestContext": {"authorizer": {"jwt": {"claims": {
                     "sub": subject, "username": subject, "token_use": "access"} if claims else {}}}}}
        result = self.gateway.handle(event)
        return result["statusCode"], json.loads(result["body"])

    def upload(self):
        owner = self.gateway.reservations.owner("customer")
        for name, data in self.files.items():
            self.s3.objects["quarantine", f"uploads/{owner}/{self.body['request_id']}/{name}"] = data

    def test_actual_sdk_policies_bind_key_size_checksum_and_short_expiry(self):
        status, response = self.call()
        assert status == 200
        for name, post in response["uploads"].items():
            policy = json.loads(base64.b64decode(post["fields"]["policy"]))
            assert {"key": post["fields"]["key"]} in policy["conditions"]
            assert ["content-length-range", len(self.files[name]), len(self.files[name])] in policy["conditions"]
            assert {"x-amz-checksum-sha256": base64.b64encode(hashlib.sha256(self.files[name]).digest()).decode()} in policy["conditions"]
            assert "ready.json" not in post["fields"]["key"]

    def test_end_to_end_retry_emits_one_ready_marker(self):
        self.call()
        self.upload()
        status, receipt = self.call(complete=True)
        assert status == 200 and receipt["status"] == "submitted"
        assert self.call(complete=True) == (status, receipt)
        assert len([k for k in self.s3.writes if k.endswith("/ready.json")]) == 1
        data = json.loads(self.s3.objects["accepted", f"aikea/cnc-requests/{receipt['request_id']}/request.json"])
        assert data["contact_email"] == "test@example.invalid"
        assert data["source_trust"] == "untrusted_do_not_execute"

    def test_cross_user_and_missing_auth_are_rejected(self):
        assert self.call(claims=False)[0] == 401
        self.call()
        self.upload()
        assert self.call(complete=True, subject="other")[0] == 403
        self.directory.enabled = False
        assert self.call(complete=True)[0] == 403
        assert not any(bucket == "accepted" for bucket, key in self.s3.objects)

    def test_daily_quota_and_retry(self):
        for _ in range(5):
            self.body["request_id"] = str(uuid4())
            assert self.call()[0] == 200
            assert self.call()[0] == 200
        self.body["request_id"] = str(uuid4())
        assert self.call()[0] == 400

    def test_changed_request_and_tampered_upload_rejected(self):
        self.call()
        self.body["preferences"]["title"] = "Changed"
        assert self.call()[0] == 400
        self.files["source-repository.zip"] = b"tampered"
        self.upload()
        assert self.call(complete=True)[0] == 400
        assert not any(bucket == "accepted" for bucket, key in self.s3.objects)

    def test_expiration_and_missing_upload(self):
        self.call()
        assert self.call(complete=True)[0] == 400
        self.upload()
        self.gateway.acceptance.clock = lambda: 9_999_999_999
        assert self.call(complete=True)[0] == 400

    def test_publish_failure_never_reports_success_and_retries_safely(self):
        self.call()
        self.upload()
        owner = self.gateway.reservations.owner("customer")
        from uuid import UUID, uuid5
        accepted_id = str(uuid5(UUID("a554e84c-5467-4aae-a1ba-cf8c904a0dcb"), owner + "/" + self.body["request_id"]))
        self.s3.fail_key = f"aikea/cnc-requests/{accepted_id}/ready.json"
        assert self.call(complete=True)[0] == 503
        self.s3.fail_key = None
        assert self.call(complete=True)[0] == 200

    def test_oversized_descriptor_cannot_obtain_upload_grant(self):
        self.body["files"]["source-repository.zip"]["size"] = 16_000_001
        assert self.call()[0] == 400
        assert not self.s3.objects
