"""Scope: Present an assembly run to the overall wardrobe calculator."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from assembly_run import AssemblyRun


class AssemblyRunOverallProjectAdapter:
    """Translate one checked assembly run without changing the source project."""

    def adapt(self, project: dict[str, Any], run: AssemblyRun) -> dict[str, Any]:
        adapted = deepcopy(project)
        settings = adapted["design_settings"]
        settings.pop("assembly_run")
        settings["cabinet_run"] = {
            "cabinet_count": len(run.assemblies),
            "cabinet_width_shares": [item.width_share for item in run.assemblies],
            "left_clearance": run.left_clearance,
            "right_clearance": run.right_clearance,
            "cabinet_gap": run.gap,
            "ceiling_clearance": run.ceiling_clearance,
        }
        return adapted


__all__ = ["AssemblyRunOverallProjectAdapter"]
