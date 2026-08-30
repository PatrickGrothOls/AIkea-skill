"""Scope: Define sourced planning values for the 500 mm Hettich KA 5332 pair."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HettichKa5332RunnerProfile:
    """Hold only manufacturer values that control drawer and runner geometry."""

    manufacturer: str
    product_code: str
    item_number: str
    asset_id: str
    nominal_length_mm: float
    minimum_cabinet_depth_mm: float
    installed_width_per_side_mm: float
    runner_height_mm: float
    installation_envelope_height_mm: float
    runner_center_from_drawer_bottom_mm: float
    runner_front_from_drawer_front_mm: float
    manufacturer_origin_from_drawer_front_mm: float
    cabinet_fixing_positions_from_front_mm: tuple[float, ...]
    drawer_fixing_positions_from_front_mm: tuple[float, ...]
    cabinet_hole_diameter_mm: float
    cabinet_hole_depth_mm: float
    drawer_pilot_diameter_mm: float
    drawer_pilot_depth_mm: float
    recommended_maximum_drawer_width_mm: float
    load_capacity_kg: float


HETTICH_KA_5332_500 = HettichKa5332RunnerProfile(
    manufacturer="Hettich",
    product_code="KA 5332",
    item_number="9057405",
    asset_id="hettich-ka-5332-500-runner-pair",
    nominal_length_mm=500.0,
    minimum_cabinet_depth_mm=504.0,
    installed_width_per_side_mm=12.7,
    runner_height_mm=45.0,
    installation_envelope_height_mm=46.0,
    runner_center_from_drawer_bottom_mm=23.0,
    runner_front_from_drawer_front_mm=2.0,
    manufacturer_origin_from_drawer_front_mm=37.0,
    cabinet_fixing_positions_from_front_mm=(37.0, 128.0, 224.0, 352.0, 416.0),
    drawer_fixing_positions_from_front_mm=(37.0, 128.0, 192.0, 352.0, 442.0),
    cabinet_hole_diameter_mm=5.0,
    cabinet_hole_depth_mm=13.0,
    drawer_pilot_diameter_mm=2.5,
    drawer_pilot_depth_mm=10.0,
    recommended_maximum_drawer_width_mm=550.0,
    load_capacity_kg=30.0,
)


__all__ = ["HETTICH_KA_5332_500", "HettichKa5332RunnerProfile"]
