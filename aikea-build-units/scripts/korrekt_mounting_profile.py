"""Scope: Preserve measured 61854 mounting facts independently of vendor CAD bytes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KorrektMountingProfile:
    """Use the plate's native frame; z=0 is its contact with the deck underside."""

    manufacturer: str = "Hettich"
    plate_article: str = "61854"
    foot_article: str = "70151"
    plate_bounds_xy_mm: tuple[float, float, float, float] = (-39.55248, 55.45, -40.8, 39.2)
    socket_axis_xy_mm: tuple[float, float] = (-0.0475, -0.0631)
    screw_centres_xy_mm: tuple[tuple[float, float], ...] = (
        (-16.05, -32.8), (-16.05, 31.2), (47.95, -32.8), (47.95, 31.2),
    )
    pilot_diameter_mm: float = 3.0
    adjustment_diameter_mm: float = 8.0
    screw_size_mm: tuple[float, float] = (4.0, 35.0)
    source_step_sha256: str = "6b70098fc67bf09f6e3ac9006e10118b01391384e7116e759cd8a08454977e34"

    @property
    def plate_size_mm(self) -> tuple[float, float]:
        left, right, front, rear = self.plate_bounds_xy_mm
        return right - left, rear - front

    @property
    def bores(self) -> tuple[tuple[float, float, float], ...]:
        return tuple((x, y, self.pilot_diameter_mm) for x, y in self.screw_centres_xy_mm) + (
            (*self.socket_axis_xy_mm, self.adjustment_diameter_mm),
        )
