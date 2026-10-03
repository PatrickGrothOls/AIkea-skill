"""Scope: Derive the complete connection graph for one tall-storage unit."""

from __future__ import annotations

from math import isclose

from assembly_taxonomy import BoundaryPoint, CabineoJointTaxonomy, JointTaxonomy


class TallStorageJointTaxonomy:
    """Describe how every generated tall-storage part connects."""

    def build(
        self,
        top: tuple[BoundaryPoint, ...],
    ) -> tuple[JointTaxonomy | CabineoJointTaxonomy, ...]:
        top_ids = tuple(
            f"top_panel_{index:02d}"
            for index in range(1, len(top))
        )
        joints = [
            CabineoJointTaxonomy(
                "left_side_to_back_panel",
                "left_side",
                "back_panel",
                ">Z",
                ">X",
                "bounded_spacing",
            ),
            CabineoJointTaxonomy(
                "right_side_to_back_panel",
                "right_side",
                "back_panel",
                ">Z",
                "<X",
                "bounded_spacing",
            ),
            JointTaxonomy(
                "door_panel_to_left_side",
                ("door_panel", "left_side"),
                "door_hinge",
            ),
            self._side_top_joint(
                "left_side_to_top",
                top_ids[0],
                "left_side",
                top[0],
                top[1],
            ),
            self._side_top_joint(
                "right_side_to_top",
                top_ids[-1],
                "right_side",
                top[-2],
                top[-1],
            ),
        ]
        joints.extend(
            CabineoJointTaxonomy(
                f"{top_id}_to_back_panel",
                top_id,
                "back_panel",
                "<Z",
                ">Y",
                "bounded_spacing",
            )
            for top_id in top_ids
        )
        joints.extend(
            JointTaxonomy(
                f"{left_id}_to_{right_id}",
                (left_id, right_id),
                "top_boundary_seam",
                "equal_thickness_miter",
            )
            for left_id, right_id in zip(top_ids, top_ids[1:])
        )
        return tuple(joints)

    def _side_top_joint(
        self,
        joint_id: str,
        top_id: str,
        side_id: str,
        start: BoundaryPoint,
        end: BoundaryPoint,
    ) -> JointTaxonomy | CabineoJointTaxonomy:
        if isclose(start.height_mm, end.height_mm):
            return CabineoJointTaxonomy(
                joint_id,
                side_id,
                top_id,
                ">Z",
                ">Y",
                "bounded_spacing",
            )
        return JointTaxonomy(
            joint_id,
            (top_id, side_id),
            "angled_panel_seam",
            "equal_thickness_miter",
        )


__all__ = ["TallStorageJointTaxonomy"]
