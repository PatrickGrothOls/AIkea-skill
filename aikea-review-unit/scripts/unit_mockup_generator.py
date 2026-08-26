"""Scope: Generate the first cabinet's visual GLB from its generated builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cadquery_glb_exporter import CadQueryGlbExporter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from unit_mockup import UnitMockupResult
from unit_mockup_geometry import UnitMockupGeometry


class UnitMockupGenerator:
    """Coordinate generated construction, visible placement, and GLB writing."""

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.geometry = UnitMockupGeometry()
        self.exporter = CadQueryGlbExporter()

    def generate_first(
        self, project_root: Path, project: dict[str, Any]
    ) -> UnitMockupResult:
        built_assembly = self.loader.load_first(project_root, project)
        parts = self.geometry.build(built_assembly)
        assembly_id = built_assembly.spec.assembly_id
        output = project_root / "assemblies" / assembly_id / f"{assembly_id}.glb"
        self.exporter.export(assembly_id, parts, output)
        return UnitMockupResult(assembly_id, output)
