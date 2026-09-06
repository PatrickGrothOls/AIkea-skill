"""Scope: Render one inspectable KA 4532 and 13952 drawer record."""

from __future__ import annotations

import yaml


class HettichKa4532SpacerLayoutRenderer:
    """Save sourced identities, limits, placements, and the machining boundary."""

    def render(self, plan) -> str:
        hardware = plan.hardware
        mounting = plan.hardware_mounting
        payload = {
            "schema_version": 1,
            "parent_assembly_id": plan.parent_assembly_id,
            "drawer": {
                "id": plan.drawer.assembly_id,
                "box": {
                    "height_mm": plan.drawer.box.sizing.box_height_mm,
                    "outside_width_mm": plan.drawer.box.outside_width_mm,
                    "outside_depth_mm": plan.drawer.box.outside_depth_mm,
                    "side_length_mm": plan.drawer.box.side_length_mm,
                },
                "local_origin_mm": list(plan.origin_in_parent_mm),
            },
            "purchased_set": {
                "runner": {
                    "manufacturer": hardware.manufacturer,
                    "product_code": hardware.runner_product_code,
                    "item_number": hardware.runner_item_number,
                    "asset_id": hardware.runner_asset_id,
                    "sha256": plan.hardware_step.runner_source.asset.sha256,
                },
                "spacer": {
                    "manufacturer": hardware.manufacturer,
                    "product_code": hardware.spacer_product_code,
                    "item_number": hardware.spacer_item_number,
                    "asset_id": hardware.spacer_asset_id,
                    "sha256": plan.hardware_step.spacer_source.asset.sha256,
                    "instances": 2,
                },
                "minimum_cabinet_depth_mm": hardware.minimum_cabinet_depth_mm,
                "combined_load_capacity_kg": hardware.combined_load_capacity_kg,
            },
            "placements": {
                name: self._placement(getattr(mounting, name))
                for name in (
                    "spacer_left_in_cabinet",
                    "spacer_right_in_cabinet",
                    "fixed_runner_left_in_cabinet",
                    "fixed_runner_right_in_cabinet",
                    "moving_runner_left_in_drawer",
                    "moving_runner_right_in_drawer",
                )
            },
            "machining_authority": plan.machining_authority,
        }
        return yaml.safe_dump(payload, sort_keys=False)

    def _placement(self, placement) -> dict[str, object]:
        return {
            "origin_mm": list(placement.origin_mm),
            "local_x": list(placement.local_x_in_owner),
            "local_y": list(placement.local_y_in_owner),
            "local_z": list(placement.local_z_in_owner),
        }


__all__ = ["HettichKa4532SpacerLayoutRenderer"]
