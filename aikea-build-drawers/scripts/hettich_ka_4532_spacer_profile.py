"""Scope: Define the approved KA 4532 runner and 13952 spacer relationship."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerProfile:
    """Hold the sourced products and dimensions that control the paired fit."""

    manufacturer: str
    runner_product_code: str
    runner_item_number: str
    runner_asset_id: str
    spacer_product_code: str
    spacer_item_number: str
    spacer_asset_id: str
    nominal_runner_length_mm: float
    installed_runner_width_per_side_mm: float
    spacer_width_per_side_mm: float
    runner_height_mm: float
    spacer_height_mm: float
    spacer_length_mm: float
    minimum_cabinet_depth_mm: float
    combined_load_capacity_kg: float
    runner_center_from_drawer_bottom_mm: float
    runner_front_from_drawer_front_mm: float
    spacer_bottom_from_drawer_bottom_mm: float
    spacer_front_from_cabinet_front_mm: float

    @property
    def hardware_width_per_side_mm(self) -> float:
        """Return the cabinet width consumed outside one wooden drawer side."""
        return self.spacer_width_per_side_mm + self.installed_runner_width_per_side_mm


HETTICH_KA_4532_500_WITH_13952 = HettichKa4532SpacerProfile(
    manufacturer="Hettich",
    runner_product_code="KA 4532 Silent System",
    runner_item_number="9114276",
    runner_asset_id="hettich-ka-4532-500-runner-pair",
    spacer_product_code="KA 4532 spacer profile",
    spacer_item_number="13952",
    spacer_asset_id="hettich-13952-spacer-profile",
    nominal_runner_length_mm=500.0,
    installed_runner_width_per_side_mm=12.7,
    spacer_width_per_side_mm=25.0,
    runner_height_mm=46.0,
    spacer_height_mm=50.0,
    spacer_length_mm=486.0,
    minimum_cabinet_depth_mm=504.0,
    combined_load_capacity_kg=20.0,
    runner_center_from_drawer_bottom_mm=23.0,
    runner_front_from_drawer_front_mm=2.0,
    spacer_bottom_from_drawer_bottom_mm=-2.0,
    spacer_front_from_cabinet_front_mm=10.0,
)


__all__ = ["HETTICH_KA_4532_500_WITH_13952", "HettichKa4532SpacerProfile"]
