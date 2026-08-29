"""Scope: Export three visual states of one exact KA 5332 drawer prototype."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from drawer_review_geometry import DrawerReviewGeometry
from drawer_review_state import DrawerReviewState
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_5332_connection_closeup import HettichKa5332ConnectionCloseup
from hettich_ka_5332_review_geometry import HettichKa5332ReviewGeometry
from hettich_ka_5332_saved_plan_loader import HettichKa5332SavedPlanLoader
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
    """Review the saved cabinet child around the exact runner STEP."""

    def __init__(self) -> None:
        self.cabinet_loader = GeneratedAssemblyBuilderLoader()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.drawer_geometry = DrawerReviewGeometry()
        self.step_loader = HettichKa5332StepAssemblyLoader()
        self.saved_plan_loader = HettichKa5332SavedPlanLoader()
        self.review_geometry = HettichKa5332ReviewGeometry()
        self.connection_closeup = HettichKa5332ConnectionCloseup()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        hardware_directory: Path,
        output_directory: Path,
    ) -> HettichKa5332PrototypeResult:
        cabinet = self.cabinet_loader.load_assembly(
            project_root,
            assembly_id,
            "with_drawers_builder",
        )
        step = self.step_loader.load(hardware_directory)
        plan = self.saved_plan_loader.load(project_root, assembly_id, cabinet)
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
                + self.drawer_geometry.build(cabinet, state)
            )
            self.exporter.export(f"ka_5332_{state.value}", parts, output)
            connection_parts = self.connection_closeup.build(
                parts,
                drawer_front_mm=plan.drawer_origin_mm[1],
                drawer_bottom_mm=plan.drawer_origin_mm[2],
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
