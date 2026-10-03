"""Scope: Freeze and authorize one local viewer's retryable quote submission."""

from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import secrets
from threading import Lock
from uuid import uuid4
from zipfile import ZipFile, BadZipFile

from quote_request_payload import QuoteRequestPayload


class QuoteSubmissionSession:
    def __init__(self, package: bytes, model_sha256: str) -> None:
        if len(package) > 64_000_000:
            raise ValueError("Quote design ZIP exceeds 64 MB.")
        try:
            with ZipFile(io.BytesIO(package)) as archive:
                if "source-manifest.json" not in archive.namelist():
                    raise ValueError("Quote package must contain the editable source repository.")
                if any(Path(name).suffix.lower() in {".step", ".stp"} for name in archive.namelist()):
                    raise ValueError("Send editable source, not STEP files.")
        except BadZipFile as error:
            raise ValueError("Quote design package must be a ZIP file.") from error
        self.package, self.model_sha256 = package, model_sha256
        self.token = secrets.token_urlsafe(32)
        self.request_id, self.created_at = str(uuid4()), datetime.now(timezone.utc).isoformat()
        self.lock, self.fingerprint, self.receipt = Lock(), None, None

    def status(self):
        return {"enabled": True, "token": self.token, "receipt": self.receipt}

    def submit(self, body, token):
        if not isinstance(token, str) or not secrets.compare_digest(token, self.token):
            raise PermissionError("Invalid quote submission token.")
        payload = QuoteRequestPayload(body)
        fingerprint = hashlib.sha256(self._json(payload.preferences) + payload.preview).hexdigest()
        with self.lock:
            if self.fingerprint and self.fingerprint != fingerprint:
                raise ValueError("This request has started. Retry unchanged, or open a new viewer for a different request.")
            if self.receipt:
                return self.receipt
            self.fingerprint = fingerprint
            self.receipt = self._deliver(payload)
            return self.receipt

    def _deliver(self, payload):
        raise NotImplementedError

    def _json(self, value):
        return json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
