"""Scope: Export three visual states of one exact KA 5332 drawer prototype."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from drawer_box_builder import DrawerBoxBuilder
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from drawer_review_state import DrawerReviewState
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_5332_drawer_box_profile import (
    HettichKa5332DrawerBoxProfileAdapter,
)
from hettich_ka_5332_connection_closeup import HettichKa5332ConnectionCloseup
from hettich_ka_5332_mounting_plan import HettichKa5332MountingPlanner
from hettich_ka_5332_review_geometry import HettichKa5332ReviewGeometry
from hettich_ka_5332_runner_profile import HETTICH_KA_5332_500
from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader


@dataclass(frozen=True, slots=True)
class HettichKa5332PrototypeResult:
    """Report review files and the two manufacturer planning checks."""

    closed_glb: Path
    open_glb: Path
    removed_glb: Path
    closed_connection_glb: Path
    open_connection_glb: Path
    removed_connection_glb: Path
    drawer_outside_width_mm: float
    recommended_width_met: bool
    minimum_depth_met: bool


class HettichKa5332PrototypeGenerator:
    """Reuse generated cabinet and drawer parts around the exact runner STEP."""

    def __init__(self) -> None:
        self.cabinet_loader = GeneratedAssemblyBuilderLoader()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.step_loader = HettichKa5332StepAssemblyLoader()
        self.mounting_planner = HettichKa5332MountingPlanner()
        self.box_profile = HettichKa5332DrawerBoxProfileAdapter()
        self.box_planner = DrawerBoxPlanner()
        self.box_builder = DrawerBoxBuilder()
        self.review_geometry = HettichKa5332ReviewGeometry()
        self.connection_closeup = HettichKa5332ConnectionCloseup()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        hardware_directory: Path,
        output_directory: Path,
        *,
        drawer_front_mm: float,
        drawer_bottom_mm: float,
    ) -> HettichKa5332PrototypeResult:
        cabinet = self.cabinet_loader.load_assembly(project_root, assembly_id)
        step = self.step_loader.load(hardware_directory)
        plan = self.mounting_planner.plan(
            cabinet.spec,
            step,
            HETTICH_KA_5332_500,
            drawer_front_mm=drawer_front_mm,
            drawer_bottom_mm=drawer_bottom_mm,
        )
        sizing = self.box_profile.build(
            HETTICH_KA_5332_500,
            side_thickness_mm=15.0,
            front_back_thickness_mm=15.0,
            bottom_thickness_mm=9.0,
            bottom_underside_recess_mm=13.0,
            box_height_mm=160.0,
        )
        box_spec = self.box_planner.plan(
            CabinetDrawerOpening.from_assembly_spec(cabinet.spec),
            sizing,
        )
        box = self.box_builder.build(box_spec)
        cabinet_parts = self.cabinet_geometry.build(
            cabinet,
            DoorReviewState.REMOVED,
        )
        output_directory.mkdir(parents=True, exist_ok=True)
        outputs = {
            state: output_directory / f"ka_5332_drawer_{state.value}.glb"
            for state in DrawerReviewState
        }
        connection_outputs = {
            state: output_directory / f"ka_5332_{state.value}_connection.glb"
            for state in DrawerReviewState
        }
        for state, output in outputs.items():
            parts = (
                cabinet_parts
                + self.review_geometry.build_hardware(step, plan, state)
                + self.review_geometry.build_drawer(box, plan, state)
            )
            self.exporter.export(f"ka_5332_{state.value}", parts, output)
            connection_parts = self.connection_closeup.build(
                parts,
                drawer_front_mm=drawer_front_mm,
                drawer_bottom_mm=drawer_bottom_mm,
            )
            self.exporter.export(
                f"ka_5332_{state.value}_connection",
                connection_parts,
                connection_outputs[state],
            )
        return HettichKa5332PrototypeResult(
            closed_glb=outputs[DrawerReviewState.CLOSED],
            open_glb=outputs[DrawerReviewState.OPEN],
            removed_glb=outputs[DrawerReviewState.REMOVED],
            closed_connection_glb=connection_outputs[DrawerReviewState.CLOSED],
            open_connection_glb=connection_outputs[DrawerReviewState.OPEN],
            removed_connection_glb=connection_outputs[DrawerReviewState.REMOVED],
            drawer_outside_width_mm=plan.drawer_outside_width_mm,
            recommended_width_met=plan.recommended_width_met,
            minimum_depth_met=plan.minimum_depth_met,
        )


__all__ = ["HettichKa5332PrototypeGenerator", "HettichKa5332PrototypeResult"]
