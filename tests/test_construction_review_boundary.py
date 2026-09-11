"""Scope: Exercise custom construction validation through actual project entry points."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from build_furniture_design import FurnitureDesignBuild
from furniture_design_project import FurnitureDesignProject
from part_construction_error import PartConstructionError
from test_furniture_geometry_check import TestFurnitureGeometryCheck as GeometryFixture


class TestConstructionReviewBoundary:
    """Keep generated and authored root builds on the same checked path."""

    def _project(self, root):
        FurnitureDesignProject().initialize(root)
        package = root / "assemblies/furniture_01"
        package.mkdir()
        (package / "__init__.py").write_text("")
        (package / "builder.py").write_text(GeometryFixture().design_source())
        return package

    def test_complete_builder_is_used_and_report_matches_returned_evidence(self, tmp_path):
        package = self._project(tmp_path)
        (package / "complete_builder.py").write_text('''"""Scope: Apply a test root feature."""
from dataclasses import replace
from .builder import BUILDER as BASE

class CompleteBuilder:
    def build(self):
        base = BASE.build()
        part = replace(base.parts[0], solid=base.parts[0].solid.translate((500, 0, 0)))
        return replace(base, parts=(part,))

BUILDER = CompleteBuilder()
''')
        output = tmp_path / "reviews/full.glb"
        report = FurnitureDesignBuild().build(tmp_path, "furniture_01", output)
        assert report["status"] == "invalid"
        assert report["outside_envelope"][0]["part"] == "foot"
        assert report["construction_status"] == "incomplete"
        checks = {item["code"]: item["passed"] for item in report["construction_checks"]}
        assert checks["construction.applied_operations"]
        assert not checks["construction.requirement_coverage"]
        assert json.loads(output.with_suffix(".geometry-check.json").read_text()) == report

    def test_failed_builder_revokes_previous_success_report(self, tmp_path):
        package = self._project(tmp_path)
        output = tmp_path / "reviews/full.glb"
        assert FurnitureDesignBuild().build(tmp_path, "furniture_01", output)["status"] == "valid"
        (package / "builder.py").write_text(self._unmachined_grid())
        with pytest.raises(PartConstructionError, match="missing="):
            FurnitureDesignBuild().build(tmp_path, "furniture_01", output)
        saved = json.loads(output.with_suffix(".geometry-check.json").read_text())
        assert saved["status"] == "invalid"
        assert saved["fabrication_ready"] is False
        assert "glb" not in saved

    def test_fabrication_cli_accepts_custom_root_and_reports_real_gaps(self, tmp_path):
        self._project(tmp_path)
        project = tmp_path / "aikea.yaml"
        project.write_text("{}\n")
        script = Path(__file__).parents[1] / "aikea-review-unit/scripts/check_fabrication_readiness.py"
        result = subprocess.run([sys.executable, str(script), str(project), "--assembly", "furniture_01"],
                                capture_output=True, text=True)
        assert result.returncode == 2, result.stderr
        report = json.loads(result.stdout)
        checks = {check["code"]: check for check in report["checks"]}
        assert report["status"] == "blocked"
        assert "evaluation.invalid" not in checks
        assert checks["construction.applied_operations"]["passed"] is True
        assert checks["pack.part_step_and_drawings"]["passed"] is False

    def _unmachined_grid(self):
        return '''"""Scope: Return a plausible but unmachined part for rejection testing."""
import cadquery as cq
from assemblies.specification import PartSpec, PartMachiningSpec, IDENTITY_LOCAL_TO_PARENT, BuiltPart, BuiltAssembly
from assemblies.panel_assembly import PanelAssemblySpec

ENVELOPE = cq.Workplane("XY").box(500, 800, 100, centered=False)

class RawBuilder:
    def build(self):
        part = PartSpec("board", "custom", (), IDENTITY_LOCAL_TO_PARENT,
                        local_size_mm=(400, 700, 16), inside_face=">Z")
        spec = PanelAssemblySpec("furniture_01", "custom", (part,),
                                machining=(PartMachiningSpec("grid", "board", "system_32"),))
        solid = cq.Workplane("XY").box(400, 700, 16, centered=False)
        return BuiltAssembly(spec, (BuiltPart(part, solid),), ())

BUILDER = RawBuilder()
'''
