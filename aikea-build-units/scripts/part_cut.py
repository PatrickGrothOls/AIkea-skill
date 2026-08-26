"""Scope: Carry resolved local cut geometry to its owning generated part."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class PartCut:
    """Identify one cutter in one part's canonical local frame."""

    joint_id: str
    part_id: str
    connector_index: int
    cutter: cq.Shape
    location: cq.Location


@dataclass(frozen=True)
class AssemblyCuts:
    """Group every resolved cut owned by one assembly."""

    all: tuple[PartCut, ...]

    def for_part(self, part_id: str) -> tuple[PartCut, ...]:
        return tuple(cut for cut in self.all if cut.part_id == part_id)


__all__ = ["AssemblyCuts", "PartCut"]
