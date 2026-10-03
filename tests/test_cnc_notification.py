"""Scope: Verify notification validation, duplicate handling and preserved bucket hooks."""

import hashlib
import io
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-requests"))
from infrastructure import CncInfrastructure
from notification_worker import CncNotificationWorker

from cnc_deployment_config import CncDeploymentConfig

EXAMPLE_CONFIG = CncDeploymentConfig("123456789012", "eu-north-1", "example-aikea-cnc-requests")


class FakeS3:
    def __init__(self):
        self.objects = {}

    def head_object(self, Bucket, Key):
        content = self.objects[Key]
        return {"ContentLength": len(content), "Metadata": {"sha256": hashlib.sha256(content).hexdigest()}}

    def get_object(self, Bucket, Key):
        return {"ContentLength": len(self.objects[Key]), "Body": io.BytesIO(self.objects[Key])}

    def list_objects_v2(self, Bucket, Prefix, MaxKeys):
        return {"Contents": [{"Key": key} for key in self.objects if key.startswith(Prefix)][:MaxKeys]}

    def put_object(self, Bucket, Key, Body, ContentType):
        self.objects[Key] = Body


class FakeSNS:
    def __init__(self):
        self.messages = []
        self.fail = False

    def publish(self, **message):
        if self.fail:
            raise RuntimeError("SNS unavailable")
        self.messages.append(message)
        return {"MessageId": "synthetic-notification"}


class TestCncNotification:
    def setup_method(self):
        self.s3, self.sns = FakeS3(), FakeSNS()
        self.worker = CncNotificationWorker(self.s3, self.sns, "bucket", "topic", "eu-north-1")
        self.request_id = "a" * 36
        self.prefix = f"aikea/cnc-requests/{self.request_id}/"
        request = {"request_id": self.request_id, "title": "Synthetic design", "postcode": "", "timing": "flexible"}
        files = {"source-repository.zip": b"source", "preview.png": b"png", "request.json": json.dumps(request).encode()}
        manifest = {"schema_version": 1, "request_id": self.request_id, "files": {}}
        for name, data in files.items():
            self.s3.objects[self.prefix + name] = data
            manifest["files"][name] = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        self.s3.objects[self.prefix + "ready.json"] = json.dumps(manifest).encode()
        self.record = {"eventName": "ObjectCreated:Put", "s3": {"bucket": {"name": "bucket"},
                       "object": {"key": self.prefix + "ready.json"}}}

    def test_source_request_email_and_repeat_delivery(self):
        self.worker.notify(self.record)
        self.worker.notify(self.record)
        assert len(self.sns.messages) == 1
        assert "No STEP exports" in self.sns.messages[0]["Message"]
        assert "isolated environment without credentials" in self.sns.messages[0]["Message"]
        assert "AWS sign-in required" in self.sns.messages[0]["Message"]

    def test_incomplete_upload_does_not_notify(self):
        self.s3.objects[self.prefix + "preview.png"] = b"changed"
        with pytest.raises(ValueError, match="Incomplete"):
            self.worker.notify(self.record)
        assert not self.sns.messages

    def test_publish_failure_does_not_mark_as_notified(self):
        self.sns.fail = True
        with pytest.raises(RuntimeError):
            self.worker.notify(self.record)
        assert self.prefix + "notified.json" not in self.s3.objects
        self.sns.fail = False
        self.worker.notify(self.record)
        assert len(self.sns.messages) == 1

    def test_s3_probe_is_ignored(self):
        self.worker.handle({"Records": [{"body": json.dumps({"Event": "s3:TestEvent"})}]})
        assert not self.sns.messages

    def test_hook_merge_retains_existing_destinations(self):
        existing = {"EventBridgeConfiguration": {}, "TopicConfigurations": [{"Id": "unrelated"}],
                    "QueueConfigurations": [{"Id": "another", "QueueArn": "old"}]}
        result = CncInfrastructure(EXAMPLE_CONFIG).notification(existing, "new-queue")
        assert result["TopicConfigurations"] == existing["TopicConfigurations"]
        assert result["EventBridgeConfiguration"] == {}
        assert result["QueueConfigurations"][0]["Id"] == "another"
        assert len(existing["QueueConfigurations"]) == 1
        assert CncInfrastructure(EXAMPLE_CONFIG).notification(result, "new-queue") == result
