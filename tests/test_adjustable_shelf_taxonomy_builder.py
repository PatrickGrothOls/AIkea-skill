"""Scope: Verify adjustable shelves derive from matching side-panel support rows."""

from adjustable_shelf_taxonomy_builder import AdjustableShelfTaxonomyBuilder
from system_32_side_panel_grid import System32SidePanelGrid


class TestAdjustableShelfTaxonomyBuilder:
    """Protect shelf counts, dimensions, and support-hole alignment."""

    def test_default_shelves_use_evenly_spread_shared_rows(self) -> None:
        shelves = AdjustableShelfTaxonomyBuilder().build(
            width_mm=991.333333,
            depth_mm=564.0,
            left_side_height_mm=2266.0,
            right_side_height_mm=2266.0,
            thickness_mm=18.0,
        )

        assert [shelf.part_id for shelf in shelves] == [
            "shelf_01",
            "shelf_02",
            "shelf_03",
        ]
        assert [dict(shelf.dimensions_mm)["support_row_height"] for shelf in shelves] == [
            612.0,
            1124.0,
            1636.0,
        ]
        assert all(
            shelf.local_size_mm == (955.333333, 564.0, 18.0)
            for shelf in shelves
        )

    def test_every_shelf_uses_a_row_present_on_both_unequal_sides(self) -> None:
        pattern = System32SidePanelGrid()
        left_rows = pattern.row_heights_mm(2266.0)
        right_rows = pattern.row_heights_mm(2010.0)
        shelves = AdjustableShelfTaxonomyBuilder().build(
            width_mm=900.0,
            depth_mm=550.0,
            left_side_height_mm=2266.0,
            right_side_height_mm=2010.0,
            thickness_mm=18.0,
        )

        for shelf in shelves:
            dimensions = dict(shelf.dimensions_mm)
            row_height = dimensions["support_row_height"]
            assert row_height in left_rows
            assert row_height in right_rows
            assert dimensions["bottom_height"] == row_height + 2.5
