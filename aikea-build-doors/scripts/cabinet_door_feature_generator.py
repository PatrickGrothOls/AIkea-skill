"""Scope: Save one fitted door as a registered reusable cabinet feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_door_feature_file_set_renderer import (
    CabinetDoorFeatureFileSetRenderer,
)
from cabinet_feature_manifest import CabinetFeatureManifest
from door_generated_file_record import DoorGeneratedFileRecord
from door_hinge_plan import DoorHingePlan
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class CabinetDoorFeatureGenerator:
    """Write generated door modules without owning review artifacts."""

    def __init__(self) -> None:
        self.renderer = CabinetDoorFeatureFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()
        self.features = CabinetFeatureManifest()

    def generate(
        self,
        project_root: Path,
        assembly: Any,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
    ) -> tuple[Path, ...]:
        files = self.renderer.render(assembly, plan, profile)
        recorded = DoorGeneratedFileRecord.load(project_root, plan.assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        DoorGeneratedFileRecord.from_rendered(
            plan.assembly_id,
            files,
        ).save(project_root)
        manifest = self.features.register(
            project_root,
            plan.assembly_id,
            "door_hinges.feature",
            20,
            review_module="door_hinges.review",
            affected_manufactured_part_paths=(
                "door_panel",
                plan.hinge_side.side_part_id,
            ),
        )
        return written + ((manifest.relative_to(project_root),) if manifest else ())


__all__ = ["CabinetDoorFeatureGenerator"]
