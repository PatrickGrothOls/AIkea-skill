"""Scope: Define numeric stock, panel rectangles and sheet placements."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class SheetStock:
    width_mm: float = 1220.0
    height_mm: float = 2440.0
    edge_margin_mm: float = 10.0
    part_gap_mm: float = 8.0
    allow_rotation: bool = False

    def __post_init__(self):
        values = (self.width_mm, self.height_mm, self.edge_margin_mm, self.part_gap_mm)
        if not all(isfinite(value) for value in values):
            raise ValueError("stock dimensions and clearances must be finite")
        if min(self.edge_margin_mm, self.part_gap_mm) < 0:
            raise ValueError("clearances cannot be negative")
        if min(self.width_mm, self.height_mm) <= 2 * self.edge_margin_mm:
            raise ValueError("sheet must have a positive usable area")


@dataclass(frozen=True)
class SheetPart:
    path: str
    width_mm: float
    height_mm: float


@dataclass(frozen=True)
class SheetPlacement:
    part: SheetPart
    x_mm: float
    y_mm: float
    width_mm: float
    height_mm: float
    rotated: bool

    @property
    def right_mm(self) -> float:
        return self.x_mm + self.width_mm

    @property
    def top_mm(self) -> float:
        return self.y_mm + self.height_mm

    def clears(self, other: "SheetPlacement", gap_mm: float) -> bool:
        return (
            self.right_mm + gap_mm <= other.x_mm + 1e-6
            or other.right_mm + gap_mm <= self.x_mm + 1e-6
            or self.top_mm + gap_mm <= other.y_mm + 1e-6
            or other.top_mm + gap_mm <= self.y_mm + 1e-6
        )
