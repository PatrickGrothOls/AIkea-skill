"""Scope: Check that thin bake charts keep pixel coverage, padding and non-overlap."""

import random
from texture_shelf_layout import TextureShelfLayout


class TestTextureShelfLayout:
    def assert_valid(self, layout, spans, scale):
        rectangles, used = layout.pack(spans, scale)
        assert len(rectangles) == len(spans)
        assert used <= layout.size
        padding = layout.padding
        boxes = []
        for x, y, width, height in rectangles.values():
            assert min(width, height) >= layout.minimum
            box = (x-padding, y-padding, x+width+padding, y+height+padding)
            assert min(box) >= 0 and max(box) <= layout.size
            boxes.append(box)
        for index, first in enumerate(boxes):
            for second in boxes[index+1:]:
                assert (first[2] <= second[0] or second[2] <= first[0]
                        or first[3] <= second[1] or second[3] <= first[1])

    def test_subpixel_edges_stay_wide_enough_after_scaling(self):
        self.assert_valid(TextureShelfLayout(512), [(0.80286, 310), (100, 120), (0.05, 90)], 0.5)

    def test_many_differently_sized_charts_keep_padding(self):
        randomizer = random.Random(18)
        spans = [(randomizer.uniform(0.05, 20), randomizer.uniform(10, 80)) for _ in range(80)]
        self.assert_valid(TextureShelfLayout(1024), spans, 0.9)

    def test_insufficient_budget_does_not_shrink_below_minimum(self):
        assert TextureShelfLayout(16).pack([(0.1, 0.1)], 0.01) is None

    def test_oversize_and_exhausted_atlas_are_reported(self):
        layout = TextureShelfLayout(64)
        assert layout.pack([(49, 2)], 1) is None
        assert layout.pack([(48, 48), (1, 1)], 1) is None
