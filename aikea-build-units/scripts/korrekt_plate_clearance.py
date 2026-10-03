"""Scope: Check the whole 61854 plate envelope against assembled deck boundaries."""

from math import isfinite

import cadquery as cq

from part_construction_error import PartConstructionError


class KorrektPlateClearance:
    """Measure clearance to external edges and cutouts, ignoring joined panel seams."""

    def check(self, support: cq.Shape, footprint: cq.Wire,
              minimum_margin_mm: float) -> float:
        if not isfinite(minimum_margin_mm) or minimum_margin_mm < 0:
            raise PartConstructionError("Plate edge margin must be finite and non-negative")
        bounds = support.BoundingBox()
        slab = cq.Solid.extrudeLinear(footprint, [], cq.Vector(0, 0, bounds.zlen))
        missing = slab.cut(support).Volume()
        if missing > 1e-5:
            raise PartConstructionError("Korrekt plate footprint extends beyond the supporting deck")
        bottom_faces = [face for face in support.Faces()
                        if face.geomType() == "PLANE" and face.normalAt().z < -0.999999]
        clearance = min(footprint.distance(wire) for face in bottom_faces for wire in face.Wires())
        if clearance + 1e-6 < minimum_margin_mm:
            raise PartConstructionError(
                f"Korrekt plate has {clearance:.3f} mm edge clearance; {minimum_margin_mm:g} mm required")
        return clearance
