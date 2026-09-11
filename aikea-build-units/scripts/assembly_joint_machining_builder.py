"""Scope: Resolve all supported assembly joints into local part cuts."""

from __future__ import annotations

from typing import Any

from local_to_parent_location import LocalToParentLocation
from cabineo_joint import CabineoJoint
from equal_thickness_miter_joint import EqualThicknessMiterJoint
from part_cut import AssemblyCuts
from part_construction_error import PartConstructionError


class AssemblyJointMachiningBuilder:
    """Dispatch each physical joint to its deterministic machining builder."""

    def __init__(self, strict: bool = False, allow_unresolved: bool = False) -> None:
        self.locations = LocalToParentLocation()
        self.strict = strict
        self.allow_unresolved = allow_unresolved
        self._joint_builders = {
            "cabineo": self._build_cabineo,
            "equal_thickness_miter": self._build_equal_thickness_miter,
        }

    def build(self, assembly: Any, joints: tuple[Any, ...]) -> AssemblyCuts:
        cuts = []
        for joint in joints:
            if self.allow_unresolved and joint.joint_type == "unresolved":
                continue
            builder = self._joint_builders.get(joint.joint_type)
            if builder is not None:
                cuts.extend(builder(assembly, joint))
            elif self.strict:
                raise PartConstructionError(
                    f"{joint.joint_id}: no machining tool for joint type {joint.joint_type}"
                )
        return AssemblyCuts(tuple(cuts))

    def _build_cabineo(self, assembly: Any, joint: Any) -> tuple[Any, ...]:
        source = assembly.part(joint.source_part_id)
        target = assembly.part(joint.target_part_id)
        source_location = self.locations.build(source.local_to_parent)
        target_location = self.locations.build(target.local_to_parent)
        return CabineoJoint().build(
            joint,
            source,
            target,
            source_location,
            target_location,
        )

    def _build_equal_thickness_miter(
        self, assembly: Any, joint: Any
    ) -> tuple[Any, ...]:
        part_a = assembly.part(joint.participant_ids[0])
        part_b = assembly.part(joint.participant_ids[1])
        location_a = self.locations.build(part_a.local_to_parent)
        location_b = self.locations.build(part_b.local_to_parent)
        return EqualThicknessMiterJoint().build(
            joint,
            part_a,
            part_b,
            location_a,
            location_b,
        )


__all__ = ["AssemblyJointMachiningBuilder"]
