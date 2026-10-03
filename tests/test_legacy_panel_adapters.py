"""Scope: Keep saved dimension-only panels working through the common construction tools."""
from types import SimpleNamespace

import cadquery as cq
import pytest

from legacy_panel_construction import LegacyPartBlankBuilder
from part_blank_builder import PartBlankBuilder
from part_construction_error import PartConstructionError
from part_cut import PartCut
from sheet_part_builder import SheetPartBuilder


class TestLegacyPanelAdapters:
    @pytest.mark.parametrize("explicit_outline", (False, True))
    def test_old_sloped_door_needs_no_new_local_size_field(self, explicit_outline):
        points = ((0, 0), (350, 0), (350, 430), (0, 600))
        part = SimpleNamespace(role="door_panel", dimensions_mm=(
            ("width", 350), ("left_height", 600), ("right_height", 430), ("thickness", 18)),
            outline_mm=tuple(SimpleNamespace(x_mm=x, height_mm=y) for x, y in points)
            if explicit_outline else ())
        expected = LegacyPartBlankBuilder().build(part).val()
        actual = PartBlankBuilder().build(part).val()
        assert actual.cut(expected).Volume() + expected.cut(actual).Volume() < 1e-6
        assert actual.Volume() == pytest.approx(350 * (600 + 430) / 2 * 18)

    def test_saved_cutter_that_misses_part_fails_common_material_check(self):
        part = SimpleNamespace(part_id="shelf", role="shelf_panel", dimensions_mm=(),
                               outline_mm=(), local_size_mm=(300, 400, 18))
        cutter = cq.Workplane("XY").circle(2).extrude(10).val()
        cut = PartCut("missing_receiver", "shelf", 1, cutter, cq.Location((500, 500, 0)))
        with pytest.raises(PartConstructionError, match="does not machine participant shelf"):
            SheetPartBuilder().build(part, (cut,))
