"""Scope: Export the complete generated cabinet run on its structural base."""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Any

from assembly_run import AssemblyRunReader
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from base_mockup_geometry import BaseMockupGeometry
from cabinet_review_addition import CabinetReviewAddition
from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from full_wardrobe_door_plan import FullWardrobeDoorPlan
from full_wardrobe_position_checker import FullWardrobePositionChecker
from full_wardrobe_review import FullWardrobeReviewResult
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from unit_mockup import UnitMockupInputError
from wardrobe_addition_review_geometry import WardrobeAdditionReviewGeometry


class FullWardrobeReviewGenerator:
    """Build, position-check, and export all generated wardrobe assemblies."""

    _ROOT_ASSEMBLY_ID = "wardrobe_01"

    def __init__(self) -> None:
        self.run_reader = AssemblyRunReader()
        self.loader = GeneratedAssemblyBuilderLoader()
        self.base_geometry = BaseMockupGeometry()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.position_checker = FullWardrobePositionChecker()
        self.tree_geometry = AssemblyTreeReviewGeometry()
        self.hardware = PurchasedHardwareHydrator(
            ProjectHardwareGeometryResolver()
        )
        self.addition_geometry = WardrobeAdditionReviewGeometry()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
        door_plan: FullWardrobeDoorPlan | None = None,
        additions: tuple[CabinetReviewAddition, ...] = (),
        output_filename: str | None = None,
    ) -> FullWardrobeReviewResult:
        run = self.run_reader.read(project)
        assembly_ids = tuple(item.assembly_id for item in run.assemblies)
        resolved_door_plan = door_plan or FullWardrobeDoorPlan.uniform(
            DoorReviewState.CLOSED
        )
        unknown_assembly_ids = resolved_door_plan.unknown_assembly_ids(assembly_ids)
        if unknown_assembly_ids:
            raise UnitMockupInputError(
                ["unknown cabinet door states: " + ", ".join(unknown_assembly_ids)]
            )
        additions_by_id = {item.assembly_id: item for item in additions}
        unknown_additions = sorted(additions_by_id.keys() - set(assembly_ids))
        if len(additions_by_id) != len(additions) or unknown_additions:
            raise UnitMockupInputError(
                ["cabinet review additions must target unique saved assemblies"]
            )
        door_states = resolved_door_plan.states_for(assembly_ids)
        wardrobe = self.loader.load_assembly(project_root, self._ROOT_ASSEMBLY_ID)
        built_base, built_cabinets = self._children(wardrobe, assembly_ids)
        base_parts = self.base_geometry.build(built_base)
        physical_cabinet_parts = tuple(
            self.cabinet_geometry.build(built, DoorReviewState.CLOSED)
            + self._addition_parts(additions_by_id, built.spec.assembly_id, True)
            for built in built_cabinets
        )
        report = self.position_checker.check(
            built_base,
            base_parts,
            built_cabinets,
            physical_cabinet_parts,
        )
        report_path = project_root / "assemblies/full-wardrobe-position-check.json"
        report.write(report_path)
        if not report.is_valid:
            raise UnitMockupInputError(
                [
                    "full wardrobe position check failed: "
                    + ", ".join(report.failed_check_names())
                ]
            )
        if additions:
            placed_parts = self.addition_geometry.build(
                built_base,
                built_cabinets,
                door_states,
                additions_by_id,
            )
        else:
            hydrated = self.hardware.hydrate(project_root, wardrobe)
            visits = self.loader.walk(project_root, hydrated)
            placed_parts = self.tree_geometry.build(visits, door_states)
        filename = output_filename or resolved_door_plan.filename_for(assembly_ids)
        glb_path = project_root / f"assemblies/{filename}"
        self.exporter.export("full_wardrobe", placed_parts, glb_path)
        return FullWardrobeReviewResult(
            tuple(built.spec.assembly_id for built in built_cabinets),
            glb_path,
            report_path,
            MappingProxyType(
                {
                    assembly_id: door_states[assembly_id].value
                    for assembly_id in assembly_ids
                }
            ),
        )

    def _children(
        self,
        wardrobe: Any,
        expected_cabinet_ids: tuple[str, ...],
    ) -> tuple[Any, tuple[Any, ...]]:
        children = tuple(child.assembly for child in wardrobe.child_assemblies)
        child_ids = tuple(child.spec.assembly_id for child in children)
        if not children or child_ids != ("base_01", *expected_cabinet_ids):
            raise UnitMockupInputError(
                ["wardrobe root children do not match the saved assembly run"]
            )
        return children[0], children[1:]

    def _addition_parts(
        self,
        additions: dict[str, CabinetReviewAddition],
        assembly_id: str,
        physical: bool,
    ) -> tuple[Any, ...]:
        addition = additions.get(assembly_id)
        if addition is None:
            return ()
        return addition.physical_parts if physical else addition.review_parts


__all__ = ["FullWardrobeReviewGenerator"]
