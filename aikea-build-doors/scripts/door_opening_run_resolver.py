"""Scope: Resolve and persist the opening side for every door in one cabinet run."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from door_opening_preference_reader import DoorOpeningPreferenceReader
from door_opening_side_resolver import DoorOpeningSidePlan, DoorOpeningSideResolver
from generated_assembly_spec_loader import GeneratedAssemblySpecLoader


@dataclass(frozen=True, slots=True)
class DoorOpeningRunPlan:
    """Carry every resolved leaf while the first cabinet remains the visual proof."""

    plans: tuple[DoorOpeningSidePlan, ...]

    @property
    def has_doors(self) -> bool:
        return bool(self.plans)

    @property
    def failure_reason(self) -> str:
        if not self.plans:
            return "the selected run has no fitted single doors"
        return ""

    def for_assembly(self, assembly_id: str) -> DoorOpeningSidePlan:
        matches = tuple(plan for plan in self.plans if plan.assembly_id == assembly_id)
        if not matches:
            raise ValueError(f"{assembly_id} has no fitted single door")
        return matches[0]

    def write_local_plans(self, project_root: Path) -> None:
        for plan in self.plans:
            plan.write(
                project_root
                / "assemblies"
                / plan.assembly_id
                / "door_hinges"
                / "opening-plan.json"
            )


class DoorOpeningRunResolver:
    """Resolve every generated single door without building later cabinets."""

    def __init__(self) -> None:
        self.specs = GeneratedAssemblySpecLoader()
        self.side = DoorOpeningSideResolver()
        self.preferences = DoorOpeningPreferenceReader()

    def resolve(
        self,
        project_root: Path,
        project: dict[str, Any],
        run: Any,
    ) -> DoorOpeningRunPlan:
        specifications = tuple(
            self.specs.load(project_root, item.assembly_id) for item in run.assemblies
        )
        door_specifications = tuple(
            specification
            for specification in specifications
            if any(part.part_id == "door_panel" for part in specification.parts)
        )
        assembly_ids = tuple(
            specification.assembly_id for specification in door_specifications
        )
        preferences = self.preferences.read(project, assembly_ids)
        return DoorOpeningRunPlan(
            tuple(
                self.side.resolve(
                    specification,
                    preferences.get(specification.assembly_id),
                )
                for specification in door_specifications
            )
        )


__all__ = ["DoorOpeningRunPlan", "DoorOpeningRunResolver"]
