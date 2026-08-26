"""Scope: Generate the first cabinet's visual GLB from its local specification."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cadquery_glb_exporter import CadQueryGlbExporter
from generated_assembly_spec_loader import GeneratedAssemblySpecLoader
from unit_mockup import UnitMockupResult
from unit_mockup_geometry import UnitMockupGeometry


class UnitMockupGenerator:
    """Coordinate local-spec loading, visible geometry, and GLB writing."""

    def __init__(self) -> None:
        self.loader = GeneratedAssemblySpecLoader()
        self.geometry = UnitMockupGeometry()
        self.exporter = CadQueryGlbExporter()

    def generate_first(
        self, project_root: Path, project: dict[str, Any]
    ) -> UnitMockupResult:
        spec = self.loader.load_first(project_root, project)
        parts = self.geometry.build(spec)
        output = project_root / "assemblies" / spec.assembly_id / f"{spec.assembly_id}.glb"
        self.exporter.export(spec.assembly_id, parts, output)
        return UnitMockupResult(spec.assembly_id, output)
