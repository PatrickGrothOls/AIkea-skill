"""Scope: Define the reusable structural spacing policy for a sheet-material base."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BaseConstructionProfile:
    """Keep local base construction limits separate from project dimensions."""

    profile_id: str
    maximum_brace_spacing_mm: float

    def __post_init__(self) -> None:
        if self.maximum_brace_spacing_mm <= 0:
            raise ValueError("maximum brace spacing must be greater than zero")


SHEET_BASE_320 = BaseConstructionProfile(
    profile_id="sheet-base-320",
    maximum_brace_spacing_mm=320.0,
)


__all__ = ["BaseConstructionProfile", "SHEET_BASE_320"]
