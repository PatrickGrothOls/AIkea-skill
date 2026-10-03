"""Scope: Configure delivery and publish packages using the trusted host's AWS identity."""

import hashlib
import json
import os
from pathlib import Path

from cnc_deployment_config import CncDeploymentConfig
from quote_object_store import QuoteObjectStore
from quote_source_repository import QuoteSourceRepository
from quote_submission_session import QuoteSubmissionSession


class QuoteDeliverySession(QuoteSubmissionSession):
    def __init__(self, package: bytes, model_sha256: str, store: QuoteObjectStore):
        super().__init__(package, model_sha256)
        self.store = store

    @classmethod
    def from_environment(cls, model_sha256: str):
        source_root = os.environ.get("AIKEA_CNC_SOURCE_REPO")
        if not source_root:
            return None
        root = Path(source_root)
        project = root / os.environ.get("AIKEA_CNC_PROJECT_PATH", "")
        package = QuoteSourceRepository(root, project).build()
        config_path = os.environ.get("AIKEA_CNC_GATEWAY_CONFIG")
        if config_path:
            from hosted_quote_session import HostedQuoteSession
            return HostedQuoteSession(package, model_sha256, json.loads(Path(config_path).read_text()))
        target_path = os.environ.get("AIKEA_CNC_DEPLOYMENT_CONFIG")
        if not target_path:
            raise ValueError("Trusted-host delivery requires AIKEA_CNC_DEPLOYMENT_CONFIG.")
        target = CncDeploymentConfig.from_file(target_path)
        target.require_live_target()
        store = QuoteObjectStore(target.accepted_bucket, target.region,
                                 os.environ.get("AIKEA_CNC_AWS_PROFILE", "default"))
        return cls(package, model_sha256, store)

    def _deliver(self, payload):
        prefix = f"aikea/cnc-requests/{self.request_id}/"
        request = {"schema_version": 1, "request_id": self.request_id,
                   "created_at": self.created_at, "model_sha256": self.model_sha256,
                   "purpose": "quote_only_not_cut_approval", **payload.preferences}
        files = {"source-repository.zip": (self.package, "application/zip"),
                 "preview.png": (payload.preview, "image/png"),
                 "request.json": (self._json(request), "application/json")}
        manifest = {"schema_version": 1, "request_id": self.request_id, "files": {}}
        for name, (content, content_type) in files.items():
            self.store.put(prefix + name, content, content_type)
            manifest["files"][name] = {"size": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        # The last conditional upload is the only notification trigger.
        self.store.put(prefix + "ready.json", self._json(manifest), "application/json")
        return {"request_id": self.request_id, "status": "submitted",
                "services_sent": ["machining"], "notification": "pending"}
