"""Scope: Estimate actual door stock and finish mass from explicit material inputs."""

from dataclasses import dataclass
from math import hypot, isfinite


@dataclass(frozen=True)
class DoorMassEstimate:
    panel_and_finish_kg: float
    attached_hardware_kg: float | None
    basis: str

    @property
    def total_kg(self):
        if self.attached_hardware_kg is None:
            return None
        return self.panel_and_finish_kg + self.attached_hardware_kg


class DoorMassEstimator:
    def estimate(self, host, densities_kg_m3, coatings_kg_m2, *,
                 attached_hardware_kg=None, basis):
        if not basis.strip():
            raise ValueError("Door mass needs its density/finish source or assumption")
        if attached_hardware_kg is not None and (
                not isfinite(attached_hardware_kg) or attached_hardware_kg < 0):
            raise ValueError("Attached hardware mass must be nonnegative or explicitly unknown")
        # A multi-part front's envelope is a planning datum, never its material volume.
        panels = tuple((part.spec, part.solid.val()) for part in host.front.assembly.parts) \
            if hasattr(host, "front") else ((host.door, None),)
        total = 0.0
        for part, solid in panels:
            density = densities_kg_m3[part.material_id]
            coating = coatings_kg_m2[part.material_id]
            if not isfinite(density) or density <= 0 or not isfinite(coating) or coating < 0:
                raise ValueError("Door density must be positive and coating mass nonnegative")
            volume, surface = (solid.Volume()/1e9, solid.Area()/1e6) \
                if solid is not None else self._blank_geometry(part)
            total += volume*density + surface*coating
        return DoorMassEstimate(total, attached_hardware_kg, basis)

    def _blank_geometry(self, part):
        width, height, thickness = part.local_size_mm
        points = tuple((p.x_mm, p.height_mm) for p in part.outline_mm) \
            if part.outline_mm else ((0, 0), (width, 0), (width, height), (0, height))
        edges = tuple(zip(points, (*points[1:], points[0])))
        area = abs(sum(x1*y2-x2*y1 for (x1,y1),(x2,y2) in edges))/2
        perimeter = sum(hypot(x2-x1, y2-y1) for (x1,y1),(x2,y2) in edges)
        return area*thickness/1e9, (2*area+perimeter*thickness)/1e6
