"""Scope: Verify every modular door-and-plinth choice in placed CadQuery solids."""

from importlib.util import find_spec
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires CadQuery")
class TestDoorAndPlinthGeometry(unittest.TestCase):
    """Prove the four choices reach valid local and assembled geometry."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"
    _CASES = (
        ("floor", "flush", 0, 0, 0),
        ("floor", "recessed", 60, 0, 60),
        ("plinth", "flush", 0, 82, 0),
        ("plinth", "recessed", 60, 82, 60),
    )

    def test_selected_geometry_is_built_and_position_checked(self) -> None:
        from base_review_generator import BaseReviewGenerator

        for case in self._CASES:
            with self.subTest(door_bottom=case[0], plinth_front=case[1]):
                self._assert_case(BaseReviewGenerator(), case)

    def _assert_case(self, generator, case: tuple) -> None:
        door_bottom, plinth_front, recess_mm, door_z_mm, front_y_mm = case
        with TemporaryDirectory() as directory:
            project_root = Path(directory)
            project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
            project["design_settings"]["doors"]["bottom"] = door_bottom
            project["design_settings"]["base"].update(
                {"front": plinth_front, "recess": recess_mm / 10}
            )
            AssemblyTaxonomyGenerator().generate(project, project_root)

            result = generator.generate(project_root, project)
            report = json.loads(result.position_report_path.read_text(encoding="utf-8"))
            built_base = generator.loader.load_assembly(project_root, "base_01")
            base_parts = generator.base_geometry.build(built_base)
            built_cabinet = generator.loader.load_first(project_root, project)
            cabinet_parts = generator.cabinet_geometry.build(built_cabinet)
            front = next(part for part in base_parts if part.name == "front_rail_01")
            brace = next(part for part in base_parts if part.name == "brace_01_01")
            door = next(part for part in cabinet_parts if part.name == "door_panel")

            self.assertEqual(report["status"], "valid")
            self.assertAlmostEqual(door.placed_shape().BoundingBox().zmin, door_z_mm)
            self.assertAlmostEqual(front.placed_shape().BoundingBox().ymin, front_y_mm)
            self.assertAlmostEqual(
                brace.placed_shape().BoundingBox().ymin,
                front_y_mm + 18,
            )
            self.assertAlmostEqual(brace.placed_shape().BoundingBox().ymax, 564)
            self.assertTrue(
                all(part.solid.val().isValid() for part in (*base_parts, *cabinet_parts))
            )
