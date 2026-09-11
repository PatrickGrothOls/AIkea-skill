"""Scope: Declare a straight rectangular groove in an explicit panel surface frame."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SurfaceGrooveSpec:
    """Start at the center of one end; +X follows the run and +Z enters material."""

    machining_id: str
    part_id: str
    surface_to_part: Any
    length_mm: float
    width_mm: float
    depth_mm: float
    operation_type: str = field(default="surface_groove", init=False)
