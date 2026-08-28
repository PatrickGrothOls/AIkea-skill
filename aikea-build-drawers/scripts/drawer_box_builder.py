"""Scope: Build and place one unmachined five-part wooden drawer box."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from blank_sheet_builder import BlankSheetBuilder
from drawer_box_spec import DrawerBoxSpec, DrawerPartSpec
from drawer_part_locator import DrawerPartLocator, DrawerPartPlacement


@dataclass(frozen=True, slots=True)
class BuiltDrawerPart:
    """Keep a sheet local while carrying its explicit drawer placement."""

    spec: DrawerPartSpec
    solid: Any
    placement: DrawerPartPlacement

    def placed_shape(self) -> Any:
        return self.solid.val().located(self.placement.location())


@dataclass(frozen=True, slots=True)
class BuiltDrawerBox:
    """Hold one resolved drawer specification and its five built sheets."""

    spec: DrawerBoxSpec
    parts: tuple[BuiltDrawerPart, ...]

    def part(self, part_id: str) -> BuiltDrawerPart:
        return next(part for part in self.parts if part.spec.part_id == part_id)


class DrawerBoxBuilder:
    """Construct every drawer part through the shared BlankSheetBuilder."""

    def __init__(self) -> None:
        self.locator = DrawerPartLocator()

    def build(self, drawer: DrawerBoxSpec) -> BuiltDrawerBox:
        parts = tuple(self._build_part(part, drawer) for part in drawer.parts)
        return BuiltDrawerBox(spec=drawer, parts=parts)

    def _build_part(
        self,
        part: DrawerPartSpec,
        drawer: DrawerBoxSpec,
    ) -> BuiltDrawerPart:
        blank = BlankSheetBuilder.rectangle(*part.local_size_mm).build()
        return BuiltDrawerPart(
            spec=part,
            solid=blank,
            placement=self.locator.placement(part.part_id, drawer),
        )


__all__ = ["BuiltDrawerBox", "BuiltDrawerPart", "DrawerBoxBuilder"]
