"""Scope: Preserve analytic contacts and expose the reproduced inconsistent-kernel failure mode."""
import cadquery as cq
import pytest

from furniture_geometry_check import FurnitureGeometryCheck
from intersection_volume_check import IntersectionVolumeCheck
from unit_mockup import MockupPart


class TestIntersectionVolumeCheck:
    @pytest.mark.parametrize("offset,volume", ((1.01, 0), (1, 0), (0.999, 0.001), (0.5, 0.5)))
    @pytest.mark.parametrize("moved", (False, True))
    def test_analytic_clearance_contact_and_overlap_in_two_frames(self, offset, volume, moved):
        first = cq.Workplane("XY").box(1, 1, 1, centered=False).val()
        second = first.translate((offset, 0, 0))
        if moved:
            frame = cq.Location((120, -45, 80), (0, 0, 1), 33)
            first, second = first.moved(frame), second.moved(frame)
        intersection, problem = IntersectionVolumeCheck().measure(first, second, 1e-4)
        assert problem is None
        assert intersection.Volume() == pytest.approx(volume, abs=1e-10)

    @pytest.mark.parametrize("allowance", (False, True))
    def test_false_empty_intersection_cannot_produce_a_valid_geometry_report(self, monkeypatch, allowance):
        # Reproduce the observed external CAD-kernel failure: common is empty while cuts remove real material.
        monkeypatch.setattr(cq.Shape, "intersect", lambda self, *others, **options: cq.Compound.makeCompound([]))
        panel = cq.Workplane("XY").box(10, 10, 10, centered=False)
        parts = (MockupPart("first", panel, cq.Location(), (1, 1, 1, 1)),
                 MockupPart("second", panel, cq.Location((9, 0, 0)), (1, 1, 1, 1)))
        envelope = cq.Workplane("XY").box(20, 20, 20, centered=False)
        allowances = ({"allowance_id": "permitted-contact", "subject_paths": ["first", "second"],
                       "minimum_mm": [0, 0, 0], "maximum_mm": [20, 20, 20],
                       "maximum_volume_mm3": 8000},) if allowance else ()
        report = FurnitureGeometryCheck().check(parts, envelope, allowances)
        assert report["status"] == "invalid"
        assert report["overlaps"] == []
        assert report["allowed_overlaps"] == []
        problem, = report["uncertain_intersections"]
        assert problem["parts"] == ["first", "second"]
        assert problem["intersection_volume_mm3"] == 0
        assert problem["removed_from_first_mm3"] == pytest.approx(100)
        assert problem["removed_from_second_mm3"] == pytest.approx(100)
        assert report["fabrication_ready"] is False
