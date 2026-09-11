"""Scope: Restrict an allowed intersection to exact subjects, spatial bounds and volume."""

from math import isfinite

import cadquery as cq


class ContactAllowanceGeometry:
    """Validate geometric bounds only; the caller supplies qualified feature evidence."""

    def index(self, allowances, names):
        indexed, identifiers = {}, set()
        for allowance in allowances:
            subjects = allowance["subject_paths"]
            minimum, maximum = allowance["minimum_mm"], allowance["maximum_mm"]
            valid = (
                allowance["allowance_id"] and allowance["allowance_id"] not in identifiers
                and len(subjects) == 2 and len(set(subjects)) == 2 and set(subjects) <= set(names)
                and len(minimum) == len(maximum) == 3
                and all(isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)
                        for value in (*minimum, *maximum, allowance["maximum_volume_mm3"]))
                and all(low < high for low, high in zip(minimum, maximum))
                and allowance["maximum_volume_mm3"] > 0
            )
            pair = frozenset(subjects)
            if not valid or pair in indexed:
                raise ValueError("contact allowances need unique exact pairs and finite positive bounds")
            identifiers.add(allowance["allowance_id"])
            indexed[pair] = allowance
        return indexed

    def permits(self, allowance, intersection, tolerance):
        minimum, maximum = allowance["minimum_mm"], allowance["maximum_mm"]
        region = cq.Workplane("XY").box(
            *(high - low for low, high in zip(minimum, maximum)), centered=False,
        ).translate(tuple(minimum)).val()
        return (intersection.Volume() <= allowance["maximum_volume_mm3"] + tolerance
                and intersection.cut(region).Volume() <= tolerance)
