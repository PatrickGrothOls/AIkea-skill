"""Scope: Preserve fabrication expectations derived from one closed assembly tree."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class FabricationPartEvidence:
    """Bind one full tree path to its built local solid and declared machining."""

    path: str
    part: Any
    joint_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FabricationHardwareEvidence:
    """Bind one full tree path to an exact purchased-hardware declaration."""

    path: str
    hardware: Any


@dataclass(frozen=True, slots=True)
class FabricationTreeEvidence:
    """Carry the physical expectations used by every fabrication-pack check."""

    parts: tuple[FabricationPartEvidence, ...]
    hardware: tuple[FabricationHardwareEvidence, ...]
    root_child_ids: tuple[str, ...]


class FabricationTreeEvidenceBuilder:
    """Derive path-stable expectations without furniture-feature branches."""

    def build(self, visits: tuple[Any, ...]) -> FabricationTreeEvidence:
        assemblies = {
            item.path: item.assembly
            for item in visits
            if type(item).__name__ == "AssemblyTreeAssembly"
        }
        parts = tuple(
            FabricationPartEvidence(
                self._path(item.path),
                item.part,
                self._joint_ids(assemblies[item.path[:-1]], item.part),
            )
            for item in visits
            if type(item).__name__ == "AssemblyTreePart"
        )
        hardware = tuple(
            FabricationHardwareEvidence(self._path(item.path), item.hardware)
            for item in visits
            if type(item).__name__ == "AssemblyTreeHardware"
        )
        root_child_ids = tuple(
            item.path[-1]
            for item in visits
            if type(item).__name__ == "AssemblyTreeAssembly" and len(item.path) == 2
        )
        return FabricationTreeEvidence(parts, hardware, root_child_ids)

    def _joint_ids(self, assembly: Any, part: Any) -> tuple[str, ...]:
        part_id = part.spec.part_id
        return tuple(
            sorted(
                {
                    cut.joint_id
                    for cut in assembly.cuts
                    if getattr(cut, "part_id", None) == part_id
                }
            )
        )

    def _path(self, path: tuple[str, ...]) -> str:
        return "/".join(segment.split(":", 1)[-1] for segment in path)


__all__ = [
    "FabricationHardwareEvidence",
    "FabricationPartEvidence",
    "FabricationTreeEvidence",
    "FabricationTreeEvidenceBuilder",
]
