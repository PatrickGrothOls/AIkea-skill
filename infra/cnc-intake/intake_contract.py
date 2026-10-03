"""Scope: Validate authenticated intake metadata and expected upload descriptors."""

import re
from uuid import UUID

from quote_preferences import QuotePreferences


class IntakeContract:
    FILES = {"source-repository.zip": (16_000_000, "application/zip"), "preview.png": (4_000_000, "image/png")}

    def validate(self, body):
        if not isinstance(body, dict) or set(body) != {"request_id", "preferences", "files", "model_sha256"}:
            raise ValueError("Invalid request fields.")
        request_id = self.identifier(body["request_id"])
        files = body["files"]
        if not isinstance(files, dict) or set(files) != set(self.FILES):
            raise ValueError("Only source ZIP and PNG preview uploads are accepted.")
        for name, item in files.items():
            if not isinstance(item, dict) or set(item) != {"size", "sha256"}:
                raise ValueError("Invalid upload descriptor.")
            if type(item["size"]) is not int or not 0 < item["size"] <= self.FILES[name][0]:
                raise ValueError("Upload exceeds size limit.")
            self.digest(item["sha256"])
        self.digest(body["model_sha256"])
        preferences = body["preferences"]
        if not isinstance(preferences, dict) or set(preferences) - {"title", "finish", "colour", "postcode", "timing", "notes", "selected"}:
            raise ValueError("Invalid preferences.")
        normalized = QuotePreferences(preferences).values
        return {"request_id": request_id, "preferences": normalized, "files": files,
                "model_sha256": body["model_sha256"]}

    def identifier(self, value):
        if not isinstance(value, str) or str(UUID(value)) != value:
            raise ValueError("Invalid request identifier.")
        return value

    def digest(self, value):
        if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
            raise ValueError("Invalid SHA-256 checksum.")
