"""Scope: Prove independent HDF floor stock preserves captured one-face construction."""

from dataclasses import asdict, replace
from functools import partial

import pytest

from generated_project_module_runtime import GeneratedProjectModuleRuntime
from movento_panel_dimensions import MoventoPanelDimensions
from movento_panel_drawer import MoventoPanelDrawer
from movento_panel_machining import MoventoPilotChoice
from panel_setup_checker import PanelSetupChecker
from test_movento_captured_bottom import TestMoventoCapturedBottom as CaptureProof
from test_movento_panel_drawer import TestMoventoPanelDrawer as DrawerFixture


class TestMoventoBottomStock:
    drawer = DrawerFixture.drawer

    def dimensions(self):
        return MoventoPanelDimensions(661,120,657,152.5,2,-18,22,
            "ply16","prepared14.5","front22",bottom_thickness_mm=6,bottom_material="HDF6")

    def build(self, dimensions=None):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        # The existing fixture calls build without arguments; comparison supplies stock explicitly.
        selected = self.dimensions() if dimensions is None else dimensions
        return PanelAssemblyBuilder(MoventoPanelDrawer().specification("drawer_01", selected,
            MoventoPilotChoice(5,14,2.5,10,"Test only; real stock/load remain unqualified"))).build()

    def test_hdf_is_captured_and_keeps_single_face_and_edge_flush_joints(self, drawer):
        proof = CaptureProof()
        proof.test_floor_is_captured_in_every_wall_without_solid_overlap(drawer)
        proof.test_wall_connector_pockets_remain_above_floor_and_edge_flush(drawer)
        proof.test_unmachined_floor_has_explicit_qualification_without_fake_cut_coverage(drawer)
        _, built = drawer
        report = PanelSetupChecker().check(built)
        expected = {part.spec.part_id:part.spec.inside_face for part in built.parts}
        assert all(expected[part["part_id"]] in part["allowed_faces"] for part in report["parts"])

    def test_hdf_choice_changes_floor_and_grooves_only(self, drawer):
        root, built = drawer
        old = GeneratedProjectModuleRuntime().execute(root, partial(self.build,
            replace(self.dimensions(),bottom_thickness_mm=16,bottom_material="ply16")))
        parts = {part.spec.part_id:part for part in built.parts}
        assert parts["bottom"].spec.local_size_mm == pytest.approx((630.6,485.6,6))
        assert parts["bottom"].spec.material_id == "HDF6"
        assert parts["left"].spec.material_id == parts["right"].spec.material_id == "ply16"
        # Each isolated project load creates fresh dataclass types; compare their values.
        assert asdict(parts["bottom"].spec.local_to_parent) == next(
            asdict(part.spec.local_to_parent) for part in old.parts if part.spec.part_id == "bottom")
        assert all(asdict(parts[part.spec.part_id].spec) == asdict(part.spec) for part in old.parts
                   if part.spec.part_id != "bottom")
        assert [asdict(j) for j in built.spec.joints] == [asdict(j) for j in old.spec.joints]
        old_ops = {op.machining_id:op for op in old.spec.machining}
        for op in built.spec.machining:
            if op.machining_id.startswith("bottom_groove_"):
                assert op.width_mm == pytest.approx(6.2)
                assert op.depth_mm == 6
            else:
                assert asdict(op) == asdict(old_ops[op.machining_id])

    def test_legacy_stock_default_is_preserved(self):
        old = MoventoPanelDimensions(661,120,657,152.5,2,-18,22,"ply16","prepared14.5","front22")
        assert old.bottom_thickness_mm == 16 and old.bottom_material == "ply16"

    @pytest.mark.parametrize("thickness", (0,5,17,float("nan"),float("inf")))
    def test_rejects_stock_outside_supported_groove_geometry(self, thickness):
        with pytest.raises(ValueError, match="6–16 mm"):
            replace(self.dimensions(),bottom_thickness_mm=thickness)

    def test_rejects_empty_selected_bottom_material(self):
        with pytest.raises(ValueError, match="material identities"):
            replace(self.dimensions(),bottom_material="")
