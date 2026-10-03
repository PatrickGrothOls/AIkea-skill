"""Scope: Upload immutable quote objects through the host's AWS CLI identity."""

import hashlib
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


class QuoteDeliveryError(RuntimeError):
    """A bounded AWS operation failed; the request must remain retryable."""


class QuoteObjectStore:
    def __init__(self, bucket: str, region: str, profile: str) -> None:
        self.bucket, self.region, self.profile = bucket, region, profile

    def put(self, key: str, content: bytes, content_type: str) -> None:
        digest = hashlib.sha256(content).hexdigest()
        with TemporaryDirectory(prefix="aikea-quote-") as directory:
            path = Path(directory) / "object"
            path.write_bytes(content)
            result = self._run([
                "put-object", "--bucket", self.bucket, "--key", key,
                "--body", str(path), "--content-type", content_type,
                "--metadata", json.dumps({"sha256": digest}),
                "--checksum-algorithm", "SHA256", "--if-none-match", "*",
            ])
        if result.returncode == 0:
            return
        # A timed-out PUT may already have succeeded; confirm identical bytes on retry.
        if "PreconditionFailed" in result.stderr:
            existing = self._run(["head-object", "--bucket", self.bucket, "--key", key])
            if existing.returncode == 0:
                metadata = json.loads(existing.stdout)
                if metadata.get("Metadata", {}).get("sha256") == digest and metadata["ContentLength"] == len(content):
                    return
        raise QuoteDeliveryError("The CNC request could not be uploaded. Check the host's AWS access and retry.")

    def _run(self, arguments: list[str]) -> subprocess.CompletedProcess:
        command = ["aws", "s3api", *arguments, "--region", self.region,
                   "--profile", self.profile, "--output", "json", "--no-cli-pager"]
        try:
            return subprocess.run(command, capture_output=True, text=True, timeout=90)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise QuoteDeliveryError("AWS upload is unavailable or timed out. Retry this request.") from error
