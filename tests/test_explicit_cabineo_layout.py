"""Scope: Verify authored connector positions retain paired cuts and spacing limits."""

from types import SimpleNamespace

import cadquery as cq
import pytest

from cabineo_connector_layout import CabineoConnectorLayout
from cabineo_joint import CabineoJoint
from part_construction_error import PartConstructionError


class TestExplicitCabineoLayout:
    def joint(self, positions):
        return SimpleNamespace(joint_id="rail_to_side", source_part_id="rail",
            target_part_id="side", source_face="<Z", source_edge="<X",
            connector_layout="explicit", connector_positions_mm=positions)

    def test_nonuniform_positions_drive_identical_paired_cutters(self):
        rail = SimpleNamespace(part_id="rail", local_size_mm=(708, 64, 29))
        side = SimpleNamespace(part_id="side", local_size_mm=(490, 150, 16))
        target_location = cq.Location(cq.Vector(-16, 0, 0))
        cuts = CabineoJoint().build(self.joint((16, 52)), rail, side,
                                    cq.Location(), target_location)
        assert len(cuts) == 4
        for position, source, target in zip((16, 52), cuts[::2], cuts[1::2]):
            bounds = source.cutter.BoundingBox()
            assert (bounds.ymin + bounds.ymax) / 2 == pytest.approx(position)
            assert source.cutter is target.cutter
            placed = target.cutter.located(target_location * target.location)
            assert source.cutter.cut(placed).Volume() == pytest.approx(0, abs=1e-5)

    @pytest.mark.parametrize("positions", [(), (16,), (52, 16), (16, 16),
        (float("nan"), 52), (16, float("inf")), (-1, 52), (16, 65)])
    def test_invalid_positions_are_rejected(self, positions):
        with pytest.raises(PartConstructionError):
            CabineoConnectorLayout().positions(self.joint(positions),
                SimpleNamespace(local_size_mm=(708, 64, 29)))

    @pytest.mark.parametrize("positions", [(201, 400), (50, 351, 500), (50, 200)])
    def test_explicit_positions_preserve_structural_spacing_limits(self, positions):
        with pytest.raises(PartConstructionError):
            CabineoConnectorLayout().positions(self.joint(positions),
                SimpleNamespace(local_size_mm=(708, 600, 29)))

    def test_source_cutter_bounds_still_apply(self):
        rail = SimpleNamespace(part_id="rail", local_size_mm=(708, 64, 29))
        with pytest.raises(PartConstructionError, match="too short"):
            CabineoJoint().build(self.joint((2, 52)), rail, rail,
                                cq.Location(), cq.Location())
