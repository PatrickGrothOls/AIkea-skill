"""Scope: Prove hardware drilling depends on a surface datum, not door construction."""

from math import pi
import cadquery as cq
import pytest
from concealed_hinge_machining import ConcealedHingeMachining
from door_hinge_side import DoorHingeSide
from riex_nc70_cup_pattern import RiexNc70CupPattern
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from surface_hole_pattern import SurfaceHole, SurfaceHolePattern


class TestSurfaceHolePattern:
    def test_pattern_on_rotated_surface_preserves_depth_and_axes(self):
        surface = cq.Plane(origin=(100, 200, 300), xDir=(0, 1, 0), normal=(-1, 0, 0))
        pattern = SurfaceHolePattern((SurfaceHole("hole", 10, 20, 8, 12),))
        placed = pattern.place(surface, entry_clearance_mm=0)[0]
        cylinder = next(face._geomAdaptor().Cylinder() for face in placed.cutter.Faces()
                        if face.geomType() == "CYLINDER")
        axis = cylinder.Axis()
        assert (axis.Location().X(), axis.Location().Y(), axis.Location().Z()) == pytest.approx((100, 210, 280))
        expected = cq.Solid.makeCylinder(4, 12, cq.Vector(100, 210, 280), cq.Vector(-1, 0, 0))
        # OCC may reverse the cylinder's parametric axis; occupied volume proves cut direction.
        assert placed.cutter.cut(expected).Volume() == pytest.approx(0, abs=1e-6)
        assert expected.cut(placed.cutter).Volume() == pytest.approx(0, abs=1e-6)
        assert placed.cutter.Volume() == pytest.approx(pi*4**2*12)
        assert placed.cutter.BoundingBox().xmin == pytest.approx(88)

    @pytest.mark.parametrize("side", [DoorHingeSide.LEFT, DoorHingeSide.RIGHT])
    def test_existing_hinge_adapter_preserves_actual_cut_volume(self, side):
        profile = RIEX_NC70_FULL_OVERLAY
        width, height = 520, 175
        x = profile.cup_center_from_edge_mm if side is DoorHingeSide.LEFT else width-profile.cup_center_from_edge_mm
        fix = profile.cup_fixing_line_from_edge_mm if side is DoorHingeSide.LEFT else width-profile.cup_fixing_line_from_edge_mm
        expected = cq.Solid.makeCylinder(17.5, 12.1, cq.Vector(x, height, -0.1))
        for y in (height-22.5, height+22.5):
            expected = expected.fuse(cq.Solid.makeCylinder(1.25, 10.1, cq.Vector(fix, y, -0.1)))
        actual = ConcealedHingeMachining()._door_cutter(height, profile, side, width).val()
        assert actual.cut(expected).Volume() == pytest.approx(0, abs=1e-6)
        assert expected.cut(actual).Volume() == pytest.approx(0, abs=1e-6)

    def test_same_pattern_cuts_one_board_or_two_layers(self):
        surface = cq.Plane(origin=(30, 60, 0), xDir=(1, 0, 0), normal=(0, 0, 1))
        pattern = RiexNc70CupPattern(RIEX_NC70_FULL_OVERLAY, 2.5, 10).build()
        holes = pattern.place(surface)
        slab = cq.Solid.makeBox(100, 120, 18)
        layers = [cq.Solid.makeBox(100, 120, 9),
                  cq.Solid.makeBox(100, 120, 9, cq.Vector(0, 0, 9))]
        for hole in holes:
            slab = slab.cut(hole.cutter)
            layers = [layer.cut(hole.cutter) for layer in layers]
        assembled = layers[0].fuse(layers[1])
        assert assembled.cut(slab).Volume() == pytest.approx(0, abs=1e-6)
        assert slab.cut(assembled).Volume() == pytest.approx(0, abs=1e-6)
        assert layers[1].Volume() < 100*120*9

    def test_pattern_can_be_placed_without_any_receiving_solid(self):
        pattern = RiexNc70CupPattern(RIEX_NC70_FULL_OVERLAY, 3, 8).build()
        assert [hole.spec.hole_id for hole in pattern.place(cq.Plane.XY())] == [
            "cup", "fixing_1", "fixing_2"]
