"""Scope: Bind one local viewer session to immutable GLB bytes and one token."""

from __future__ import annotations

from pathlib import Path
import secrets

from glb_artifact_snapshot import GlbArtifactSnapshot
from review_decision_store import ReviewDecisionStore
from verified_blender_presentation import VerifiedBlenderPresentation


class ReviewServerSession:
    """Expose one snapshotted model and one decision capability."""

    def __init__(self, model_path: Path, review_path: Path | None, inspection_path: Path | None = None) -> None:
        self.artifact = GlbArtifactSnapshot.load(model_path)
        self.inspection = GlbArtifactSnapshot.load(inspection_path) if inspection_path else None
        VerifiedBlenderPresentation().require(self.artifact, self.inspection)
        self.store = ReviewDecisionStore(review_path) if review_path else None
        self.token = secrets.token_urlsafe(32) if self.store else None
        self.construction_sha256 = ""
        if self.store:
            self.construction_sha256 = self.store.read(self.artifact).get("construction_sha256", "")

    def models(self) -> dict:
        """Describe only fixed session routes; decision authority remains the primary artifact."""
        return {
            "assembled": {"url": "/model.glb", "baked": True,
                          "sha256": self.artifact.sha256},
            "inspection": {"url": "/inspection.glb", "baked": False,
                           "sha256": self.inspection.sha256},
        }

    def display_artifact(self, path: str) -> GlbArtifactSnapshot | None:
        return {"/model.glb": self.artifact, "/inspection.glb": self.inspection}.get(path)

    def review_data(self) -> dict:
        if self.store is None:
            raise ValueError("this viewer has no decision record")
        return self.store.read(self.artifact, self.construction_sha256) | {"decision_token": self.token}

    def decide(self, decision: str, token: str | None) -> dict:
        if self.store is None:
            raise ValueError("this viewer has no decision record")
        if (
            not isinstance(token, str)
            or not isinstance(self.token, str)
            or not secrets.compare_digest(token, self.token)
        ):
            raise PermissionError("review decision token is invalid")
        return self.store.decide(decision, self.artifact, self.construction_sha256)


__all__ = ["ReviewServerSession"]
