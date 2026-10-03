"""Scope: Declare a bounded intentional intersection between two exact physical items."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContactAllowanceSpec:
    allowance_id: str
    subject_paths: tuple[str, str]
    minimum_mm: tuple[float, float, float]
    maximum_mm: tuple[float, float, float]
    maximum_volume_mm3: float
    evidence_feature: str
    basis: str
