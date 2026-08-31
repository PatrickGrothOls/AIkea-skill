"""Scope: Turn one recursive assembly-tree walk into named review geometry."""

from __future__ import annotations

from typing import Any

from door_review_state import DoorReviewState
from local_to_parent_location import LocalToParentLocation
from review_part_locator import ReviewPartLocator
from unit_mockup import MockupPart, UnitMockupInputError


class AssemblyTreeReviewGeometry:
    """Render every built part and hardware item from accumulated tree frames."""

    _CARCASS = (0.78, 0.69, 0.55, 1.0)
    _BACK = (0.67, 0.58, 0.46, 1.0)
    _DOOR = (0.91, 0.86, 0.77, 1.0)
    _BASE_DECK = (0.82, 0.74, 0.61, 1.0)
    _BASE_FRAME = (0.67, 0.58, 0.46, 1.0)
    _HARDWARE = (0.48, 0.50, 0.52, 1.0)

    def __init__(self) -> None:
        self.locations = LocalToParentLocation()
        self.open_doors = ReviewPartLocator()

    def build(
        self,
        visits: tuple[Any, ...],
        door_states: dict[str, DoorReviewState],
    ) -> tuple[MockupPart, ...]:
        assemblies = {
            item.path: item
            for item in visits
            if type(item).__name__ == "AssemblyTreeAssembly"
        }
        rendered = []
        for item in visits:
            renderer = {
                "AssemblyTreePart": self._part,
                "AssemblyTreeHardware": self._hardware,
            }.get(type(item).__name__)
            if renderer:
                rendered.extend(renderer(item, assemblies, door_states))
        return tuple(rendered)

    def _part(self, item, assemblies, door_states) -> tuple[MockupPart, ...]:
        owner = assemblies[item.path[:-1]]
        part = item.part
        state = door_states.get(owner.assembly.spec.assembly_id)
        if part.spec.part_id == "door_panel" and state is DoorReviewState.REMOVED:
            return ()
        location = self.locations.build(item.local_to_root)
        if part.spec.part_id == "door_panel" and state is DoorReviewState.OPEN:
            owner_location = self.locations.build(owner.local_to_root)
            location = owner_location * self.open_doors.locate(
                part.spec,
                owner.assembly.spec,
                float(owner.assembly.spec.base_height_mm),
            )
        return (
            MockupPart(
                self._name(item.path),
                part.solid,
                location,
                self._part_color(part.spec.role),
            ),
        )

    def _hardware(self, item, _assemblies, _door_states) -> tuple[MockupPart, ...]:
        if not item.hardware.has_geometry or item.local_to_root is None:
            raise UnitMockupInputError(
                ["purchased hardware is missing exact placed geometry: " + self._name(item.path)]
            )
        return (
            MockupPart(
                self._name(item.path),
                item.hardware.solid,
                self.locations.build(item.local_to_root),
                self._HARDWARE,
            ),
        )

    def _name(self, path: tuple[str, ...]) -> str:
        return "__".join(segment.split(":", 1)[-1] for segment in path[1:])

    def _part_color(self, role: str) -> tuple[float, float, float, float]:
        return {
            "back_panel": self._BACK,
            "door_panel": self._DOOR,
            "base_deck": self._BASE_DECK,
            "base_rail": self._BASE_FRAME,
            "base_brace": self._BASE_FRAME,
        }.get(role, self._CARCASS)


__all__ = ["AssemblyTreeReviewGeometry"]
