"""Scope: Export one built drawer child close-up and in its existing wardrobe."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cabinet_review_addition import CabinetReviewAddition
from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from drawer_cabinet_position_checker import DrawerCabinetPositionChecker
from drawer_review_geometry import DrawerReviewGeometry
from drawer_review_state import DrawerReviewState
from drawer_wardrobe_review import DrawerWardrobeReviewResult
from fixed_runner_mounting_zone_review_geometry import (
    FixedRunnerMountingZoneReviewGeometry,
)
from full_wardrobe_door_plan import FullWardrobeDoorPlan
from full_wardrobe_review_generator import FullWardrobeReviewGenerator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from unit_mockup import UnitMockupInputError


class DrawerWardrobeReviewGenerator:
    """Consume a cabinet-owned drawer child in local and global review views."""

    _COMPOSED_BUILDER_MODULE = "with_drawers_builder"

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.drawer_geometry = DrawerReviewGeometry()
        self.runner_mounting_zones = FixedRunnerMountingZoneReviewGeometry()
        self.position_checker = DrawerCabinetPositionChecker()
        self.full_wardrobe = FullWardrobeReviewGenerator()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
        assembly_id: str,
        drawer_state: DrawerReviewState = DrawerReviewState.OPEN,
    ) -> DrawerWardrobeReviewResult:
        built_cabinet = self.loader.load_assembly(
            project_root,
            assembly_id,
            self._COMPOSED_BUILDER_MODULE,
        )
        cabinet_physical = self.cabinet_geometry.build(
            built_cabinet,
            DoorReviewState.CLOSED,
        )
        drawer_physical = self.drawer_geometry.build(
            built_cabinet,
            DrawerReviewState.CLOSED,
        )
        report = self.position_checker.check(
            built_cabinet,
            cabinet_physical,
            drawer_physical,
        )
        report_path = (
            project_root
            / "assemblies"
            / assembly_id
            / "drawer-position-check.json"
        )
        report.write(report_path)
        if not report.is_valid:
            raise UnitMockupInputError(
                [
                    "drawer position check failed: "
                    + ", ".join(report.failed_check_names())
                ]
            )

        drawer_review = self.drawer_geometry.build(built_cabinet, drawer_state)
        runner_review = (
            self.runner_mounting_zones.build(built_cabinet)
            if drawer_state is DrawerReviewState.REMOVED
            else ()
        )
        cabinet_review = self.cabinet_geometry.build(
            built_cabinet,
            DoorReviewState.REMOVED,
        )
        closeup_path = (
            project_root
            / "assemblies"
            / assembly_id
            / f"{assembly_id}_drawer_{drawer_state.value}_review.glb"
        )
        self.exporter.export(
            f"{assembly_id}_drawer_review",
            cabinet_review + runner_review + drawer_review,
            closeup_path,
        )
        addition = CabinetReviewAddition(
            assembly_id,
            drawer_physical,
            runner_review + drawer_review,
        )
        door_plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            (f"{assembly_id}=removed",),
        )
        full_result = self.full_wardrobe.generate(
            project_root,
            project,
            door_plan,
            (addition,),
            f"full_wardrobe_{assembly_id}_drawer_{drawer_state.value}_review.glb",
        )
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        return DrawerWardrobeReviewResult(
            assembly_id=assembly_id,
            drawer_id=child.spec.assembly_id,
            drawer_state=drawer_state.value,
            runner_product_code=child.assembly.spec.runner_product_code,
            runner_review_representation=(
                "mounting_zones_only_source_cad_verified_unplaced"
                if drawer_state is DrawerReviewState.REMOVED
                else "source_cad_verified_unplaced"
            ),
            closeup_glb_path=closeup_path,
            full_wardrobe_glb_path=full_result.glb_path,
            drawer_position_report_path=report_path,
            full_position_report_path=full_result.position_report_path,
        )


__all__ = ["DrawerWardrobeReviewGenerator"]
