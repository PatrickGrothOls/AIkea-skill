"""Scope: Export a wardrobe containing independently posed drawer collections."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import cadquery as cq

from assembly_tree_review_plan import (
    AssemblyReviewMotion,
    AssemblyReviewOverlay,
    AssemblyTreeReviewPlan,
)
from assembly_run import AssemblyRunReader
from cabinet_review_geometry import CabinetReviewGeometry
from door_review_state import DoorReviewState
from drawer_collection_wardrobe_review import DrawerCollectionWardrobeReviewResult
from full_wardrobe_door_plan import FullWardrobeDoorPlan
from full_wardrobe_review_generator import FullWardrobeReviewGenerator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_5332_drawers_position_checker import (
    HettichKa5332DrawersPositionChecker,
)
from hettich_ka_5332_drawers_review_geometry import (
    HettichKa5332DrawersReviewGeometry,
)
from hettich_ka_5332_saved_drawers_loader import HettichKa5332SavedDrawersLoader
from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader
from unit_mockup import UnitMockupInputError


class DrawerCollectionWardrobeReviewGenerator:
    """Build all saved drawers, validate closed positions, and pose each independently."""

    _COMPOSED_BUILDER_MODULE = "with_drawers_builder"
    _CURRENT_RUNNER_ITEM_NUMBER = "9057405"

    def __init__(self) -> None:
        self.run_reader = AssemblyRunReader()
        self.loader = GeneratedAssemblyBuilderLoader()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.saved_drawers = HettichKa5332SavedDrawersLoader()
        self.drawer_geometry = HettichKa5332DrawersReviewGeometry()
        self.position_checker = HettichKa5332DrawersPositionChecker()
        self.step_loader = HettichKa5332StepAssemblyLoader()
        self.full_wardrobe = FullWardrobeReviewGenerator()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
        hardware_directory: Path,
        extensions_mm: Mapping[str, Mapping[str, float]],
        door_plan: FullWardrobeDoorPlan | None = None,
        output_filename: str = "full_wardrobe_drawer_collection_review.glb",
    ) -> DrawerCollectionWardrobeReviewResult:
        step = self.step_loader.load(hardware_directory)
        steps = {self._CURRENT_RUNNER_ITEM_NUMBER: step}
        assembly_ids = tuple(
            item.assembly_id for item in self.run_reader.read(project).assemblies
        )
        unknown = set(extensions_mm) - set(assembly_ids)
        if unknown:
            raise UnitMockupInputError(
                ["drawer extensions target unknown cabinets: " + ", ".join(sorted(unknown))]
            )
        motions: list[AssemblyReviewMotion] = []
        hidden_hardware: list[tuple[str, ...]] = []
        overlays: list[AssemblyReviewOverlay] = []
        reports: list[Path] = []
        for assembly_id in assembly_ids:
            cabinet = self.loader.load_assembly(
                project_root,
                assembly_id,
                self._COMPOSED_BUILDER_MODULE,
            )
            saved = self.saved_drawers.load(project_root, assembly_id, cabinet)
            cabinet_parts = self.cabinet_geometry.build(
                cabinet,
                DoorReviewState.CLOSED,
            )
            closed_drawers = self.drawer_geometry.build_drawers(saved, {})
            report = self.position_checker.check(
                cabinet,
                cabinet_parts,
                closed_drawers,
            )
            report_path = (
                project_root
                / "assemblies"
                / assembly_id
                / "drawers-position-check.json"
            )
            report.write(report_path)
            if not report.is_valid:
                raise UnitMockupInputError(
                    [
                        f"{assembly_id} drawer position check failed: "
                        + ", ".join(report.failed_check_names())
                    ]
                )
            poses = extensions_mm.get(assembly_id, {})
            cabinet_path = ("wardrobe_01", assembly_id)
            overlays.append(
                AssemblyReviewOverlay(
                    cabinet_path,
                    self.drawer_geometry.build_hardware(saved, steps, poses),
                )
            )
            for drawer in saved:
                extension_mm = float(poses.get(drawer.drawer_id, 0.0))
                if extension_mm:
                    motions.append(
                        AssemblyReviewMotion(
                            cabinet_path + (drawer.drawer_id,),
                            cq.Location(cq.Vector(0.0, -extension_mm, 0.0)),
                        )
                    )
                hidden_hardware.extend(
                    cabinet_path
                    + (f"hardware:{drawer.drawer_id}_runner_{hand}",)
                    for hand in ("left", "right")
                )
            reports.append(report_path)
        review_plan = AssemblyTreeReviewPlan(
            motions=tuple(motions),
            hidden_paths=tuple(hidden_hardware),
            overlays=tuple(overlays),
        )
        full = self.full_wardrobe.generate(
            project_root,
            project,
            door_plan or FullWardrobeDoorPlan.uniform(DoorReviewState.CLOSED),
            review_plan,
            output_filename,
        )
        return DrawerCollectionWardrobeReviewResult(
            full.glb_path,
            tuple(reports),
            full.position_report_path,
        )


__all__ = ["DrawerCollectionWardrobeReviewGenerator"]
