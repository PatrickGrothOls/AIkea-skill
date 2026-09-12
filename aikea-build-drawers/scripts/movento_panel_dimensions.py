"""Scope: Declare a 500 mm MOVENTO drawer's chosen panel construction dimensions."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class MoventoPanelDimensions:
    """Cabinet clear width is between the actual runner mounting faces."""

    clear_width_mm: float
    box_height_mm: float
    front_width_mm: float
    front_height_mm: float
    front_left_mm: float
    front_bottom_mm: float
    front_thickness_mm: float
    panel_material: str
    rail_material: str
    front_material: str

    def __post_init__(self):
        positive = (self.clear_width_mm, self.box_height_mm, self.front_width_mm,
                    self.front_height_mm, self.front_thickness_mm)
        if not all(isfinite(v) and v > 0 for v in positive):
            raise ValueError("drawer dimensions must be finite and positive")
        if self.clear_width_mm < 200 or self.box_height_mm < 100:
            raise ValueError("this panel recipe needs at least 200 mm clear width and 100 mm height")
        if not all((self.panel_material, self.rail_material, self.front_material)):
            raise ValueError("declare material identities for all drawer stock")

    @property
    def inside_width_mm(self):
        return self.clear_width_mm - 42


__all__ = ["MoventoPanelDimensions"]
