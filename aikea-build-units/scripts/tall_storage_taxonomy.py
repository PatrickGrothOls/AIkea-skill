"""Scope: Derive tall-storage parts and physical joint ownership from a local boundary."""

from __future__ import annotations

from assembly_taxonomy import (
    BoundaryPoint,
    CabineoJointTaxonomy,
    JointTaxonomy,
    PartTaxonomy,
)
from adjustable_shelf_taxonomy_builder import AdjustableShelfTaxonomyBuilder
from side_panel_height_resolver import SidePanelHeightResolver
from tall_storage_joint_taxonomy import TallStorageJointTaxonomy
from top_panel_taxonomy_builder import TopPanelTaxonomyBuilder
from top_boundary_panel_outline_builder import TopBoundaryPanelOutlineBuilder


class TallStorageTaxonomy:
    """Create the manufactured-part taxonomy for one full-height storage unit."""

    def __init__(self) -> None:
        self.outline_builder = TopBoundaryPanelOutlineBuilder()
        self.joint_taxonomy = TallStorageJointTaxonomy()
        self.side_panel_height_resolver = SidePanelHeightResolver()
        self.shelf_builder = AdjustableShelfTaxonomyBuilder()
        self.top_panel_builder = TopPanelTaxonomyBuilder()

    def build_parts(
        self,
        top: tuple[BoundaryPoint, ...],
        width_mm: float,
        carcass_panel_depth_mm: float,
        door_width_mm: float,
        base_height_mm: float,
        door_bottom_mm: float,
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
            base_height_mm - door_bottom_mm,
        )
        left_side_height_mm = self.side_panel_height_resolver.resolve_left(
            top,
            panel_thickness_mm,
        )
        right_side_height_mm = self.side_panel_height_resolver.resolve_right(
            top,
            panel_thickness_mm,
        )
        parts = [
            PartTaxonomy(
                "left_side",
                "side_panel",
                self._dimensions(
                    height=left_side_height_mm,
                    depth=carcass_panel_depth_mm,
                    thickness=panel_thickness_mm,
                ),
                local_size_mm=(
                    carcass_panel_depth_mm,
                    left_side_height_mm,
                    panel_thickness_mm,
                ),
                inside_face=">Z",
            ),
            PartTaxonomy(
                "right_side",
                "side_panel",
                self._dimensions(
                    height=right_side_height_mm,
                    depth=carcass_panel_depth_mm,
                    thickness=panel_thickness_mm,
                ),
                local_size_mm=(
                    carcass_panel_depth_mm,
                    right_side_height_mm,
                    panel_thickness_mm,
                ),
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
            self.shelf_builder.build(
                width_mm,
                carcass_panel_depth_mm,
                left_side_height_mm,
                right_side_height_mm,
                panel_thickness_mm,
            )
        )
        parts.extend(
            self.top_panel_builder.build(
                top,
                carcass_panel_depth_mm,
                panel_thickness_mm,
            )
        )
        return tuple(parts)

    def build_joints(
        self, top: tuple[BoundaryPoint, ...]
    ) -> tuple[JointTaxonomy | CabineoJointTaxonomy, ...]:
        return self.joint_taxonomy.build(top)

    def _dimensions(self, **values: float) -> tuple[tuple[str, float], ...]:
        return tuple((name, value) for name, value in values.items())
