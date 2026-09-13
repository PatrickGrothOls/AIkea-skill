"""Scope: Verify complete drawer material removal and reject equal-volume wrong cuts."""

from dataclasses import replace
from math import pi
from types import SimpleNamespace

import cadquery as cq
import pytest

from movento_panel_dimensions import MoventoPanelDimensions
from movento_panel_drawer import MoventoPanelDrawer
from movento_panel_machining import MoventoPilotChoice
from panel_blank_builder import PanelBlankBuilder
from panel_material_proof import PanelMaterialProof
from test_movento_panel_drawer import TestMoventoPanelDrawer as DrawerFixture


class TestMoventoMaterialRemoval:
    drawer = DrawerFixture.drawer

    def build(self):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        # Actual eight-drawer dresser's local dimensions, including its visible front.
        dimensions = MoventoPanelDimensions(661,120,657,152.5,2,-18,22,
                                           "ply16","prepared14.5","front22")
        spec = MoventoPanelDrawer().specification("drawer_01", dimensions,
            MoventoPilotChoice(5,14,2.5,10,"Test preparation; not production qualification"))
        return PanelAssemblyBuilder(spec).build()

    def test_every_panel_matches_all_declared_cuts_in_volume_and_shape(self, drawer):
        _, built = drawer
        proof = PanelMaterialProof()
        cuts = proof.expected_cuts(built.spec)
        assert {part.spec.part_id for part in built.parts} == {"left","right","back","front","rail","bottom"}
        for part in built.parts:
            proof.assert_matches(proof.measure(part, cuts))

    def test_grooves_and_drilling_match_independent_analytic_volumes(self, drawer):
        _, built = drawer
        expected = {"bottom_groove_left":490*16.2*6,
                    "bottom_groove_right":490*16.2*6,
                    "bottom_groove_back":619*16.2*6,
                    "bottom_groove_front":(651*16.2-(4-pi)*3**2)*6,
                    "rear_hooks":2*pi*3**2*16,
                    "locking_clips":4*pi*1.25**2*10,
                    "runner_relief":2*pi*6**2*.5}
        for identifier, volume in expected.items():
            cut = next(c for c in built.cuts if c.joint_id == identifier)
            part = next(p for p in built.parts if p.spec.part_id == cut.part_id)
            blank = PanelBlankBuilder().build(part.spec).val()
            assert blank.intersect(cut.cutter.located(cut.location)).Volume() == pytest.approx(
                volume, abs=1e-5, rel=0), identifier

    def test_rejects_extra_cut_in_otherwise_unmachined_bottom(self, drawer):
        _, built = drawer
        bottom = next(p for p in built.parts if p.spec.part_id == "bottom")
        changed = replace(bottom, solid=bottom.solid.cut(cq.Workplane("XY").circle(3).extrude(16)))
        proof = PanelMaterialProof()
        with pytest.raises(AssertionError):
            proof.assert_matches(proof.measure(changed, proof.expected_cuts(built.spec)))

    def test_equal_volume_wrong_position_fails_shape_comparison(self, drawer):
        _, built = drawer
        part = next(p for p in built.parts if p.spec.part_id == "left")
        groove = next(c for c in built.cuts if c.joint_id == "bottom_groove_left")
        blank = PanelBlankBuilder().build(part.spec)
        wrong = groove.cutter.located(groove.location).translate((0,30,0))
        changed = replace(part, solid=blank.cut(wrong))
        proof = PanelMaterialProof()
        report = proof.measure(changed, (groove,))
        assert report["actual_removed_mm3"] == pytest.approx(report["expected_removed_mm3"], abs=1e-5, rel=0)
        assert report["missing_cut_mm3"] > 1000 and report["extra_cut_mm3"] > 1000
        with pytest.raises(AssertionError):
            proof.assert_matches(report)

    def test_overlapping_cutters_are_counted_once_and_clipped_to_stock(self, drawer):
        _, built = drawer
        bottom = next(p for p in built.parts if p.spec.part_id == "bottom")
        blank = PanelBlankBuilder().build(bottom.spec)
        first = cq.Solid.makeBox(20,10,20,cq.Vector(10,10,-2))
        second = cq.Solid.makeBox(20,10,20,cq.Vector(20,10,-2))
        cuts = tuple(SimpleNamespace(part_id="bottom",cutter=shape,location=cq.Location())
                     for shape in (first,second))
        changed = replace(bottom,solid=blank.cut(first).cut(second))
        proof = PanelMaterialProof()
        report = proof.measure(changed,cuts)
        assert report["expected_removed_mm3"] == pytest.approx(30*10*16, abs=1e-5, rel=0)
        proof.assert_matches(report)

    def test_rejects_material_added_outside_blank(self, drawer):
        _, built = drawer
        bottom = next(p for p in built.parts if p.spec.part_id == "bottom")
        tab = cq.Solid.makeBox(10,10,16,cq.Vector(-5,10,0))
        changed = replace(bottom,solid=bottom.solid.union(tab))
        proof = PanelMaterialProof()
        report = proof.measure(changed,())
        assert report["added_material_mm3"] == pytest.approx(5*10*16,abs=1e-5,rel=0)
        with pytest.raises(AssertionError):
            proof.assert_matches(report)
