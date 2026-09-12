"""Scope: Verify the ordinary build includes resolved hardware in exports and evidence."""

import json
from unittest.mock import patch

import cadquery as cq
import pytest

from build_furniture_design import FurnitureDesignBuild
from construction_position_evidence import ConstructionPositionEvidence
from furniture_design_project import FurnitureDesignProject
from project_hardware_geometry_resolver import ProjectHardwareGeometryError, ProjectHardwareGeometryResolver


class TestHardwareProvider:
    """Supply a known synthetic body to test integration, not vendor dimensions."""

    def supports(self, asset_id):
        return asset_id == "test-foot"

    def resolve(self, project_root, spec):
        return cq.Workplane("XY").box(10, 10, 10, centered=False)


class TestConstructionHardwareLoading:
    def _project(self, root):
        FurnitureDesignProject().initialize(root)
        folder = root / "assemblies/furniture_01"
        folder.mkdir()
        (folder / "builder.py").write_text('''"""Scope: Declare a panel and an unresolved purchased item for integration proof."""
import cadquery as cq
from assemblies.specification import PartSpec, IDENTITY_LOCAL_TO_PARENT, IDENTITY_AXIS_BASIS, LocalToParentPlacement, Point3D
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder
from assemblies.assembly_composition import BuiltPurchasedHardware
from purchased_hardware_spec import PurchasedHardwareSpec, HardwarePurchaseSpec

class Builder:
    def build(self):
        panel = PartSpec("panel", "shelf", (), IDENTITY_LOCAL_TO_PARENT,
                         local_size_mm=(100, 50, 16), material_id="test-mdf")
        item = PurchasedHardwareSpec("foot", "test", "test-foot", "test-foot",
            LocalToParentPlacement(Point3D(120, 0, 0), IDENTITY_AXIS_BASIS),
            purchase=HardwarePurchaseSpec("foot", "test-foot", "piece", "item", ("item",)))
        spec = PanelAssemblySpec("furniture_01", "test", parts=(panel,), purchased_hardware=(item,))
        return PanelAssemblyBuilder(spec, hardware=(BuiltPurchasedHardware(item, None),)).build()

BUILDER = Builder()
ENVELOPE = cq.Workplane("XY").box(200, 100, 100, centered=False)
''')

    @pytest.mark.parametrize("fabrication", [False, True])
    def test_hydrated_hardware_reaches_geometry_export_and_position_evidence(self, tmp_path, fabrication):
        self._project(tmp_path)
        output = tmp_path / ("assemblies/full_wardrobe_review.glb" if fabrication else "reviews/current.glb")
        with patch.object(ProjectHardwareGeometryResolver, "_default_providers", return_value=(TestHardwareProvider(),)):
            report = FurnitureDesignBuild().build(tmp_path, "furniture_01", output, fabrication)
        assert report["status"] == "valid"
        assert report["construction_status"] == "incomplete"
        assert output.is_file()
        record = json.loads((tmp_path / ConstructionPositionEvidence.REPORT).read_text())
        assert len(record["physical_items"]) == 2
        assert any("hardware:foot" in str(item) for item in record["physical_items"])

    def test_missing_provider_keeps_failure_visible(self, tmp_path):
        self._project(tmp_path)
        output = tmp_path / "reviews/current.glb"
        with patch.object(ProjectHardwareGeometryResolver, "_default_providers", return_value=()):
            with pytest.raises(ProjectHardwareGeometryError, match="no exact geometry provider"):
                FurnitureDesignBuild().build(tmp_path, "furniture_01", output)
        assert not output.exists()
        report = json.loads(output.with_suffix(".geometry-check.json").read_text())
        assert report["status"] == "invalid"
        assert not report["fabrication_ready"]
