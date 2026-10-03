"""Scope: Declare a dimensioned hole pattern in an existing part-local surface frame."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from surface_hole_pattern import SurfaceHole


@dataclass(frozen=True)
class SurfaceDrillingSpec:
    """Use the existing local-to-parent frame with positive local Z into the material."""

    machining_id: str
    part_id: str
    surface_to_part: Any
    holes: tuple[SurfaceHole, ...]
    reuse_machining_ids: tuple[str, ...] = ()
    operation_type: str = field(default="surface_holes", init=False)
