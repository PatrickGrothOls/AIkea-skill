"""Scope: Bind installed point proofs to native solids under stored and baked source transforms."""
import cadquery as cq
import pytest

from source_normalized_frame import SourceNormalizedFrame
from unit_mockup import MockupPart


class TestSourceNormalizedFrame:
    @pytest.mark.parametrize("stored", (False, True))
    @pytest.mark.parametrize("angle,expected", ((0, ((110, -20, 35), (110, -19, 35))),
                                               (90, ((80, -30, 35), (79, -30, 35)))))
    def test_native_points_match_hand_derived_installed_vertices(self, stored, angle, expected):
        source = self.source(stored)
        native_location = source.location().toTuple()
        parent = cq.Location((100, -40, 5), (0, 0, 1), angle)
        part = MockupPart("source", cq.Workplane(obj=source), parent, (1, 1, 1, 1))
        proof = SourceNormalizedFrame(part, source)
        vertices = tuple(vertex.toTuple() for vertex in part.placed_shape().Vertices())
        for native, wanted in zip(((10, 20, 30), (10, 21, 30)), expected):
            assert proof.point(native) == pytest.approx(wanted, abs=1e-9)
            assert min(sum((actual-target)**2 for actual, target in zip(vertex, wanted))
                       for vertex in vertices) < 1e-16
        assert source.location().toTuple() == native_location

    def source(self, stored):
        if stored:
            box = cq.Workplane("XY").box(1, 2, 3, centered=False).val()
            return box.located(cq.Location((10, 20, 30), (0, 0, 1), 90))
        source = cq.Workplane(cq.Plane(origin=(0, 0, 30))).polyline(
            ((10, 20), (10, 21), (8, 21), (8, 20))).close().extrude(3).val()
        assert source.location().toTuple() == cq.Location().toTuple()
        return source
