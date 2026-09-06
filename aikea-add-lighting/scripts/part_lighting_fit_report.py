"""Scope: Record deterministic fit evidence for one host-owned light run."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PartLightingFitReport:
    """Keep each manufacturing and placement check independently visible."""

    status: str
    run_inside_host_face: bool
    groove_within_host_thickness: bool
    groove_avoids_existing_machining: bool
    purchased_body_fits_groove: bool
    purchased_body_avoids_other_parts: bool
    emission_points_into_cabinet: bool
    remaining_material_mm: float
    existing_machining_overlap_mm3: float
    purchased_body_overlap_mm3: float
    other_part_overlap_mm3: float
    frame_path: dict[str, object]

    @property
    def is_valid(self) -> bool:
        return self.status == "pass"

    def as_record(self) -> dict[str, object]:
        return {
            "status": self.status,
            "checks": {
                "run_inside_host_face": self.run_inside_host_face,
                "groove_within_host_thickness": self.groove_within_host_thickness,
                "groove_avoids_existing_machining": self.groove_avoids_existing_machining,
                "purchased_body_fits_groove": self.purchased_body_fits_groove,
                "purchased_body_avoids_other_parts": self.purchased_body_avoids_other_parts,
                "emission_points_into_cabinet": self.emission_points_into_cabinet,
            },
            "measurements": {
                "remaining_material_mm": self.remaining_material_mm,
                "existing_machining_overlap_mm3": self.existing_machining_overlap_mm3,
                "purchased_body_overlap_mm3": self.purchased_body_overlap_mm3,
                "other_part_overlap_mm3": self.other_part_overlap_mm3,
            },
            "frame_path": self.frame_path,
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.as_record(), indent=2) + "\n", encoding="utf-8")


__all__ = ["PartLightingFitReport"]
