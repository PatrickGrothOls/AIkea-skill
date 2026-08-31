"""Scope: Record the exact contents of one recursively composed review GLB."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


class CompleteAssemblyReviewReport:
    """Expose names and placed bounds without project-local inspection code."""

    def write(
        self,
        assembly_id: str,
        glb_path: Path,
        parts: tuple,
        feature_states: dict[str, str],
    ) -> Path:
        report_path = glb_path.with_suffix(".review.json")
        items = [self._item(part) for part in parts]
        report = {
            "schema_version": 1,
            "review_type": "complete_recursive_assembly",
            "status": "valid",
            "manufacturing_authority": False,
            "assembly_id": assembly_id,
            "artifact": str(glb_path),
            "artifact_sha256": sha256(glb_path.read_bytes()).hexdigest(),
            "part_count": len(items),
            "feature_states": feature_states,
            "items": items,
        }
        report_path.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        return report_path

    def _item(self, part) -> dict[str, object]:
        bounds = part.placed_shape().BoundingBox()
        return {
            "name": part.name,
            "bounds_mm": {
                "x": [bounds.xmin, bounds.xmax],
                "y": [bounds.ymin, bounds.ymax],
                "z": [bounds.zmin, bounds.zmax],
            },
        }


__all__ = ["CompleteAssemblyReviewReport"]
