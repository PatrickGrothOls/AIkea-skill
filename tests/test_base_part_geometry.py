"""Scope: Verify generated structural-base parts are valid local CadQuery solids."""

from __future__ import annotations

import importlib
from importlib.util import find_spec
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestBasePartGeometry(unittest.TestCase):
    """Build every planned deck, rail, and brace from its generated local spec."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        self.built = self._load_base()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_every_base_part_matches_its_local_manufacturing_size(self) -> None:
        self.assertEqual(len(self.built.parts), 19)
        for part in self.built.parts:
            bounds = part.solid.val().BoundingBox()
            expected = part.spec.local_size_mm
            self.assertAlmostEqual(bounds.xlen, expected[0])
            self.assertAlmostEqual(bounds.ylen, expected[1])
            self.assertAlmostEqual(bounds.zlen, expected[2])
            self.assertTrue(part.solid.val().isValid())

    def _load_base(self):
        sys.path.insert(0, str(self.project_root))
        try:
            module = importlib.import_module("assemblies.base_01.builder")
            return module.BUILDER.build()
        finally:
            sys.path.remove(str(self.project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)


if __name__ == "__main__":
    unittest.main()
