"""Scope: Read generated drawer choices before adding another cabinet child."""

from __future__ import annotations

from pathlib import Path

import yaml

from cabinet_drawer_plan import DrawerLayout


class HettichKa5332DrawerLayoutCollectionLoader:
    """Recover every generated drawer choice without reading child code."""

    def load(
        self,
        project_root: Path,
        parent_assembly_id: str,
    ) -> tuple[DrawerLayout, ...]:
        path = (
            project_root
            / "assemblies"
            / parent_assembly_id
            / "drawer-layout.yaml"
        )
        if not path.is_file():
            return ()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return tuple(self._layout(record) for record in data.get("drawers", ()))

    def _layout(self, record: dict) -> DrawerLayout:
        box = record["box"]
        requested_depth_mm = box.get("requested_depth_mm")
        resolved_depth_mm = box.get("resolved_depth_mm")
        selected_depth_mm = (
            requested_depth_mm
            if requested_depth_mm is not None
            else resolved_depth_mm
        )
        if selected_depth_mm is None:
            selected_depth_mm = box["side_length_mm"]
        return DrawerLayout(
            drawer_id=record["id"],
            bottom_height_mm=float(
                record.get(
                    "requested_bottom_height_mm",
                    record["bottom_height_mm"],
                )
            ),
            side_thickness_mm=float(box["side_thickness_mm"]),
            front_back_thickness_mm=float(box["front_back_thickness_mm"]),
            bottom_thickness_mm=float(box["bottom_thickness_mm"]),
            bottom_underside_recess_mm=float(
                box["bottom_underside_recess_mm"]
            ),
            box_height_mm=float(box["height_mm"]),
            box_depth_mm=float(selected_depth_mm),
        )


__all__ = ["HettichKa5332DrawerLayoutCollectionLoader"]
