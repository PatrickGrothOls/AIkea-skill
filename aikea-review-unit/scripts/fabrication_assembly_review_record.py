"""Scope: Bind one client visual decision to the exact closed assembly GLB."""

from __future__ import annotations

import json
from pathlib import Path

from glb_artifact_snapshot import GlbArtifactSnapshot


class FabricationAssemblyReviewRecord:
    """Preserve approval only while the reviewed model bytes remain unchanged."""

    _MESSAGE = "Approve the complete closed assembly shown here for fabrication."

    def write_proposal(
        self,
        project_root: Path,
        model_path: Path,
    ) -> Path:
        record_path = project_root / "reviews/fabrication-assembly.json"
        model = GlbArtifactSnapshot.load(model_path)
        relative_model = model.path.relative_to(project_root.resolve())
        proposal = {
            "review_type": "fabrication_assembly",
            "status": "proposed",
            "message": self._MESSAGE,
            "artifact": str(relative_model),
            "artifact_sha256": model.sha256,
        }
        existing = self._read(record_path)
        if (
            existing.get("status") == "approved"
            and existing.get("artifact") == proposal["artifact"]
            and existing.get("artifact_sha256") == proposal["artifact_sha256"]
            and existing.get("decision_artifact_sha256")
            == proposal["artifact_sha256"]
        ):
            return record_path
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
        return record_path

    def _read(self, path: Path) -> dict:
        if not path.is_file():
            return {}
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return value if isinstance(value, dict) else {}


__all__ = ["FabricationAssemblyReviewRecord"]
