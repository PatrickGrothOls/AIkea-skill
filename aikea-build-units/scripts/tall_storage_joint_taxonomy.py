"""Scope: Derive the complete connection graph for one tall-storage unit."""

from __future__ import annotations

from assembly_taxonomy import CabineoJointTaxonomy, JointTaxonomy


class TallStorageJointTaxonomy:
    """Describe how every generated tall-storage part connects."""

    def build(
        self, top_panel_count: int
    ) -> tuple[JointTaxonomy | CabineoJointTaxonomy, ...]:
        top_ids = tuple(
            f"top_panel_{index:02d}"
            for index in range(1, top_panel_count + 1)
        )
        joints = [
            JointTaxonomy(
                "left_side_to_back_panel",
                ("left_side", "back_panel"),
                "structural_seam",
            ),
            JointTaxonomy(
                "right_side_to_back_panel",
                ("right_side", "back_panel"),
                "structural_seam",
            ),
            JointTaxonomy(
                "door_panel_to_left_side",
                ("door_panel", "left_side"),
                "door_hinge",
            ),
            CabineoJointTaxonomy(
                "left_side_to_top",
                "left_side",
                top_ids[0],
                ">Z",
                ">Y",
                "two_quarter_points",
            ),
            JointTaxonomy(
                "right_side_to_top",
                ("right_side", top_ids[-1]),
                "structural_seam",
            ),
        ]
        joints.extend(
            JointTaxonomy(
                f"{top_id}_to_back_panel",
                (top_id, "back_panel"),
                "structural_seam",
            )
            for top_id in top_ids
        )
        joints.extend(
            JointTaxonomy(
                f"{left_id}_to_{right_id}",
                (left_id, right_id),
                "top_boundary_seam",
            )
            for left_id, right_id in zip(top_ids, top_ids[1:])
        )
        return tuple(joints)


__all__ = ["TallStorageJointTaxonomy"]
