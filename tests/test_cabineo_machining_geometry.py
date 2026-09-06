"""Scope: Preserve the existing Cabineo pocket and custom brass-insert machining."""

from math import pi

import cadquery as cq
import pytest

from cabineo_cutter import CabineoCutter


class TestCabineoMachiningGeometry:
    """Check the actual removed material against the established panel cuts."""

    def test_receiver_preserves_the_enlarged_brass_insert_pocket(self) -> None:
        cutter = CabineoCutter().cutout("<Z", "<Y", 0, 18, 0)
        panel = cq.Solid.makeBox(100, 18, 80, cq.Vector(-50, -18, 0))
        receiver = cutter.intersect(panel)
        bounds = receiver.BoundingBox()

        assert receiver.isValid()
        assert len(receiver.Solids()) == 1
        assert (bounds.xlen, bounds.ylen, bounds.zlen) == pytest.approx(
            (9.1, 12.5, 9.1)
        )
        assert (bounds.zmin, bounds.zmax) == pytest.approx((0.45, 9.55))
        assert receiver.Volume() == pytest.approx(pi * 4.55**2 * 12.5)

    def test_source_pocket_preserves_the_established_removed_volume(self) -> None:
        cutter = CabineoCutter().cutout("<Z", "<Y", 0, 18, 0)
        panel = cq.Solid.makeBox(100, 80, 18, cq.Vector(-50, 0, 0))
        pocket = cutter.intersect(panel)
        bounds = pocket.BoundingBox()

        assert pocket.isValid()
        assert len(pocket.Solids()) == 1
        assert (bounds.xlen, bounds.ylen, bounds.zlen) == pytest.approx(
            (15.0, 33.0, 10.5)
        )
        # This value was measured from the previous cutter inside the source panel.
        assert pocket.Volume() == pytest.approx(4568.311275598426, rel=0, abs=1e-6)
