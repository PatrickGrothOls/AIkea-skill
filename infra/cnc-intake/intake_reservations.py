"""Scope: Reserve bounded daily upload slots and sign exact quarantine uploads."""

import base64
from datetime import datetime, timezone
import hashlib
import time

from intake_contract import IntakeContract


class IntakeReservations:
    def __init__(self, storage, clock=time.time):
        self.storage, self.clock = storage, clock

    def reserve(self, owner, body, email):
        request = IntakeContract().validate(body)
        now = int(self.clock())
        key = f"reservations/{owner}/{request['request_id']}.json"
        existing = self.storage.record(key)
        if existing is None:
            day = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%d")
            self._quota(owner, day, request["request_id"])
            candidate = {"owner": owner, "request": request, "email": email, "created_at": now, "expires_at": now + 900}
            self.storage.create(self.storage.quarantine, key, self.storage.json(candidate))
            existing = self.storage.record(key)
        if existing["request"] != request:
            raise ValueError("Request ID already belongs to different content.")
        return self.grants(existing)

    def _quota(self, owner, day, request_id):
        data = self.storage.json({"request_id": request_id})
        for slot in range(5):
            key = f"quotas/{day}/{owner}/{slot}.json"
            if self.storage.create(self.storage.quarantine, key, data):
                return
            if self.storage.record(key) == {"request_id": request_id}:
                return
        raise ValueError("Daily request limit reached. Try again tomorrow.")

    def grants(self, intent):
        remaining = intent["expires_at"] - int(self.clock())
        if remaining <= 0:
            raise ValueError("Upload reservation expired; create a new request.")
        uploads = {}
        for name, descriptor in intent["request"]["files"].items():
            fields = {"Content-Type": IntakeContract.FILES[name][1], "x-amz-checksum-algorithm": "SHA256",
                      "x-amz-checksum-sha256": base64.b64encode(bytes.fromhex(descriptor["sha256"])).decode()}
            conditions = [{k: v} for k, v in fields.items()]
            conditions.append(["content-length-range", descriptor["size"], descriptor["size"]])
            key = f"uploads/{intent['owner']}/{intent['request']['request_id']}/{name}"
            uploads[name] = self.storage.s3.generate_presigned_post(
                Bucket=self.storage.quarantine, Key=key, Fields=fields, Conditions=conditions, ExpiresIn=min(300, remaining))
        return {"request_id": intent["request"]["request_id"], "uploads": uploads}

    def owner(self, subject):
        return hashlib.sha256(subject.encode()).hexdigest()
