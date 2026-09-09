"""Scope: Verify exact furniture fit checks and arbitrary nested design execution."""

import json
import os
from pathlib import Path
import subprocess
import sys

import cadquery as cq
import pytest

from build_furniture_design import FurnitureDesignBuild
from furniture_design_project import FurnitureDesignProject
from furniture_geometry_check import FurnitureGeometryCheck
from unit_mockup import MockupPart


class TestFurnitureGeometryCheck:
    """Use actual solids, including a concave envelope and nested rotated frames."""

    def part(self, name, size, origin=(0, 0, 0)):
        return MockupPart(
            name, cq.Workplane("XY").box(*size, centered=False),
            cq.Location(cq.Vector(*origin)), (0.7, 0.6, 0.5, 1),
        )

    def test_accepts_contact_but_reports_actual_material_overlap(self):
        envelope = cq.Workplane("XY").box(200, 100, 100, centered=False)
        left = self.part("left", (100, 50, 18))
        touching = self.part("right", (100, 50, 18), (100, 0, 0))
        valid = FurnitureGeometryCheck().check((left, touching), envelope)
        assert valid["status"] == "valid"
        assert valid["fabrication_ready"] is False
        overlap = self.part("right", (100, 50, 18), (99, 0, 0))
        result = FurnitureGeometryCheck().check((left, overlap), envelope)
        assert result["status"] == "invalid"
        assert result["overlaps"][0]["volume_mm3"] == pytest.approx(900)

    def test_checks_envelope_solid_instead_of_only_its_bounding_box(self):
        box = cq.Workplane("XY").box(200, 200, 100, centered=False)
        obstacle = cq.Workplane("XY").box(100, 100, 100, centered=False).translate((100, 100, 0))
        envelope = box.cut(obstacle)
        panel = self.part("shelf", (20, 20, 18), (120, 120, 0))
        result = FurnitureGeometryCheck().check((panel,), envelope)
        assert result["outside_envelope"][0]["outside_volume_mm3"] == pytest.approx(7200)
        assert result["status"] == "invalid"

    def test_rejects_empty_or_ambiguously_named_physical_output(self):
        envelope = cq.Workplane("XY").box(200, 100, 100, centered=False)
        with pytest.raises(ValueError, match="no physical parts"):
            FurnitureGeometryCheck().check((), envelope)
        part = self.part("same", (10, 10, 10))
        with pytest.raises(ValueError, match="paths must be unique"):
            FurnitureGeometryCheck().check((part, part), envelope)

    def test_keeps_every_solid_visible_at_the_custom_builder_boundary(self):
        first = cq.Workplane("XY").box(10, 10, 10, centered=False).val()
        second = first.translate((100, 0, 0))
        multiple = cq.Workplane("XY").newObject([first, second])
        part = MockupPart("custom", multiple, cq.Location(), (1, 1, 1, 1))
        envelope = cq.Workplane("XY").box(20, 20, 20, centered=False)
        with pytest.raises(ValueError, match="one Shape per Workplane"):
            FurnitureGeometryCheck().check((part,), envelope)
        with pytest.raises(ValueError, match="envelope must contain one Shape"):
            FurnitureGeometryCheck().check((part,), multiple)
        compound = cq.Workplane("XY").newObject([cq.Compound.makeCompound(multiple.vals())])
        complete = MockupPart("custom", compound, cq.Location(), (1, 1, 1, 1))
        report = FurnitureGeometryCheck().check((complete,), envelope)
        assert report["status"] == "invalid"
        assert report["outside_envelope"][0]["outside_volume_mm3"] == pytest.approx(1000)

    def test_builds_full_rotated_nested_tree_and_reloads_changed_design(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        package = tmp_path / "assemblies/furniture_01"
        package.mkdir()
        (package / "__init__.py").write_text('"""Scope: Own test furniture."""\n')
        builder = package / "builder.py"
        builder.write_text(self.design_source())
        output = tmp_path / "reviews/full.glb"
        result = FurnitureDesignBuild().build(tmp_path, "furniture_01", output)
        assert result["status"] == "valid"
        assert result["assembly_count"] == 2
        assert result["part_count"] == 2
        assert output.read_bytes()[:4] == b"glTF"
        assert json.loads(output.with_suffix(".geometry-check.json").read_text())["overlaps"] == []
        script = Path(__file__).resolve().parents[1] / "aikea-review-unit/scripts/build_furniture_design.py"
        command = subprocess.run(
            [sys.executable, str(script), str(tmp_path)], capture_output=True, text=True,
            env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        )
        assert command.returncode == 0, command.stderr
        assert json.loads(command.stdout)["part_count"] == 2
        builder.write_text(self.design_source().replace("Point3D(80, 20, 40)", "Point3D(300, 20, 40)"))
        changed = FurnitureDesignBuild().build(tmp_path, "furniture_01", output)
        assert changed["status"] == "invalid"
        assert changed["outside_envelope"][0]["part"] == "raised_01__surface"

    def design_source(self):
        return '''"""Scope: Define an invented nested composition for geometry tests."""
import cadquery as cq
from assemblies.specification import (
    PartSpec, Point3D, AxisBasis, AxisDirection, LocalToParentPlacement,
    IDENTITY_LOCAL_TO_PARENT, ChildAssemblySpec, BuiltChildAssembly,
)
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder

ENVELOPE = cq.Workplane("XY").box(150, 150, 150, centered=False)

class DesignBuilder:
    def build(self):
        surface = PartSpec("surface", "invented_surface", (), IDENTITY_LOCAL_TO_PARENT,
                           local_size_mm=(100, 60, 18))
        child = PanelAssemblySpec("raised_01", "raised_display", (surface,))
        placement = LocalToParentPlacement(Point3D(80, 20, 40), AxisBasis(
            AxisDirection(0, 1, 0), AxisDirection(-1, 0, 0), AxisDirection(0, 0, 1)))
        child_spec = ChildAssemblySpec("raised_01", "raised_display", placement)
        foot = PartSpec("foot", "foot", (), IDENTITY_LOCAL_TO_PARENT, local_size_mm=(50, 50, 18))
        root = PanelAssemblySpec("furniture_01", "unregistered_design", (foot,),
                                 child_assemblies=(child_spec,))
        return PanelAssemblyBuilder(root, children=(
            BuiltChildAssembly(child_spec, PanelAssemblyBuilder(child).build()),)).build()

BUILDER = DesignBuilder()
'''
