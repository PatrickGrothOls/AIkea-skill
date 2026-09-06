"""Scope: Render one fully placed manufactured-part specification."""

from __future__ import annotations

from assembly_taxonomy import BoundaryPoint, PartPlacementTaxonomy, PartTaxonomy


class PartSpecSourceRenderer:
    """Translate resolved taxonomy placement into the project contract."""

    def render(self, part: PartTaxonomy) -> str:
        placement = part.local_to_parent
        if placement is None:
            raise ValueError(f"part has no resolved placement: {part.part_id}")
        return (
            "        PartSpec(\n"
            f"            part_id={part.part_id!r},\n"
            f"            role={part.role!r},\n"
            f"            dimensions_mm={part.dimensions_mm!r},\n"
            f"            local_to_parent={self._placement(placement)},\n"
            f"            outline_mm={self._points(part.outline_mm)},\n"
            f"            local_size_mm={part.local_size_mm!r},\n"
            f"            inside_face={part.inside_face!r},\n"
            "        ),"
        )

    def _placement(self, placement: PartPlacementTaxonomy) -> str:
        origin = placement.origin_in_parent_mm
        x_axis = placement.local_x_in_parent
        y_axis = placement.local_y_in_parent
        z_axis = placement.local_z_in_parent
        return (
            "LocalToParentPlacement("
            f"Point3D{origin!r}, "
            "AxisBasis("
            f"AxisDirection{x_axis!r}, "
            f"AxisDirection{y_axis!r}, "
            f"AxisDirection{z_axis!r}"
            ")"
            ")"
        )

    def _points(self, points: tuple[BoundaryPoint, ...]) -> str:
        if not points:
            return "()"
        values = ", ".join(
            f"BoundaryPoint({point.x_mm!r}, {point.height_mm!r})"
            for point in points
        )
        suffix = "," if len(points) == 1 else ""
        return f"({values}{suffix})"


__all__ = ["PartSpecSourceRenderer"]
