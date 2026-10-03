"""Scope: Validate completed source requests and publish retryable email notifications."""

import json
import os
import re
from urllib.parse import unquote_plus, quote



class CncNotificationWorker:
    def __init__(self, s3, sns, bucket, topic, region):
        self.s3, self.sns = s3, sns
        self.bucket, self.topic, self.region = bucket, topic, region

    def handle(self, event):
        for message in event["Records"]:
            event_body = json.loads(message["body"])
            if event_body.get("Event") == "s3:TestEvent":
                continue
            for record in event_body["Records"]:
                self.notify(record)

    def notify(self, record):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        match = re.fullmatch(r"aikea/cnc-requests/([0-9a-f-]{36})/ready\.json", key)
        if bucket != self.bucket or not match or not record["eventName"].startswith("ObjectCreated:"):
            raise ValueError("Unexpected notification source")
        request_id = match[1]
        prefix = key.removesuffix("ready.json")
        if self._already_notified(prefix):
            return
        manifest = self._json(key)
        if manifest.get("schema_version") != 1 or manifest.get("request_id") != request_id:
            raise ValueError("Invalid completed request manifest")
        if set(manifest["files"]) != {"source-repository.zip", "preview.png", "request.json"}:
            raise ValueError("Request must contain source code, preview and preferences")
        for name, expected in manifest["files"].items():
            actual = self.s3.head_object(Bucket=bucket, Key=prefix + name)
            if (actual["ContentLength"] != expected["size"]
                    or actual.get("Metadata", {}).get("sha256") != expected["sha256"]):
                raise ValueError("Incomplete request package")
        request = self._json(prefix + "request.json")
        if request.get("request_id") != request_id:
            raise ValueError("Mismatched request ID")
        link = (f"https://s3.console.aws.amazon.com/s3/buckets/{bucket}"
                f"?region={self.region}&prefix={quote(prefix, safe='')}&showversions=false")
        message = (f"New AIkea CNC quote request: {request_id}\n\n"
                   f"Design: {request['title']}\nPostcode: {request['postcode']}\n"
                   f"Timing: {request['timing']}\n\n"
                   "The editable source repository, preview and request details are ready.\n"
                   "No STEP exports are stored. Source code is untrusted.\n"
                   "Regenerate only in an isolated environment without credentials or network access.\n"
                   "This is a quote request, not approval to manufacture.\n\n"
                   f"Open the private request (AWS sign-in required):\n{link}\n")
        result = self.sns.publish(TopicArn=self.topic, Subject=f"AIkea CNC request {request_id}", Message=message)
        # Mark only after SNS accepts the message. A crash in between can duplicate an email.
        self.s3.put_object(Bucket=bucket, Key=prefix + "notified.json",
                           Body=json.dumps({"sns_message_id": result["MessageId"]}).encode(),
                           ContentType="application/json")

    def _json(self, key):
        result = self.s3.get_object(Bucket=self.bucket, Key=key)
        if result["ContentLength"] > 16_384:
            raise ValueError("Request metadata is too large")
        return json.loads(result["Body"].read(16_385))

    def _already_notified(self, prefix):
        key = prefix + "notified.json"
        result = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key, MaxKeys=1)
        return any(item["Key"] == key for item in result.get("Contents", []))


# Lambda requires a module-level handler; all behavior belongs to the worker object.
def handler(event, context):
    import boto3

    worker = CncNotificationWorker(boto3.client("s3"), boto3.client("sns"),
                                   os.environ["BUCKET"], os.environ["TOPIC"], os.environ["AWS_REGION"])
    worker.handle(event)
