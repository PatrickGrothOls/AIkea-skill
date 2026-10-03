"""Scope: Represent deterministic fit evidence for one recessed-light panel."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class LightingPanelFitReport:
    """Report the checks needed before visual approval can begin."""

    status: str
    run_inside_panel: bool
    groove_within_thickness: bool
    remaining_panel_thickness_mm: float
    body_panel_overlap_mm3: float
    purchased_body_fits_groove: bool

    def as_record(self) -> dict[str, object]:
        return asdict(self)


__all__ = ["LightingPanelFitReport"]
