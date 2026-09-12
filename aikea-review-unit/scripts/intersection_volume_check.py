"""Scope: Cross-check one CAD intersection against independent subtraction volumes."""
from math import isfinite


class IntersectionVolumeCheck:
    """Return the native result and a diagnostic when the kernel's volume identities disagree."""

    def measure(self, first, second, tolerance):
        intersection = first.intersect(second)
        volumes = {
            "intersection_volume_mm3": intersection.Volume(),
            "removed_from_first_mm3": first.Volume() - first.cut(second).Volume(),
            "removed_from_second_mm3": second.Volume() - second.cut(first).Volume(),
        }
        values = tuple(volumes.values())
        inconsistent = (any(not isfinite(value) or value < -tolerance for value in values)
                        or max(values) - min(values) > tolerance)
        if inconsistent:
            return intersection, {
                "reason": "CAD Boolean volumes disagree; intersection is unresolved",
                **{name: value if isfinite(value) else None for name, value in volumes.items()},
            }
        return intersection, None
