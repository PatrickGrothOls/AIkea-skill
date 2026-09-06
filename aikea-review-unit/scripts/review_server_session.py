"""Scope: Bind one local viewer session to immutable GLB bytes and one token."""

from __future__ import annotations

from pathlib import Path
import secrets

from glb_artifact_snapshot import GlbArtifactSnapshot
from review_decision_store import ReviewDecisionStore


class ReviewServerSession:
    """Expose one snapshotted model and one decision capability."""

    def __init__(self, model_path: Path, review_path: Path | None) -> None:
        self.artifact = GlbArtifactSnapshot.load(model_path)
        self.store = ReviewDecisionStore(review_path) if review_path else None
        self.token = secrets.token_urlsafe(32) if self.store else None
        if self.store:
            self.store.read(self.artifact)

    def review_data(self) -> dict:
        if self.store is None:
            raise ValueError("this viewer has no decision record")
        return self.store.read(self.artifact) | {"decision_token": self.token}

    def decide(self, decision: str, token: str | None) -> dict:
        if self.store is None:
            raise ValueError("this viewer has no decision record")
        if (
            not isinstance(token, str)
            or not isinstance(self.token, str)
            or not secrets.compare_digest(token, self.token)
        ):
            raise PermissionError("review decision token is invalid")
        return self.store.decide(decision, self.artifact)


__all__ = ["ReviewServerSession"]
