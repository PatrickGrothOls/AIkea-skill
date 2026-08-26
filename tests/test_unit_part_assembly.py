"""Scope: Verify calculated panel blanks and their first-unit assembly placements."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestUnitPartAssembly(unittest.TestCase):
    """Prove every generated part remains local before explicit assembly placement."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        from unit_mockup_generator import UnitMockupGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        self.generator = UnitMockupGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_every_flat_part_is_built_in_its_own_sheet_frame(self) -> None:
        spec, parts = self._build(self.project)
        local_sizes = {
            "left_side": (spec.depth_mm, 2284.0, 18.0),
            "right_side": (spec.depth_mm, 2284.0, 18.0),
            "back_panel": (spec.width_mm, 2284.0, 6.0),
            "door_panel": (spec.door_width_mm, 2384.0, 18.0),
            "top_panel_01": (spec.width_mm, spec.depth_mm, 18.0),
        }

        for part in parts:
            bounds = part.solid.val().BoundingBox()
            self.assert_bounds(
                bounds,
                (0.0, local_sizes[part.name][0], 0.0, local_sizes[part.name][1], 0.0, local_sizes[part.name][2]),
            )
            self.assertTrue(part.solid.val().isValid())

    def test_flat_part_placements_close_the_calculated_cabinet_bounds(self) -> None:
        spec, parts = self._build(self.project)
        expected = {
            "left_side": (0.0, 18.0, 0.0, 582.0, 100.0, 2384.0),
            "right_side": (spec.width_mm - 18.0, spec.width_mm, 0.0, 582.0, 100.0, 2384.0),
            "back_panel": (0.0, spec.width_mm, 576.0, 582.0, 100.0, 2384.0),
            "door_panel": (-17.0, 1.0, -spec.door_width_mm, 0.0, 0.0, 2384.0),
            "top_panel_01": (0.0, spec.width_mm, 0.0, 582.0, 2366.0, 2384.0),
        }

        for part in parts:
            self.assert_bounds(part.placed_shape().BoundingBox(), expected[part.name])

    def test_profile_unit_builds_every_top_segment_and_shaped_door_point(self) -> None:
        project = self.project
        project["measured_space"]["top_boundary"] = "measured_profile"
        project["measured_space"]["height_measurements"] = [
            {"distance_from_left": 0, "height_from_floor": 240},
            {"distance_from_left": 75, "height_from_floor": 240},
            {"distance_from_left": 300, "height_from_floor": 180},
        ]
        spec, parts = self._build(project)
        door = spec.part("door_panel")

        self.assertEqual(
            [part.name for part in parts],
            ["left_side", "right_side", "back_panel", "door_panel", "top_panel_01", "top_panel_02"],
        )
        self.assertEqual(len(door.outline_mm), 5)
        self.assertAlmostEqual(door.outline_mm[3].x_mm, 739.0)
        self.assertTrue(all(part.solid.val().isValid() for part in parts))

    def _build(self, project: dict):
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        spec = self.generator.loader.load_first(self.project_root, project)
        return spec, self.generator.geometry.build(spec)

    def assert_bounds(self, bounds, expected: tuple[float, ...]) -> None:
        actual = (bounds.xmin, bounds.xmax, bounds.ymin, bounds.ymax, bounds.zmin, bounds.zmax)
        for value, target in zip(actual, expected):
            self.assertAlmostEqual(value, target, places=5)
