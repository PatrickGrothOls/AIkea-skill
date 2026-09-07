"""Scope: Verify manufactured blanks cannot evade CNC limits through tree placement."""

import importlib

import cadquery as cq
import pytest

from assembly_composition_test_case import AssemblyCompositionTestCase
from furniture_cnc_check import FurnitureCncCheck


class TestFurnitureCncCheck(AssemblyCompositionTestCase):
    """Exercise actual project contracts and solids, including custom-built parts."""

    @pytest.mark.parametrize("actual,declared,expected", [
        ((2490, 1990, 18), (), "valid"),
        ((1990, 2490, 18), (), "valid"),
        ((2490.001, 100, 18), (), "invalid"),
        ((3940, 465, 18), (100, 465, 18), "invalid"),
        ((100, 465, 18), (3940, 465, 18), "invalid"),
        ((2000, 2000, 18), (), "invalid"),
    ])
    def test_uses_actual_and_declared_local_blank_extents(
        self, generated_values, actual, declared, expected
    ):
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        part = self.part(values, actual, declared)
        visit = tree.AssemblyTreePart(
            ("furniture_01", "part:custom"), part, values.IDENTITY_LOCAL_TO_PARENT)
        report = FurnitureCncCheck().check((visit,))
        assert report["status"] == expected
        assert report["checked_part_count"] == 1
        assert report["usable_xy_mm"] == [2490, 1990]

    @pytest.mark.parametrize("declared", [(100, 100), (100, float("nan"), 18), (100, 100, 0)])
    def test_rejects_malformed_custom_blank_dimensions(self, generated_values, declared):
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        part = self.part(values, (100, 100, 3000), declared)
        visit = tree.AssemblyTreePart(
            ("furniture_01", "part:custom"), part, values.IDENTITY_LOCAL_TO_PARENT)
        with pytest.raises(ValueError, match="three finite positive dimensions"):
            FurnitureCncCheck().check((visit,))

    def test_nested_rotation_and_hardware_role_do_not_exempt_a_panel(self, generated_values):
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        rotated = values.LocalToParentPlacement(values.Point3D(0, 0, 0), values.AxisBasis(
            values.AxisDirection(0, 0, 1), values.AxisDirection(0, 1, 0),
            values.AxisDirection(-1, 0, 0)))
        part = self.part(values, (3000, 100, 18), ())
        child_spec = self.fixture_assembly_spec("child_01", "custom", (), (), (part.spec,))
        child = values.BuiltAssembly(child_spec, (part,), ())
        placement = values.ChildAssemblySpec("child_01", "custom", rotated)
        root_spec = self.fixture_assembly_spec("furniture_01", "custom", (placement,), ())
        root = values.BuiltAssembly(root_spec, (), (), child_assemblies=(
            values.BuiltChildAssembly(placement, child),))
        report = FurnitureCncCheck().check(tree.AssemblyTreeWalker().walk(root))
        assert report["oversized_parts"][0]["part"] == "furniture_01/child_01/part:custom"
        assert report["oversized_parts"][0]["blank_size_mm"] == [3000, 100, 18]

    def test_purchased_hardware_is_outside_panel_machining(self, generated_values):
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        spec = values.PurchasedHardwareSpec(
            "bought_rail", "supplier", "article", "asset", values.IDENTITY_LOCAL_TO_PARENT)
        hardware = values.BuiltPurchasedHardware(spec, cq.Workplane("XY").box(3000, 20, 20))
        visit = tree.AssemblyTreeHardware(("furniture_01", "hardware:bought_rail"),
                                          hardware, values.IDENTITY_LOCAL_TO_PARENT)
        report = FurnitureCncCheck().check((visit,))
        assert report["status"] == "valid"
        assert report["checked_part_count"] == 0

    def part(self, values, actual, declared):
        spec = values.PartSpec("custom", "hardware", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=declared)
        return values.BuiltPart(spec, cq.Workplane("XY").box(*actual, centered=False))
