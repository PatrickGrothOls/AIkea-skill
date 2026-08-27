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

    def test_deck_and_frame_close_the_overall_base_dimensions(self) -> None:
        decks = [part for part in self.base.parts if part.role == "base_deck"]
        rails = [part for part in self.base.parts if part.role == "base_rail"]
        braces = [part for part in self.base.parts if part.role == "base_brace"]

        assert len(decks) == 2
        assert len(rails) == 4
        assert len(braces) == 13
        assert sum(part.local_size_mm[0] for part in decks) == 2978.0
        assert {part.local_size_mm[1] for part in decks} == {582.0}
        assert {part.local_size_mm[1] for part in rails} == {82.0}
        assert {part.local_size_mm[:2] for part in braces} == {(546.0, 82.0)}

    def test_brace_centers_include_module_ends_and_stay_within_spacing(self) -> None:
        for module_index, module in enumerate(self.base.modules, start=1):
            brace_prefix = f"brace_{module_index:02d}_"
            positions = [
                dict(part.dimensions_mm)["center_x"]
                for part in self.base.parts
                if part.part_id.startswith(brace_prefix)
            ]
            assert positions[0] == 9.0
            assert positions[-1] == module.width_mm - 9.0
            assert max(
                right - left for left, right in zip(positions, positions[1:])
            ) <= 320.0

    def test_every_brace_has_paired_cabineo_joints_to_both_rails(self) -> None:
        corners = [
            joint for joint in self.base.joints if joint.purpose == "base_frame_corner"
        ]

        assert len(corners) == 26
        assert all(joint.joint_type == "cabineo" for joint in corners)
        assert all(joint.source_part_id.startswith("brace_") for joint in corners)
        assert all(joint.source_face == ">Z" for joint in corners)
        assert all(joint.connector_layout == "bounded_spacing" for joint in corners)
        assert {
            (joint.target_part_id.split("_")[0], joint.source_edge)
            for joint in corners
        } == {("front", "<X"), ("back", ">X")}
        for brace in {
            joint.source_part_id for joint in corners
        }:
            assert {
                joint.target_part_id.split("_")[0]
                for joint in corners
                if joint.source_part_id == brace
            } == {"front", "back"}

    def test_module_seam_is_an_explicit_assembly_relationship(self) -> None:
        seams = [
            joint for joint in self.base.joints if joint.purpose == "base_module_seam"
        ]

        assert len(seams) == 1
        assert seams[0].participant_ids == (
            "deck_01",
            "deck_02",
            "front_rail_01",
            "front_rail_02",
            "back_rail_01",
            "back_rail_02",
        )
