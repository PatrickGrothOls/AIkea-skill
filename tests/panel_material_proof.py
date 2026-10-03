"""Scope: Independently measure missing, extra and misplaced material in CNC panel results."""

import pytest

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from panel_blank_builder import PanelBlankBuilder
from panel_machining_builder import PanelMachiningBuilder


class PanelMaterialProof:
    """Test-only solid comparison; no load, toolpath or hardware-fit certification."""

    TOLERANCE_MM3 = 1e-5

    def expected_cuts(self, specification):
        # Rebuild from declared inputs rather than trusting returned cutter records.
        return (AssemblyJointMachiningBuilder(strict=True).build(specification, specification.joints).all
                + PanelMachiningBuilder().build(specification).all)

    def measure(self, part, cuts):
        blank = PanelBlankBuilder().build(part.spec).val()
        finished = part.solid.val()
        cutters = [cut.cutter.located(cut.location) for cut in cuts if cut.part_id == part.spec.part_id]
        actual_removed = blank.cut(finished)
        expected_volume = missing_volume = 0.0
        extra_volume = actual_removed.Volume()
        if cutters:
            # Boolean union counts shared holes/pockets once and clipping excludes
            # cutter material outside this participant (e.g. paired Cabineo cuts).
            union = cutters[0].fuse(*cutters[1:]) if len(cutters) > 1 else cutters[0]
            expected_removed = blank.intersect(union)
            expected_volume = expected_removed.Volume()
            missing_volume = expected_removed.cut(actual_removed).Volume()
            extra_volume = actual_removed.cut(expected_removed).Volume()
        return dict(part_id=part.spec.part_id,
                    expected_removed_mm3=expected_volume,
                    actual_removed_mm3=blank.Volume()-finished.Volume(),
                    missing_cut_mm3=missing_volume,
                    extra_cut_mm3=extra_volume,
                    added_material_mm3=finished.cut(blank).Volume())

    def assert_matches(self, report):
        assert report["actual_removed_mm3"] == pytest.approx(
            report["expected_removed_mm3"], abs=self.TOLERANCE_MM3, rel=0), report
        for field in ("missing_cut_mm3", "extra_cut_mm3", "added_material_mm3"):
            assert report[field] == pytest.approx(0, abs=self.TOLERANCE_MM3, rel=0), report
