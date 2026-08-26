"""Scope: Derive tall-storage parts and physical joint ownership from a local boundary."""

from __future__ import annotations

from math import hypot

from assembly_taxonomy import (
    BoundaryPoint,
    CabineoJointTaxonomy,
    JointTaxonomy,
    PartTaxonomy,
)
from tall_storage_joint_taxonomy import TallStorageJointTaxonomy
from top_boundary_panel_outline_builder import TopBoundaryPanelOutlineBuilder


class TallStorageTaxonomy:
    """Create the manufactured-part taxonomy for one full-height storage unit."""

    def __init__(self) -> None:
        self.outline_builder = TopBoundaryPanelOutlineBuilder()
        self.joint_taxonomy = TallStorageJointTaxonomy()

    def build_parts(
        self,
        top: tuple[BoundaryPoint, ...],
        width_mm: float,
        depth_mm: float,
        door_width_mm: float,
        base_height_mm: float,
        panel_thickness_mm: float,
        door_thickness_mm: float,
        back_thickness_mm: float,
    ) -> tuple[PartTaxonomy, ...]:
        back_outline = self.outline_builder.build(top, 0.0, width_mm)
        door_inset_mm = (width_mm - door_width_mm) / 2.0
        door_outline = self.outline_builder.build(
            top,
            door_inset_mm,
            width_mm - door_inset_mm,
            base_height_mm,
        )
        parts = [
            PartTaxonomy(
                "left_side",
                "side_panel",
                self._dimensions(
                    height=top[0].height_mm,
                    depth=depth_mm,
                    thickness=panel_thickness_mm,
                ),
                local_size_mm=(depth_mm, top[0].height_mm, panel_thickness_mm),
                inside_face=">Z",
            ),
            PartTaxonomy(
                "right_side",
                "side_panel",
                self._dimensions(
                    height=top[-1].height_mm,
                    depth=depth_mm,
                    thickness=panel_thickness_mm,
                ),
                local_size_mm=(depth_mm, top[-1].height_mm, panel_thickness_mm),
                inside_face=">Z",
            ),
            PartTaxonomy(
                "back_panel",
                "back_panel",
                self._dimensions(width=width_mm, thickness=back_thickness_mm),
                back_outline,
                (width_mm, max(point.height_mm for point in back_outline), back_thickness_mm),
                ">Z",
            ),
            PartTaxonomy(
                "door_panel",
                "door_panel",
                self._dimensions(
                    width=door_width_mm,
                    left_height=door_outline[-1].height_mm,
                    right_height=door_outline[2].height_mm,
                    thickness=door_thickness_mm,
                ),
                door_outline,
                (
                    door_width_mm,
                    max(point.height_mm for point in door_outline),
                    door_thickness_mm,
                ),
                "<Z",
            ),
        ]
        parts.extend(
            self._top_panel(index, left, right, depth_mm, panel_thickness_mm)
            for index, (left, right) in enumerate(zip(top, top[1:]), start=1)
        )
        return tuple(parts)

    def build_joints(
        self, top_panel_count: int
    ) -> tuple[JointTaxonomy | CabineoJointTaxonomy, ...]:
        return self.joint_taxonomy.build(top_panel_count)

    def _top_panel(
        self,
        index: int,
        left: BoundaryPoint,
        right: BoundaryPoint,
        depth_mm: float,
        thickness_mm: float,
    ) -> PartTaxonomy:
        return PartTaxonomy(
            f"top_panel_{index:02d}",
            "top_panel",
            self._dimensions(
                start_x=left.x_mm,
                end_x=right.x_mm,
                start_height=left.height_mm,
                end_height=right.height_mm,
                length=hypot(right.x_mm - left.x_mm, right.height_mm - left.height_mm),
                depth=depth_mm,
                thickness=thickness_mm,
            ),
            local_size_mm=(
                hypot(right.x_mm - left.x_mm, right.height_mm - left.height_mm),
                depth_mm,
                thickness_mm,
            ),
            inside_face="<Z",
        )

    def _dimensions(self, **values: float) -> tuple[tuple[str, float], ...]:
        return tuple((name, value) for name, value in values.items())
