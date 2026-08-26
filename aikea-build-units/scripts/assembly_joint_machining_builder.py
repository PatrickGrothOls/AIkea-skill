"""Scope: Resolve all supported assembly joints into local part cuts."""

from __future__ import annotations

from typing import Any

from assembly_part_locator import AssemblyPartLocator
from cabineo_joint import CabineoJoint
from part_cut import AssemblyCuts


class AssemblyJointMachiningBuilder:
    """Dispatch each physical joint to its deterministic machining builder."""

    def __init__(self) -> None:
        self.locator = AssemblyPartLocator()
        self._joint_builders = {"cabineo": self._build_cabineo}

    def build(self, assembly: Any, joints: tuple[Any, ...]) -> AssemblyCuts:
        cuts = []
        for joint in joints:
            builder = self._joint_builders.get(joint.joint_type)
            if builder is not None:
                cuts.extend(builder(assembly, joint))
        return AssemblyCuts(tuple(cuts))

    def _build_cabineo(self, assembly: Any, joint: Any) -> tuple[Any, ...]:
        source = assembly.part(joint.source_part_id)
        target = assembly.part(joint.target_part_id)
        source_location = self.locator.locate(
            source,
            assembly,
            float(assembly.base_height_mm),
        )
        target_location = self.locator.locate(
            target,
            assembly,
            float(assembly.base_height_mm),
        )
        return CabineoJoint().build(
            joint,
            source,
            target,
            source_location,
            target_location,
        )


__all__ = ["AssemblyJointMachiningBuilder"]
