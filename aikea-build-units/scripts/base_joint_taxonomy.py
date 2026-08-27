"""Scope: Define the physical relationships inside and between structural base modules."""

from __future__ import annotations

from assembly_taxonomy import CabineoJointTaxonomy, JointTaxonomy


class BaseJointTaxonomy:
    """Connect every brace and rail to its deck and retain each module seam."""

    def build_module(
        self,
        module_index: int,
        brace_count: int,
    ) -> tuple[JointTaxonomy | CabineoJointTaxonomy, ...]:
        suffix = f"{module_index:02d}"
        deck_id = f"deck_{suffix}"
        front_id = f"front_rail_{suffix}"
        back_id = f"back_rail_{suffix}"
        joints: list[JointTaxonomy | CabineoJointTaxonomy] = [
            JointTaxonomy(
                f"{deck_id}_to_front_rail",
                (deck_id, front_id),
                "base_deck_support",
            ),
            JointTaxonomy(
                f"{deck_id}_to_back_rail",
                (deck_id, back_id),
                "base_deck_support",
            ),
        ]
        for brace_index in range(1, brace_count + 1):
            brace_id = f"brace_{suffix}_{brace_index:02d}"
            joints.extend(
                (
                    CabineoJointTaxonomy(
                        joint_id=f"{brace_id}_to_front_rail",
                        source_part_id=brace_id,
                        target_part_id=front_id,
                        source_face=">Z",
                        source_edge="<X",
                        connector_layout="bounded_spacing",
                        purpose="base_frame_corner",
                    ),
                    CabineoJointTaxonomy(
                        joint_id=f"{brace_id}_to_back_rail",
                        source_part_id=brace_id,
                        target_part_id=back_id,
                        source_face=">Z",
                        source_edge=">X",
                        connector_layout="bounded_spacing",
                        purpose="base_frame_corner",
                    ),
                    JointTaxonomy(
                        f"{deck_id}_to_{brace_id}",
                        (deck_id, brace_id),
                        "base_deck_support",
                    ),
                )
            )
        return tuple(joints)

    def build_module_seams(self, module_count: int) -> tuple[JointTaxonomy, ...]:
        return tuple(
            JointTaxonomy(
                f"base_module_{index:02d}_to_{index + 1:02d}",
                (
                    f"deck_{index:02d}",
                    f"deck_{index + 1:02d}",
                    f"front_rail_{index:02d}",
                    f"front_rail_{index + 1:02d}",
                    f"back_rail_{index:02d}",
                    f"back_rail_{index + 1:02d}",
                ),
                "base_module_seam",
            )
            for index in range(1, module_count)
        )


__all__ = ["BaseJointTaxonomy"]
