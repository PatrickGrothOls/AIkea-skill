"""Scope: Verify one visually complete cabinet is built and exported by CadQuery."""

from __future__ import annotations

from importlib.util import find_spec
import json
from pathlib import Path
import struct
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


class GlbTestDocument:
    """Read the CadQuery GLB structure needed to verify its named assembly."""

    def __init__(self, path: Path) -> None:
        data = path.read_bytes()
        magic, version, total_length = struct.unpack_from("<4sII", data)
        if magic != b"glTF" or version != 2 or total_length != len(data):
            raise AssertionError("CadQuery did not produce a valid GLB container")
        json_length, json_kind = struct.unpack_from("<I4s", data, 12)
        if json_kind != b"JSON":
            raise AssertionError("GLB is missing its JSON document")
        payload = data[20 : 20 + json_length].decode("utf-8").rstrip(" \0")
        self.document = json.loads(payload)

    @property
    def node_names(self) -> set[str]:
        return {node["name"] for node in self.document["nodes"] if "name" in node}


@unittest.skipUnless(find_spec("cadquery"), "requires the project's CadQuery environment")
class TestUnitMockupGenerator(unittest.TestCase):
    """Keep the visual checkpoint as one valid CadQuery cabinet assembly."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"
    _PART_NAMES = {
        "left_side",
        "right_side",
        "back_panel",
        "door_panel",
        "shelf_01",
        "shelf_02",
        "shelf_03",
        "top_panel_01",
    }

    def setUp(self) -> None:
        from unit_mockup_generator import UnitMockupGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = UnitMockupGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_generates_only_the_first_saved_assembly(self) -> None:
        result = self.generator.generate_first(self.project_root, self.project)

        expected = self.project_root / "assemblies/tall_storage_01/tall_storage_01.glb"
        self.assertEqual(result.assembly_id, "tall_storage_01")
        self.assertEqual(result.glb_path, expected)
        self.assertTrue(expected.is_file())
        self.assertFalse(
            (self.project_root / "assemblies/tall_storage_02/tall_storage_02.glb").exists()
        )
        self.assertFalse(
            (self.project_root / "assemblies/tall_storage_03/tall_storage_03.glb").exists()
        )

    def test_glb_contains_the_named_cadquery_part_set(self) -> None:
        result = self.generator.generate_first(self.project_root, self.project)

        glb = GlbTestDocument(result.glb_path)

        self.assertTrue(self._PART_NAMES.issubset(glb.node_names))

    def test_cadquery_solids_are_valid_and_match_the_calculated_unit(self) -> None:
        built_assembly = self.generator.loader.load_first(self.project_root, self.project)
        parts = self.generator.geometry.build(built_assembly)
        bounds = [part.placed_shape().BoundingBox() for part in parts]

        self.assertEqual(
            [part.spec.part_id for part in built_assembly.parts],
            [
                "left_side",
                "right_side",
                "back_panel",
                "door_panel",
                "shelf_01",
                "shelf_02",
                "shelf_03",
                "top_panel_01",
            ],
        )
        self.assertTrue(all(part.solid.val().isValid() for part in built_assembly.parts))
        self.assertEqual({part.name for part in parts}, self._PART_NAMES)
        self.assertTrue(all(part.solid.val().isValid() for part in parts))
        self.assertAlmostEqual(min(bound.xmin for bound in bounds), -17.0)
        self.assertAlmostEqual(
            min(bound.ymin for bound in bounds),
            -989.3333333333334,
        )
        self.assertAlmostEqual(min(bound.zmin for bound in bounds), 82.0)
        self.assertAlmostEqual(max(bound.xmax for bound in bounds), 991.3333333333334)
        self.assertAlmostEqual(max(bound.ymax for bound in bounds), 582.0)
        self.assertAlmostEqual(max(bound.zmax for bound in bounds), 2384.0)
