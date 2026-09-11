"""Scope: Check placed furniture solids against an envelope and each other."""

from itertools import combinations
from math import isfinite
from contact_allowance_geometry import ContactAllowanceGeometry


class FurnitureGeometryCheck:
    """Check actual closed solids without inferring strength or fabrication readiness."""

    VOLUME_TOLERANCE_MM3 = 1e-4

    def check(self, parts, envelope, allowances=()) -> dict:
        if len(envelope.vals()) != 1:
            raise ValueError("the envelope must contain one Shape; combine its solids into a compound")
        allowed = envelope.val()
        if not allowed.isValid() or not allowed.Solids() or allowed.Volume() <= 0:
            raise ValueError("the design envelope must be a valid positive-volume solid")
        for part in parts:
            if len(part.solid.vals()) != 1:
                raise ValueError(
                    f"{part.name}: return one Shape per Workplane; use a compound for multiple solids"
                )
        shapes = tuple((part.name, part.placed_shape()) for part in parts)
        if not shapes:
            raise ValueError("the furniture design contains no physical parts")
        names = tuple(name for name, _ in shapes)
        if len(names) != len(set(names)):
            raise ValueError("physical item paths must be unique")
        contacts = ContactAllowanceGeometry()
        permitted = contacts.index(allowances, names)
        invalid = [
            name for name, shape in shapes
            if not shape.isValid() or not shape.Solids()
            or not isfinite(shape.Volume()) or shape.Volume() <= 0
        ]
        outside = []
        overlaps = []
        allowed_overlaps = []
        if not invalid:
            for name, shape in shapes:
                volume = shape.cut(allowed).Volume()
                if volume > self.VOLUME_TOLERANCE_MM3:
                    outside.append({"part": name, "outside_volume_mm3": volume})
            for (name_a, a), (name_b, b) in combinations(shapes, 2):
                if self._boxes_overlap(a.BoundingBox(), b.BoundingBox()):
                    intersection = a.intersect(b)
                    volume = intersection.Volume()
                    if volume > self.VOLUME_TOLERANCE_MM3:
                        record = {"parts": [name_a, name_b], "volume_mm3": round(volume, 6)}
                        allowance = permitted.get(frozenset((name_a, name_b)))
                        if allowance and contacts.permits(allowance, intersection, self.VOLUME_TOLERANCE_MM3):
                            allowed_overlaps.append(record | {"allowance_id": allowance["allowance_id"]})
                        else:
                            overlaps.append(record)
        return {
            "status": "invalid" if invalid or outside or overlaps else "valid",
            "part_count": len(shapes),
            "invalid_solids": invalid,
            "outside_envelope": outside,
            "overlaps": overlaps,
            "allowed_overlaps": allowed_overlaps,
            "volume_tolerance_mm3": self.VOLUME_TOLERANCE_MM3,
            "fabrication_ready": False,
            "scope": "Closed geometry only; requirements, joints, loads, hardware and motion need their own evidence.",
        }

    def _boxes_overlap(self, a, b) -> bool:
        return all(
            min(getattr(a, axis + "max"), getattr(b, axis + "max"))
            - max(getattr(a, axis + "min"), getattr(b, axis + "min")) > 1e-7
            for axis in "xyz"
        )
