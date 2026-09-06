"""Scope: Check recursive built geometry, frames, joints, and joint machining."""

from __future__ import annotations

from typing import Any

from fabrication_readiness_report import FabricationReadinessCheck


class AssemblyFabricationChecker:
    """Inspect arbitrary assembly depth without knowing furniture feature types."""

    _VOLUME_TOLERANCE_MM3 = 1e-6

    def check(self, visits: tuple[Any, ...]) -> tuple[FabricationReadinessCheck, ...]:
        parts = tuple(
            item for item in visits if type(item).__name__ == "AssemblyTreePart"
        )
        hardware = tuple(
            item for item in visits if type(item).__name__ == "AssemblyTreeHardware"
        )
        assemblies = tuple(
            item for item in visits if type(item).__name__ == "AssemblyTreeAssembly"
        )
        return (
            self._geometry(parts),
            self._placements(parts, hardware),
            self._hardware(hardware),
            self._joints(assemblies),
            self._joint_machining(assemblies),
        )

    def _geometry(self, parts) -> FabricationReadinessCheck:
        missing = tuple(
            self.path(item.path)
            for item in parts
            if item.part.solid.val().Volume() <= self._VOLUME_TOLERANCE_MM3
        )
        return self._check("tree.manufactured_geometry", missing)

    def _placements(self, parts, hardware) -> FabricationReadinessCheck:
        missing = tuple(
            self.path(item.path)
            for item in (*parts, *hardware)
            if item.local_to_root is None
        )
        return self._check("tree.explicit_placements", missing)

    def _hardware(self, hardware) -> FabricationReadinessCheck:
        missing = tuple(
            self.path(item.path)
            for item in hardware
            if not item.hardware.has_geometry
        )
        return self._check("tree.exact_hardware_geometry", missing)

    def _joints(self, assemblies) -> FabricationReadinessCheck:
        problems = []
        for item in assemblies:
            assembly = item.assembly
            if len(assembly.parts) > 1 and not assembly.joints:
                problems.append(self.path(item.path) + ": no declared joints")
            problems.extend(
                self.path(item.path) + f": unresolved joint {joint.joint_id}"
                for joint in assembly.joints
                if getattr(joint, "joint_type", "unresolved") == "unresolved"
            )
        return self._check("tree.resolved_joints", tuple(problems))

    def _joint_machining(self, assemblies) -> FabricationReadinessCheck:
        problems = []
        for item in assemblies:
            cut_joint_ids = {
                cut.joint_id for cut in item.assembly.cuts if hasattr(cut, "joint_id")
            }
            problems.extend(
                self.path(item.path) + f": no machining for {joint.joint_id}"
                for joint in item.assembly.joints
                if getattr(joint, "joint_type", "unresolved") != "unresolved"
                and joint.joint_id not in cut_joint_ids
            )
        return self._check("tree.joint_machining", tuple(problems))

    def path(self, path: tuple[str, ...]) -> str:
        return "/".join(segment.split(":", 1)[-1] for segment in path)

    def _check(self, code: str, problems: tuple[str, ...]) -> FabricationReadinessCheck:
        return FabricationReadinessCheck(code, not problems, problems)


__all__ = ["AssemblyFabricationChecker"]
