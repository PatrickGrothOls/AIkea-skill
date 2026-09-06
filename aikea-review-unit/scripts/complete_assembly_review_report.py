"""Scope: Record the exact contents of one recursively composed review GLB."""

from __future__ import annotations

import json
from math import isfinite
from pathlib import Path

from glb_artifact_snapshot import GlbArtifactSnapshot
from unit_mockup import UnitMockupInputError


class CompleteAssemblyReviewReport:
    """Expose names and placed bounds without project-local inspection code."""

    _MINIMUM_VOLUME_MM3 = 1e-6

    def write(
        self,
        assembly_id: str,
        glb_path: Path,
        parts: tuple,
        feature_states: dict[str, str],
    ) -> Path:
        artifact = GlbArtifactSnapshot.load(glb_path)
        self._validate_feature_states(feature_states)
        report_path = glb_path.with_suffix(".review.json")
        items = self._validated_items(parts)
        report = {
            "schema_version": 1,
            "review_type": "complete_recursive_assembly",
            "status": "valid",
            "manufacturing_authority": False,
            "assembly_id": assembly_id,
            "artifact": str(glb_path),
            "artifact_sha256": artifact.sha256,
            "part_count": len(items),
            "feature_states": feature_states,
            "items": items,
        }
        report_path.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        return report_path

    def _validated_items(self, parts: tuple) -> list[dict[str, object]]:
        names = tuple(getattr(part, "name", None) for part in parts)
        if not parts:
            raise UnitMockupInputError(["complete assembly review contains no parts"])
        if any(not isinstance(name, str) or not name.strip() for name in names):
            raise UnitMockupInputError(["complete assembly review has an invalid part name"])
        if len(set(names)) != len(names):
            raise UnitMockupInputError(["complete assembly review part names must be unique"])
        return [self._item(part) for part in parts]

    def _item(self, part) -> dict[str, object]:
        shape = part.placed_shape()
        if (
            shape.ShapeType() not in {"Solid", "CompSolid", "Compound"}
            or not shape.isValid()
            or shape.Volume() <= self._MINIMUM_VOLUME_MM3
        ):
            raise UnitMockupInputError(
                [f"complete assembly review part has invalid geometry: {part.name}"]
            )
        bounds = shape.BoundingBox()
        return {
            "name": part.name,
            "bounds_mm": {
                "x": self._axis(part.name, bounds.xmin, bounds.xmax),
                "y": self._axis(part.name, bounds.ymin, bounds.ymax),
                "z": self._axis(part.name, bounds.zmin, bounds.zmax),
            },
        }

    def _axis(self, name: str, minimum: float, maximum: float) -> list[float]:
        if not all(isfinite(value) for value in (minimum, maximum)) or maximum <= minimum:
            raise UnitMockupInputError(
                [f"complete assembly review part has invalid bounds: {name}"]
            )
        return [round(minimum, 6), round(maximum, 6)]

    def _validate_feature_states(self, states: dict[str, str]) -> None:
        invalid = tuple(
            key
            for key, value in states.items()
            if not isinstance(key, str)
            or not key.strip()
            or not isinstance(value, str)
            or not value.strip()
        )
        if invalid:
            raise UnitMockupInputError(["complete assembly review has invalid feature states"])


__all__ = ["CompleteAssemblyReviewReport"]
