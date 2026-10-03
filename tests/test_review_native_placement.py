"""Scope: Bind reported and checked geometry to analytically known nested native transforms."""
import json

import cadquery as cq
import pytest

from cadquery_glb_exporter import CadQueryGlbExporter
from complete_assembly_review_report import CompleteAssemblyReviewReport
from furniture_geometry_check import FurnitureGeometryCheck
from unit_mockup import MockupPart


class TestReviewNativePlacement:
    @pytest.mark.parametrize("nested,expected", (
        (False, {"x": [7, 12], "y": [11, 14], "z": [11, 13]}),
        (True, {"x": [86, 89], "y": [207, 212], "z": [311, 313]})))
    def test_report_and_fit_keep_native_transform_under_parent_frame(self, tmp_path, nested, expected):
        source = cq.Workplane("XY").box(2, 3, 5, centered=False).val().located(
            cq.Location((7, 11, 13), (0, 1, 0), 90))
        native = source.location().toTuple()
        parent = cq.Location((100, 200, 300), (0, 0, 1), 90) if nested else cq.Location()
        part = MockupPart("front", cq.Workplane(obj=source), parent, (1, 1, 1, 1))
        path = tmp_path / "front.glb"
        CadQueryGlbExporter().export("front_01", (part,), path)
        report = json.loads(CompleteAssemblyReviewReport().write("front_01", path, (part,), {}).read_text())
        assert report["items"][0]["bounds_mm"] == expected
        origin = tuple(expected[axis][0] for axis in "xyz")
        size = tuple(expected[axis][1] - expected[axis][0] for axis in "xyz")
        envelope = cq.Workplane("XY").box(*size, centered=False).translate(origin)
        result = FurnitureGeometryCheck().check((part,), envelope)
        assert result["status"] == "valid", result
        assert source.location().toTuple() == native

    def test_collision_check_uses_the_same_composed_native_shape(self):
        native = cq.Location((20, 30, 40))
        source = cq.Workplane("XY").box(10, 10, 10, centered=False).val().located(native)
        shifted = MockupPart("shifted", cq.Workplane(obj=source), cq.Location((100, 0, 0)), (1, 1, 1, 1))
        obstacle = MockupPart("obstacle", cq.Workplane("XY").box(1, 1, 1, centered=False),
                              cq.Location((125, 35, 45)), (1, 1, 1, 1))
        envelope = cq.Workplane("XY").box(200, 100, 100, centered=False)
        result = FurnitureGeometryCheck().check((shifted, obstacle), envelope)
        assert result["outside_envelope"] == []
        assert result["overlaps"] == [{"parts": ["shifted", "obstacle"], "volume_mm3": 1.0}]
        assert result["status"] == "invalid"
