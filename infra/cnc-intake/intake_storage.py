"""Scope: Read bounded quarantine objects and write immutable server-owned records."""

import hashlib
import json

from botocore.exceptions import ClientError


class IntakeStorage:
    def __init__(self, s3, quarantine, accepted):
        self.s3, self.quarantine, self.accepted = s3, quarantine, accepted

    def read(self, bucket, key, limit):
        # Exact-prefix listing distinguishes missing objects without granting bucket-wide listing.
        listed = self.s3.list_objects_v2(Bucket=bucket, Prefix=key, MaxKeys=1)
        if not any(item["Key"] == key for item in listed.get("Contents", [])):
            return None
        try:
            result = self.s3.get_object(Bucket=bucket, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] in {"NoSuchKey", "404"}:
                return None
            raise
        with result["Body"] as stream:
            if result["ContentLength"] > limit:
                raise ValueError("Stored object exceeds limit.")
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise ValueError("Stored object exceeds limit.")
        return data

    def record(self, key):
        data = self.read(self.quarantine, key, 16_384)
        return json.loads(data) if data is not None else None

    def create(self, bucket, key, data, content_type="application/json"):
        try:
            self.s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type,
                               Metadata={"sha256": hashlib.sha256(data).hexdigest()}, IfNoneMatch="*")
            return True
        except ClientError as error:
            if error.response["Error"]["Code"] == "PreconditionFailed":
                return False
            raise

    def immutable(self, bucket, key, data, content_type="application/json"):
        if not self.create(bucket, key, data, content_type):
            if self.read(bucket, key, len(data)) != data:
                raise ValueError("Conflicting immutable request content.")

    def json(self, value):
        return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
