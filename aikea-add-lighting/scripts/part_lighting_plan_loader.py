"""Scope: Load one generated part-lighting plan from its local YAML source."""

from __future__ import annotations

from pathlib import Path

import yaml

from lighting_run import LightingRun
from part_lighting_plan import PartLightingPlan
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class PartLightingPlanLoader:
    """Parse the local source while resolving only verified hardware profiles."""

    _PROFILES = {DOMUS_APEX_84_HI.profile_id: DOMUS_APEX_84_HI}

    def load(self, path: Path) -> PartLightingPlan:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            raise ValueError(f"cannot read lighting plan {path}: {error}") from error
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValueError(f"unsupported lighting plan: {path}")
        host = data["host_part"]
        run = data["run"]
        profile_id = str(run["profile_id"])
        if profile_id not in self._PROFILES:
            raise ValueError(f"unverified recessed-light profile: {profile_id}")
        return PartLightingPlan(
            assembly_id=str(data["assembly_id"]),
            part_id=str(host["id"]),
            face=str(host["face"]),
            run=LightingRun(
                run_id=str(run["id"]),
                start_mm=self._point(run["start_mm"]),
                end_mm=self._point(run["end_mm"]),
                color_temperature_k=int(run["color_temperature_k"]),
                profile=self._PROFILES[profile_id],
            ),
        )

    def _point(self, values: object) -> tuple[float, float]:
        if not isinstance(values, list) or len(values) != 2:
            raise ValueError("lighting endpoints must contain two coordinates")
        return float(values[0]), float(values[1])


__all__ = ["PartLightingPlanLoader"]
