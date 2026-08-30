"""Scope: Load every saved KA 5332 drawer and verify its composed child frame."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from hettich_ka_5332_mounting_plan import HettichKa5332MountingPlan
from unit_mockup import UnitMockupInputError


@dataclass(frozen=True, slots=True)
class HettichKa5332SavedDrawer:
    """Join one generated child to its saved runner and local-frame record."""

    drawer_id: str
    runner_item_number: str
    child: Any
    mounting: HettichKa5332MountingPlan


class HettichKa5332SavedDrawersLoader:
    """Require every saved record to match one composed drawer child."""

    def load(
        self,
        project_root: Path,
        assembly_id: str,
        built_cabinet: Any,
    ) -> tuple[HettichKa5332SavedDrawer, ...]:
        path = project_root / "assemblies" / assembly_id / "drawer-layout.yaml"
        if not path.is_file():
            raise UnitMockupInputError([f"missing saved drawer layout: {path}"])
        records = yaml.safe_load(path.read_text(encoding="utf-8")).get(
            "drawers", ()
        )
        children = {
            child.spec.assembly_id: child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        }
        record_ids = tuple(record["id"] for record in records)
        if len(set(record_ids)) != len(record_ids) or set(record_ids) != set(children):
            raise UnitMockupInputError(
                ["saved drawer layouts and composed cabinet children differ"]
            )
        return tuple(
            self._saved_drawer(record, children[record["id"]])
            for record in records
        )

    def _saved_drawer(self, record: dict, child: Any) -> HettichKa5332SavedDrawer:
        built_origin = child.spec.local_to_parent.origin_in_parent
        built_origin_mm = (
            built_origin.x_mm,
            built_origin.y_mm,
            built_origin.z_mm,
        )
        saved_origin_mm = self._vector(
            record["local_frame"]["origin_in_parent_mm"]
        )
        if built_origin_mm != saved_origin_mm:
            raise UnitMockupInputError(
                [f"saved and composed frames differ for {record['id']}"]
            )
        runner = record["runner"]
        fit = runner["fit_evidence"]
        system_32 = runner["system_32"]
        placements = runner["side_placements"]
        mounting = HettichKa5332MountingPlan(
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
        return HettichKa5332SavedDrawer(
            record["id"],
            str(runner["item_number"]),
            child,
            mounting,
        )

    def _vector(self, values: dict[str, float]) -> tuple[float, float, float]:
        return tuple(float(values[axis]) for axis in ("x", "y", "z"))


__all__ = ["HettichKa5332SavedDrawer", "HettichKa5332SavedDrawersLoader"]
