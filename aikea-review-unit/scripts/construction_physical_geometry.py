"""Scope: Place every closed physical item using its complete typed tree path."""

from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart


class ConstructionPhysicalGeometry:
    """Keep position checks independent of shortened display names and review poses."""

    def build(self, visits):
        parts = []
        for visit in visits:
            if hasattr(visit, "part"):
                item = visit.part
            elif hasattr(visit, "hardware"):
                item = visit.hardware
                if not item.has_geometry or visit.local_to_root is None:
                    raise ValueError(f"{'/'.join(visit.path)}: exact placed hardware geometry is missing")
            else:
                continue
            parts.append(MockupPart("/".join(visit.path), item.solid,
                                    LocalToParentLocation().build(visit.local_to_root), (0.7, 0.6, 0.5, 1)))
        return tuple(parts)

    def bounds(self, parts):
        records = []
        for part in parts:
            box = part.placed_shape().BoundingBox()
            records.append({"path": part.name,
                            "minimum_mm": [round(getattr(box, axis + "min"), 6) for axis in "xyz"],
                            "maximum_mm": [round(getattr(box, axis + "max"), 6) for axis in "xyz"]})
        return sorted(records, key=lambda record: record["path"])
