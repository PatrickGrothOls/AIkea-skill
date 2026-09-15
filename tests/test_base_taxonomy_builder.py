"""Scope: Verify the structural base derives manufacturable modules and parts."""

from base_taxonomy_builder import BaseTaxonomyBuilder
from cnc_work_area import CNC_2500_X_2000_8MM


class TestBaseTaxonomyBuilder:
    """Protect the base envelope, module splits, support grid, and seam ownership."""

    def setup_method(self) -> None:
        self.base = BaseTaxonomyBuilder().build(
            (
                (10.0, 1001.3333333333334),
                (1003.3333333333334, 1994.6666666666667),
                (1996.6666666666667, 2988.0),
            ),
            depth_mm=582.0,
            height_mm=100.0,
            panel_thickness_mm=18.0,
            plinth_front="flush",
            plinth_recess_mm=0.0,
        )

    def test_base_splits_at_a_cabinet_gap(self) -> None:
        assert self.base.width_mm == 2978.0
        assert [module.module_id for module in self.base.modules] == [
            "base_module_01",
            "base_module_02",
        ]
        assert self.base.modules[0].end_x_mm == 992.3333333333334
        assert self.base.modules[1].start_x_mm == 992.3333333333334
        assert self.base.modules[1].end_x_mm == 2978.0

    def test_every_base_part_fits_the_cnc_work_area(self) -> None:
        assert all(
            CNC_2500_X_2000_8MM.fits(
                part.local_size_mm[0],
                part.local_size_mm[1],
            )
            for part in self.base.parts
        )

    def test_deck_and_kickboard_close_the_overall_base_dimensions(self):
        decks = [p for p in self.base.parts if p.role == "base_deck"]
        fronts = [p for p in self.base.parts if p.role == "base_kickboard"]
        assert len(decks) == len(fronts) == 2
        assert len(self.base.parts) == 4
        assert sum(p.local_size_mm[0] for p in decks) == 2978
        assert {p.local_size_mm[1] for p in fronts} == {82}
        assert not any(p.role in {"base_rail","base_brace"} for p in self.base.parts)

    def test_module_seam_and_kickboard_attachment_remain_explicit(self):
        seams = [j for j in self.base.joints if j.purpose == "base_module_seam"]
        assert len(seams) == 1
        assert seams[0].participant_ids == ("deck_01","deck_02")
        assert len([j for j in self.base.joints if j.purpose == "select_korrekt_kickboard_clips"]) == 2
        assert all(j.joint_type == "unresolved" for j in self.base.joints)
