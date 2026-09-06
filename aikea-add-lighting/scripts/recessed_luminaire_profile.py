"""Scope: Define verified purchased recessed-luminaire manufacturing profiles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecessedLuminaireProfile:
    """Keep manufacturer-owned groove and electrical facts together."""

    profile_id: str
    manufacturer: str
    product_name: str
    source_url: str
    groove_width_mm: float
    groove_depth_mm: float
    voltage_v: int
    power_w_per_m: float
    cable_length_mm: float
    color_temperatures_k: tuple[int, ...]

    def supports(self, color_temperature_k: int) -> bool:
        return color_temperature_k in self.color_temperatures_k


DOMUS_APEX_84_HI = RecessedLuminaireProfile(
    profile_id="domus_apex_84_hi",
    manufacturer="Domus Line",
    product_name="APEX 84 HI",
    source_url="https://www.domusline.com/product/apex-84/",
    groove_width_mm=4.0,
    groove_depth_mm=8.0,
    voltage_v=24,
    power_w_per_m=10.0,
    cable_length_mm=2000.0,
    color_temperatures_k=(2900, 3200, 4300),
)


__all__ = ["DOMUS_APEX_84_HI", "RecessedLuminaireProfile"]
