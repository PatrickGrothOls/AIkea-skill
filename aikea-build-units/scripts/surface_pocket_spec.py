"""Scope: Declare a rectangular pocket or through-opening with an explicit corner radius."""
from dataclasses import dataclass, field
from surface_groove_spec import SurfaceGrooveSpec


@dataclass(frozen=True)
class SurfacePocketSpec(SurfaceGrooveSpec):
    """Use the groove frame: X along length, Y across its center, Z into material."""

    corner_radius_mm: float = 0.0
    operation_type: str = field(default="surface_pocket", init=False)
