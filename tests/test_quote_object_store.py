"""Scope: Verify conditional writes and recovery after an ambiguous upload result."""

import hashlib
import json
import subprocess
from unittest.mock import patch

import pytest

from quote_object_store import QuoteObjectStore, QuoteDeliveryError


class TestQuoteObjectStore:
    def test_conditional_upload_uses_checksum_and_no_public_acl(self):
        with patch("quote_object_store.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "{}", "")
            QuoteObjectStore("bucket", "eu-north-1", "default").put("source-repository.zip", b"source", "application/zip")
            command = run.call_args.args[0]
        assert command[command.index("--if-none-match") + 1] == "*"
        assert command[command.index("--checksum-algorithm") + 1] == "SHA256"
        assert "--acl" not in command

    def test_existing_identical_content_is_successful_retry(self):
        metadata = {"Metadata": {"sha256": hashlib.sha256(b"source").hexdigest()}, "ContentLength": 6}
        with patch("quote_object_store.subprocess.run") as run:
            run.side_effect = [subprocess.CompletedProcess([], 254, "", "PreconditionFailed"),
                               subprocess.CompletedProcess([], 0, json.dumps(metadata), "")]
            QuoteObjectStore("bucket", "eu-north-1", "default").put("key", b"source", "application/zip")

    def test_existing_different_object_is_never_overwritten(self):
        with patch("quote_object_store.subprocess.run") as run:
            run.side_effect = [subprocess.CompletedProcess([], 254, "", "PreconditionFailed"),
                               subprocess.CompletedProcess([], 0, '{"Metadata":{},"ContentLength":6}', "")]
            with pytest.raises(QuoteDeliveryError):
                QuoteObjectStore("bucket", "eu-north-1", "default").put("key", b"source", "application/zip")
            assert run.call_count == 2
