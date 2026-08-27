"""Scope: Verify incorrect cabinet-to-base placement cannot pass visual review."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestCabinetBasePositionChecker(unittest.TestCase):
    """Prove the review gate detects a wrong local-to-assembly height."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        from base_review_generator import BaseReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = BaseReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_rejects_a_carcass_placed_at_the_base_floor(self) -> None:
        import cadquery as cq

        from unit_mockup import MockupPart

        built_base = self.generator.loader.load_assembly(self.project_root, "base_01")
        built_cabinet = self.generator.loader.load_first(
            self.project_root,
            self.project,
        )
        base_parts = self.generator.base_geometry.build(built_base)
        review_base_parts = self.generator._first_module_parts(base_parts)
        cabinet_parts = self.generator.cabinet_geometry.build(built_cabinet)
        lowering = cq.Location(cq.Vector(0.0, 0.0, -100.0))
        misplaced_parts = tuple(
            part
            if part.name == "door_panel"
            else MockupPart(
                part.name,
                part.solid,
                lowering * part.location,
                part.color,
            )
            for part in cabinet_parts
        )
        next_spec = self.generator.spec_loader.load(
            self.project_root,
            "tall_storage_02",
        )

        report = self.generator.position_checker.check(
            built_base,
            built_cabinet,
            base_parts,
            review_base_parts,
            misplaced_parts,
            next_spec,
        )

        self.assertFalse(report.is_valid)
        self.assertIn(
            "cabinet sides meet the base top",
            report.failed_check_names(),
        )
        self.assertIn(
            "cabinet carcass does not overlap base material",
            report.failed_check_names(),
        )


if __name__ == "__main__":
    unittest.main()
