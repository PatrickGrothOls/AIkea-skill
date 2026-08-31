"""Scope: Render one resolved KA 5332 drawer layout as inspectable YAML."""

from __future__ import annotations

import yaml

from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
)


class HettichKa5332DrawerLayoutRenderer:
    """Expose the wooden box, source CAD, fit evidence, and saved frames."""

    def render(self, plan: HettichKa5332CabinetDrawerPlan) -> str:
        layout = plan.layout
        mounting = plan.hardware_mounting
        source = plan.hardware_step.source
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
                        "side_thickness_mm": layout.side_thickness_mm,
                        "front_back_thickness_mm": layout.front_back_thickness_mm,
                        "bottom_thickness_mm": layout.bottom_thickness_mm,
                        "bottom_underside_recess_mm": (
                            layout.bottom_underside_recess_mm
                        ),
                        "outside_width_mm": plan.drawer.box.outside_width_mm,
                        "side_length_mm": plan.drawer.box.side_length_mm,
                        "outside_depth_mm": plan.drawer.box.outside_depth_mm,
                    },
                    "runner": {
                        "manufacturer": plan.runner.manufacturer,
                        "assembly_owner": plan.parent_assembly_id,
                        "product_code": plan.runner.product_code,
                        "item_number": plan.runner.item_number,
                        "asset_id": plan.runner.asset_id,
                        "nominal_length_mm": plan.runner.nominal_length_mm,
                        "geometry": plan.drawer.hardware_geometry_state,
                        "source": {
                            "filename": source.asset.path.name,
                            "sha256": source.asset.sha256,
                            "solid_count": source.solid_count,
                            "members_per_side": [
                                "cabinet_member",
                                "middle_member",
                                "drawer_member",
                            ],
                        },
                        "fit_evidence": {
                            "minimum_depth_met": mounting.minimum_depth_met,
                            "recommended_width_met": mounting.recommended_width_met,
                        },
                        "side_placements": {
                            "left": self._translation_data(
                                mounting.left_runner_translation_mm
                            ),
                            "right": self._translation_data(
                                mounting.right_runner_translation_mm
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

    def _translation_data(
        self,
        translation_mm: tuple[float, float, float],
    ) -> dict[str, float]:
        return dict(zip(("x", "y", "z"), translation_mm))


__all__ = ["HettichKa5332DrawerLayoutRenderer"]
