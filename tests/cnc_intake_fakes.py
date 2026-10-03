"""Scope: Emulate atomic S3 operations and verified identity for intake tests."""

import io

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


class IntakeS3:
    def __init__(self):
        self.objects, self.writes = {}, []
        self.fail_key = None
        self.signer = boto3.client("s3", region_name="eu-north-1", aws_access_key_id="testing",
                                   aws_secret_access_key="testing", config=Config(signature_version="s3v4"))

    def put_object(self, Bucket, Key, Body, **kwargs):
        if Key == self.fail_key:
            raise ClientError({"Error": {"Code": "ServiceUnavailable"}}, "PutObject")
        if (Bucket, Key) in self.objects and kwargs.get("IfNoneMatch") == "*":
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        self.objects[Bucket, Key] = Body
        self.writes.append(Key)

    def get_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        data = self.objects[Bucket, Key]
        return {"Body": io.BytesIO(data), "ContentLength": len(data)}

    def generate_presigned_post(self, **kwargs):
        return self.signer.generate_presigned_post(**kwargs)

    def list_objects_v2(self, Bucket, Prefix, MaxKeys):
        return {"Contents": [{"Key": key} for bucket, key in sorted(self.objects)
                             if bucket == Bucket and key.startswith(Prefix)][:MaxKeys]}


class IntakeDirectory:
    def __init__(self):
        self.enabled = True

    def admin_get_user(self, **kwargs):
        return {"Enabled": self.enabled, "UserAttributes": [{"Name": "email", "Value": "test@example.invalid"},
                                                            {"Name": "email_verified", "Value": "true"}]}
