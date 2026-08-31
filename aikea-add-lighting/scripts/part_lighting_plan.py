"""Scope: Define one recessed-light run owned by one generated furniture part."""

from __future__ import annotations

from dataclasses import dataclass

from lighting_run import LightingRun


@dataclass(frozen=True, slots=True)
class PartLightingPlan:
    """Name the owning assembly, part, face, and single saved run."""

    assembly_id: str
    part_id: str
    face: str
    run: LightingRun

    def as_record(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "assembly_id": self.assembly_id,
            "host_part": {"id": self.part_id, "face": self.face},
            "run": {
                "id": self.run.run_id,
                "start_mm": list(self.run.start_mm),
                "end_mm": list(self.run.end_mm),
                "profile_id": self.run.profile.profile_id,
                "color_temperature_k": self.run.color_temperature_k,
            },
        }


__all__ = ["PartLightingPlan"]
