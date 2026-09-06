"""Scope: Carry verified KA 4532 rail-to-spacer fixing-axis evidence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerFixingAxis:
    """Describe one official rail axis in cabinet and exact-spacer frames."""

    side: str
    cabinet_depth_from_front_mm: float
    cabinet_height_mm: float
    runner_native_depth_mm: float
    spacer_native_depth_mm: float
    spacer_native_height_mm: float


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerFixingAlignment:
    """Prove official rail openings land in the spacer's solid centre web."""

    installation_document: str
    installation_url: str
    hole_diameter_mm: float
    spacer_support_width_mm: float
    axes: tuple[HettichKa4532SpacerFixingAxis, ...]

    @property
    def cabinet_depth_axes_mm(self) -> tuple[float, ...]:
        """Return the one repeated official depth pattern without side copies."""
        return tuple(
            axis.cabinet_depth_from_front_mm
            for axis in self.axes
            if axis.side == "left"
        )


__all__ = [
    "HettichKa4532SpacerFixingAlignment",
    "HettichKa4532SpacerFixingAxis",
]
