"""Scope: Load the saved KA 5332 drawer and runner frames for review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from hettich_ka_5332_mounting_plan import HettichKa5332MountingPlan
from unit_mockup import UnitMockupInputError


class HettichKa5332SavedPlanLoader:
    """Recreate the visual mounting plan only from generated project data."""

    def load(
        self,
        project_root: Path,
        assembly_id: str,
        built_cabinet: Any,
    ) -> HettichKa5332MountingPlan:
        path = project_root / "assemblies" / assembly_id / "drawer-layout.yaml"
        if not path.is_file():
            raise UnitMockupInputError([f"missing saved drawer layout: {path}"])
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        records = data.get("drawers", [])
        if len(records) != 1:
            raise UnitMockupInputError(
                ["KA 5332 review requires exactly one saved drawer"]
            )
        record = records[0]
        drawers = tuple(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )
        if len(drawers) != 1 or drawers[0].spec.assembly_id != record["id"]:
            raise UnitMockupInputError(
                ["saved drawer layout and composed cabinet child differ"]
            )
        child = drawers[0]
        built_origin = child.spec.local_to_parent.origin_in_parent
        built_origin_mm = (
            built_origin.x_mm,
            built_origin.y_mm,
            built_origin.z_mm,
        )
        saved_origin_mm = self._vector(record["local_frame"]["origin_in_parent_mm"])
        if built_origin_mm != saved_origin_mm:
            raise UnitMockupInputError(
                ["saved drawer origin and composed cabinet frame differ"]
            )
        runner = record["runner"]
        fit = runner["fit_evidence"]
        system_32 = runner["system_32"]
        placements = runner["side_placements"]
        return HettichKa5332MountingPlan(
            drawer_origin_mm=saved_origin_mm,
            drawer_outside_width_mm=child.assembly.spec.box.outside_width_mm,
            left_runner_translation_mm=self._vector(placements["left"]),
            right_runner_translation_mm=self._vector(placements["right"]),
            system_32_row_height_mm=float(
                system_32["front_node_row_height_mm"]
            ),
            resolved_drawer_bottom_height_mm=float(
                record["bottom_height_mm"]
            ),
            recommended_width_met=fit["recommended_width_met"],
            minimum_depth_met=fit["minimum_depth_met"],
        )

    def _vector(self, values: dict[str, float]) -> tuple[float, float, float]:
        return tuple(float(values[axis]) for axis in ("x", "y", "z"))


__all__ = ["HettichKa5332SavedPlanLoader"]
