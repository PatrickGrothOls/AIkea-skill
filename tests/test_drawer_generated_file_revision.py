"""Scope: Verify generated drawer files revise safely without overwriting local work."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from cabinet_drawer_generator import CabinetDrawerGenerator
from cabinet_drawer_plan import DrawerLayout
from drawer_generated_file_record import DrawerGeneratedFileRecord
from drawer_hardware_test_support import (
    DrawerHardwareSetVerifierFactoryTestDouble,
    TEST_HARDWARE_DIRECTORY,
)


class TestDrawerGeneratedFileRevision(unittest.TestCase):
    """Protect the boundary between generator-owned files and client edits."""

    FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.project_root = Path(self.temporary_directory.name)
        project = yaml.safe_load(self.FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, self.project_root)
        self.parent = self.project_root / "assemblies/tall_storage_01"
        self.taxonomy_record = self.project_root / "assemblies/generated-files.json"
        self.original_taxonomy_record = self.taxonomy_record.read_text(
            encoding="utf-8"
        )
        self.generator = CabinetDrawerGenerator(
            DrawerHardwareSetVerifierFactoryTestDouble()
        )

    def test_changed_bottom_height_revises_unchanged_generated_files(self) -> None:
        self._generate(bottom_height_mm=356.0)
        result = self._generate(bottom_height_mm=400.0)

        layout = yaml.safe_load(
            (self.parent / "drawer-layout.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(layout["drawers"][0]["bottom_height_mm"], 400.0)
        self.assertEqual(result.plan.origin_in_parent_mm, (24.0, 18.0, 500.0))
        self.assertEqual(
            set(result.written_paths),
            {
                Path("assemblies/tall_storage_01/drawer-layout.yaml"),
                Path("assemblies/tall_storage_01/drawer_installation.py"),
            },
        )
        self.assertTrue(
            (
                self.project_root
                / DrawerGeneratedFileRecord.path_for("tall_storage_01")
            ).is_file()
        )
        self.assertEqual(
            self.taxonomy_record.read_text(encoding="utf-8"),
            self.original_taxonomy_record,
        )

    def test_manual_edit_blocks_the_complete_revision(self) -> None:
        self._generate(bottom_height_mm=356.0)
        child_spec = self.parent / "drawers/drawer_01/spec.py"
        child_spec.write_text(
            child_spec.read_text(encoding="utf-8") + "# client change\n",
            encoding="utf-8",
        )
        original_layout = (self.parent / "drawer-layout.yaml").read_text(
            encoding="utf-8"
        )

        with self.assertRaisesRegex(
            AssemblyTaxonomyConflict,
            "drawers/drawer_01/spec.py",
        ):
            self._generate(bottom_height_mm=400.0)

        self.assertEqual(
            (self.parent / "drawer-layout.yaml").read_text(encoding="utf-8"),
            original_layout,
        )
        self.assertTrue(
            child_spec.read_text(encoding="utf-8").endswith("# client change\n")
        )

    def _generate(self, bottom_height_mm: float):
        return self.generator.generate(
            self.project_root,
            "tall_storage_01",
            DrawerLayout("drawer_01", bottom_height_mm=bottom_height_mm),
            hardware_directory=TEST_HARDWARE_DIRECTORY,
        )


if __name__ == "__main__":
    unittest.main()
