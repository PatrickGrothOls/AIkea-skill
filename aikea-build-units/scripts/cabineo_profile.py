"""Scope: Define fixed Cabineo construction profiles owned by AIkea."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CabineoProfile:
    """Name the cutter asset and fixed placement values for one connector."""

    profile_id: str
    profile_revision: int
    cutter_asset_filename: str
    alignment_asset_filename: str
    face_inset_mm: float
    pocket_depth_mm: float
    extra_floor_mm: float
    minimum_sheet_thickness_mm: float


NON_BOTTOM_CABINEO = CabineoProfile(
    profile_id="cabineo_8_non_bottom",
    profile_revision=1,
    cutter_asset_filename="Cabineo_8_connector_9dot1_19dot5.step",
    alignment_asset_filename="cabineo_with_perimeter_cap.step",
    face_inset_mm=9.5,
    pocket_depth_mm=10.5,
    extra_floor_mm=0.5,
    minimum_sheet_thickness_mm=10.0,
)


__all__ = ["CabineoProfile", "NON_BOTTOM_CABINEO"]
