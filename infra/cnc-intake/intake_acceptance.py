"""Scope: Validate pinned upload bytes and publish one immutable notification package."""

from datetime import datetime, timezone
import hashlib
import time

from intake_contract import IntakeContract
from package_validation import PackageValidation
from preview_validation import PreviewValidation


class IntakeAcceptance:
    def __init__(self, storage, clock=time.time):
        self.storage, self.clock = storage, clock

    def complete(self, owner, request_id):
        IntakeContract().identifier(request_id)
        intent = self.storage.record(f"reservations/{owner}/{request_id}.json")
        if intent is None:
            raise PermissionError("Request does not belong to this account.")
        # The accepted ID is server-derived and namespace-separated from local UUIDs.
        from uuid import UUID, uuid5
        accepted_id = str(uuid5(UUID("a554e84c-5467-4aae-a1ba-cf8c904a0dcb"), owner + "/" + request_id))
        prefix = f"aikea/cnc-requests/{accepted_id}/"
        receipt = {"request_id": accepted_id, "status": "submitted", "services_sent": ["machining"], "notification": "pending"}
        if self.storage.read(self.storage.accepted, prefix + "ready.json", 16_384) is not None:
            return receipt
        if int(self.clock()) >= intent["expires_at"]:
            raise ValueError("Upload reservation expired.")
        files = {}
        for name, expected in intent["request"]["files"].items():
            key = f"uploads/{owner}/{request_id}/{name}"
            content = self.storage.read(self.storage.quarantine, key, expected["size"])
            if content is None or len(content) != expected["size"] or hashlib.sha256(content).hexdigest() != expected["sha256"]:
                raise ValueError("Upload missing or checksum mismatch.")
            files[name] = content
        PackageValidation().validate(files["source-repository.zip"])
        PreviewValidation().validate(files["preview.png"])
        request = {"schema_version": 1, "request_id": accepted_id,
                   "created_at": datetime.fromtimestamp(intent["created_at"], timezone.utc).isoformat(),
                   "purpose": "quote_only_not_cut_approval", "source_trust": "untrusted_do_not_execute",
                   "contact_email": intent["email"], "owner": owner,
                   "model_sha256": intent["request"]["model_sha256"], **intent["request"]["preferences"]}
        files["request.json"] = self.storage.json(request)
        manifest = {"schema_version": 1, "request_id": accepted_id, "files": {}}
        for name, data in files.items():
            content_type = IntakeContract.FILES[name][1] if name in IntakeContract.FILES else "application/json"
            self.storage.immutable(self.storage.accepted, prefix + name, data, content_type)
            manifest["files"][name] = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        self.storage.immutable(self.storage.accepted, prefix + "ready.json", self.storage.json(manifest))
        return receipt
