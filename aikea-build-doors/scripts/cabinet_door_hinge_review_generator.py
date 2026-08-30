"""Scope: Generate one checked cabinet door with exact hinge hardware reviews."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from assembly_run import AssemblyRunReader
from assembly_run_overall_project_adapter import AssemblyRunOverallProjectAdapter
from cadquery_glb_exporter import CadQueryGlbExporter
from concealed_hinge_machining import ConcealedHingeMachining
from door_hinge_plan import DoorHingePlanner
from door_hinge_review_geometry import DoorHingeReviewGeometry
from door_hinge_review_report import DoorHingeReviewReport
from door_opening_review_record import DoorOpeningReviewRecord
from door_opening_run_resolver import DoorOpeningRunResolver
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from riex_nc70_hardware_loader import RiexNc70HardwareLoader
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from overall_wardrobe_inputs import OverallWardrobeInputReader
from panel_hardware_reservation import PanelHardwareReservationStore
from riex_nc70_hardware_reservations import RiexNc70HardwareReservations


@dataclass(frozen=True, slots=True)
class CabinetDoorHingeReviewResult:
    """Name every saved source and visual artifact from the proof."""

    assembly_id: str
    installation_path: Path
    opening_plan_path: Path
    opening_review_path: Path
    hardware_reservation_path: Path
    report_path: Path
    closed_glb_path: Path
    open_glb_path: Path
    fabrication_ready: bool
    compatibility_issues: tuple[str, ...]


class CabinetDoorHingeReviewGenerator:
    """Build panels once, then export the exact closed and open hardware states."""

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.assembly_run = AssemblyRunReader()
        self.overall_project = AssemblyRunOverallProjectAdapter()
        self.planner = DoorHingePlanner()
        self.opening_run = DoorOpeningRunResolver()
        self.opening_review = DoorOpeningReviewRecord()
        self.hardware_loader = RiexNc70HardwareLoader()
        self.machining = ConcealedHingeMachining()
        self.geometry = DoorHingeReviewGeometry()
        self.exporter = CadQueryGlbExporter()
        self.reservation_store = PanelHardwareReservationStore()
        self.hardware_reservations = RiexNc70HardwareReservations()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
        assembly_id: str,
        hardware_root: Path,
    ) -> CabinetDoorHingeReviewResult:
        built = self.loader.load_assembly(project_root, assembly_id)
        profile = RIEX_NC70_FULL_OVERLAY
        run = self.assembly_run.read(project)
        overall_project = self.overall_project.adapt(project, run)
        inputs = OverallWardrobeInputReader().read(overall_project)
        opening_run = self.opening_run.resolve(
            project_root,
            project,
            run,
            inputs,
            profile,
        )
        opening_run.write_local_plans(project_root)
        if not opening_run.passes:
            raise ValueError(opening_run.failure_reason)
        opening_plan = opening_run.for_assembly(assembly_id)
        source_directory = project_root / "assemblies" / assembly_id / "door_hinges"
        opening_plan_path = source_directory / "opening-plan.json"
        existing_reservations = tuple(
            item
            for item in self.reservation_store.load(project_root, assembly_id)
            if item.hardware_kind != "hinge_plate"
        )
        plan = self.planner.plan(
            built.spec,
            profile,
            opening_plan.proposed_side,
            existing_reservations,
        )
        hardware = self.hardware_loader.load(hardware_root)
        machined = self.machining.apply(built, plan, profile)
        installation_path = source_directory / "installation.json"
        plan.write(installation_path)
        side_dimensions = {
            name: float(value)
            for name, value in built.spec.part(plan.hinge_side.side_part_id).dimensions_mm
        }
        report = DoorHingeReviewReport.from_plan(
            plan,
            opening_plan,
            side_dimensions["thickness"],
            profile,
        )
        report_path = source_directory / "fit-check.json"
        report.write(report_path)
        opening_review_path = project_root / "reviews" / "door-openings.json"
        self.opening_review.write_proposal(opening_review_path, opening_run.plans)
        review_directory = source_directory / "review"
        review_directory.mkdir(parents=True, exist_ok=True)
        closed_path = review_directory / "door-hinges-closed.glb"
        open_path = review_directory / "door-hinges-open.glb"
        self.exporter.export(
            f"{assembly_id}_door_hinges_closed",
            self.geometry.build(built, machined, hardware, plan, profile, False),
            closed_path,
        )
        self.exporter.export(
            f"{assembly_id}_door_hinges_open",
            self.geometry.build(built, machined, hardware, plan, profile, True),
            open_path,
        )
        hardware_reservation_path = self.reservation_store.write(
            project_root,
            assembly_id,
            existing_reservations
            + self.hardware_reservations.from_plan(plan, profile),
        )
        return CabinetDoorHingeReviewResult(
            assembly_id=assembly_id,
            installation_path=installation_path,
            opening_plan_path=opening_plan_path,
            opening_review_path=opening_review_path,
            hardware_reservation_path=hardware_reservation_path,
            report_path=report_path,
            closed_glb_path=closed_path,
            open_glb_path=open_path,
            fabrication_ready=plan.fabrication_ready and opening_run.passes,
            compatibility_issues=plan.compatibility_issues
            + tuple(issue for check in opening_plan.checks for issue in check.issues),
        )


__all__ = ["CabinetDoorHingeReviewGenerator", "CabinetDoorHingeReviewResult"]
