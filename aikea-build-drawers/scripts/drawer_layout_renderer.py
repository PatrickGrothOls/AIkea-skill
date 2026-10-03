"""Scope: Render one cabinet-owned drawer layout as inspectable YAML."""

from __future__ import annotations

import yaml

from cabinet_drawer_plan import CabinetDrawerPlan


class DrawerLayoutRenderer:
    """Expose resolved box, runner, mounting, and child-frame values."""

    def render(self, plan: CabinetDrawerPlan) -> str:
        layout = plan.layout
        x_mm, y_mm, z_mm = plan.origin_in_parent_mm
        data = {
            "schema_version": 1,
            "parent_assembly_id": plan.parent_assembly_id,
            "drawers": [
                {
                    "id": layout.drawer_id,
                    "bottom_height_mm": layout.bottom_height_mm,
                    "box": {
                        "height_mm": layout.box_height_mm,
                        "outside_width_mm": plan.drawer.box.outside_width_mm,
                        "side_length_mm": plan.drawer.box.side_length_mm,
                        "outside_depth_mm": plan.drawer.box.outside_depth_mm,
                        "side_thickness_mm": layout.side_thickness_mm,
                        "front_back_thickness_mm": layout.front_back_thickness_mm,
                        "bottom_thickness_mm": layout.bottom_thickness_mm,
                        "bottom_underside_recess_mm": (
                            layout.bottom_underside_recess_mm
                        ),
                    },
                    "runner": {
                        "manufacturer": "Blum",
                        "assembly_owner": plan.parent_assembly_id,
                        "product_code": plan.runner.product_code,
                        "item_number": plan.runner.item_number,
                        "nominal_length_mm": plan.runner.nominal_length_mm,
                        "geometry": plan.drawer.hardware_geometry_state,
                        "fixed_mounting_frames": {
                            "left": self._placement_data(
                                plan.hardware_mounting.runner_left_in_cabinet
                            ),
                            "right": self._placement_data(
                                plan.hardware_mounting.runner_right_in_cabinet
                            ),
                        },
                    },
                    "local_frame": {
                        "origin_in_parent_mm": {"x": x_mm, "y": y_mm, "z": z_mm},
                        "local_x_in_parent": [1.0, 0.0, 0.0],
                        "local_y_in_parent": [0.0, 1.0, 0.0],
                        "local_z_in_parent": [0.0, 0.0, 1.0],
                    },
                }
            ],
        }
        return yaml.safe_dump(data, sort_keys=False)

    def _placement_data(self, placement) -> dict:
        return {
            "origin_mm": dict(zip(("x", "y", "z"), placement.origin_mm)),
            "native_x_in_owner": list(placement.local_x_in_owner),
            "native_y_in_owner": list(placement.local_y_in_owner),
            "native_z_in_owner": list(placement.local_z_in_owner),
        }


__all__ = ["DrawerLayoutRenderer"]
