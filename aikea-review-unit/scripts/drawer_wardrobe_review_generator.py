"""Scope: Export one built drawer child close-up and in its existing wardrobe."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from drawer_assembly_review_plan import DrawerAssemblyReviewPlanBuilder
from drawer_cabinet_position_checker import DrawerCabinetPositionChecker
from drawer_hardware_review import DrawerHardwareReviewBuilder
from drawer_review_geometry import DrawerReviewGeometry
from drawer_review_state import DrawerReviewState
from drawer_wardrobe_review import DrawerWardrobeReviewResult
from drawer_wardrobe_review_paths import DrawerWardrobeReviewPaths
from full_wardrobe_door_plan import FullWardrobeDoorPlan
from full_wardrobe_review_generator import FullWardrobeReviewGenerator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from unit_mockup import UnitMockupInputError


class DrawerWardrobeReviewGenerator:
    """Consume a cabinet-owned drawer child in local and global review views."""

    _COMPOSED_BUILDER_MODULE = "with_drawers_builder"

    def __init__(
        self,
        hardware_review_builder: DrawerHardwareReviewBuilder | None = None,
    ) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.drawer_geometry = DrawerReviewGeometry()
        self.hardware_review = hardware_review_builder or DrawerHardwareReviewBuilder()
        self.review_plan = DrawerAssemblyReviewPlanBuilder()
        self.position_checker = DrawerCabinetPositionChecker()
        self.full_wardrobe = FullWardrobeReviewGenerator()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
        assembly_id: str,
        hardware_directory: Path,
        drawer_state: DrawerReviewState = DrawerReviewState.OPEN,
    ) -> DrawerWardrobeReviewResult:
        paths = DrawerWardrobeReviewPaths.build(
            project_root,
            assembly_id,
            drawer_state,
        )
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
        self._write_valid_report(report, paths.drawer_position_report, "drawer position")

        hardware = self.hardware_review.build(
            built_cabinet,
            cabinet_physical,
            drawer_physical,
            hardware_directory,
            drawer_state,
        )
        for checked_report, path, label in (
            (
                hardware.position_report,
                paths.hardware_position_report,
                "drawer hardware position",
            ),
            (
                hardware.movement_report,
                paths.runner_movement_report,
                "drawer runner movement",
            ),
        ):
            self._write_valid_report(checked_report, path, label)

        drawer_review = self.drawer_geometry.build(built_cabinet, drawer_state)
        cabinet_review = self.cabinet_geometry.build(
            built_cabinet,
            DoorReviewState.REMOVED,
        )
        self.exporter.export(
            f"{assembly_id}_drawer_review",
            cabinet_review + hardware.review_parts + drawer_review,
            paths.closeup_glb,
        )
        review_plan = self.review_plan.build(
            built_cabinet,
            drawer_state,
            hardware.review_parts,
        )
        door_plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            (f"{assembly_id}=removed",),
        )
        full_result = self.full_wardrobe.generate(
            project_root,
            project,
            door_plan,
            review_plan,
            paths.full_wardrobe_filename,
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
                "review_only_runner_movement"
                if drawer_state is DrawerReviewState.OPEN
                else "source_cad_mounted_and_position_checked"
            ),
            closeup_glb_path=paths.closeup_glb,
            full_wardrobe_glb_path=full_result.glb_path,
            drawer_position_report_path=paths.drawer_position_report,
            hardware_position_report_path=paths.hardware_position_report,
            runner_movement_report_path=paths.runner_movement_report,
            full_position_report_path=full_result.position_report_path,
        )

    def _write_valid_report(self, report, path, label: str) -> None:
        report.write(path)
        if not report.is_valid:
            raise UnitMockupInputError(
                [f"{label} check failed: " + ", ".join(report.failed_check_names())]
            )


__all__ = ["DrawerWardrobeReviewGenerator"]
