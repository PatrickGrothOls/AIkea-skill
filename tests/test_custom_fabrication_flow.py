"""Scope: Run a non-cabinet root from generated code through its existing fabrication decision."""

import json
from pathlib import Path
import subprocess
import sys

import cadquery as cq

from check_fabrication_readiness import CheckFabricationReadinessCommand
from furniture_design_project import FurnitureDesignProject
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from review_server_session import ReviewServerSession
from blender_presentation_test_evidence import BlenderPresentationTestEvidence


class TestCustomFabricationFlow:
    def test_flat_custom_root_reaches_ready_only_after_current_pack_and_decision(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        (tmp_path / "aikea.yaml").write_text("{}\n")
        package = tmp_path / "assemblies/furniture_01"
        package.mkdir()
        builder = package / "builder.py"
        builder.write_text(self._source())
        script = Path(__file__).resolve().parents[1] / "aikea-review-unit/scripts/build_furniture_design.py"
        result = subprocess.run([sys.executable, str(script), str(tmp_path), "--fabrication-review"],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        report = json.loads(result.stdout)
        assert report["status"] == "valid" and report["fabrication_ready"] is False
        assert report["construction_status"] == "verified_operations"
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, "furniture_01")
        self._pack(tmp_path, built.parts[0])
        command = CheckFabricationReadinessCommand()
        assert command.run(tmp_path / "aikea.yaml", "furniture_01") == 2
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        BlenderPresentationTestEvidence().write(model, model)
        session = ReviewServerSession(model, tmp_path / "reviews/fabrication-assembly.json", model)
        session.decide("approved", session.token)
        assert command.run(tmp_path / "aikea.yaml", "furniture_01") == 0
        assert not (tmp_path / "assemblies/full-wardrobe-position-check.json").exists()
        builder.write_text(self._source().replace('material_id="mdf"', 'material_id="birch"'))
        assert command.run(tmp_path / "aikea.yaml", "furniture_01") == 2

    def _source(self):
        return '''"""Scope: Build one intentionally loose cut sample outside any cabinet recipe."""
import cadquery as cq
from assemblies.specification import PartSpec, ConstructionRequirementSpec, IDENTITY_LOCAL_TO_PARENT
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder

ENVELOPE = cq.Workplane("XY").box(120, 120, 20, centered=False)
PART = PartSpec("sample", "test sample", (), IDENTITY_LOCAL_TO_PARENT,
                local_size_mm=(100, 100, 16), material_id="mdf")
SPEC = PanelAssemblySpec("furniture_01", "custom sample", (PART,), requirements=(
    ConstructionRequirementSpec("loose_sample", "Supply an unattached material sample", ("part:sample",),
                                disposition="loose", basis="This sample is intentionally unattached"),
))
BUILDER = PanelAssemblyBuilder(SPEC)
'''

    def _pack(self, root, part):
        path = "furniture_01/sample"
        output = root / "manufacturing/parts/furniture_01__sample"
        output.parent.mkdir(parents=True)
        cq.exporters.export(part.solid, str(output.with_suffix(".step")))
        cq.exporters.export(part.solid.faces(">Z"), str(output.with_suffix(".dxf")))
        (root / "manufacturing/bom.json").write_text(json.dumps({"schema_version": 1,
            "manufactured_parts": [{"path": path, "material": "mdf", "thickness_mm": 16, "quantity": 1}],
            "purchased_hardware": []}))
        (root / "manufacturing/cut-list.csv").write_text(
            "path,material,thickness_mm,quantity,blank_width_mm,blank_height_mm\n"
            f"{path},mdf,16,1,100,100\n")
        (root / "manufacturing/machining.json").write_text(json.dumps(
            {"schema_version": 1, "parts": [{"path": path, "operations": []}]}))
