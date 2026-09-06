"""Scope: Verify repeated KA 5332 drawers receive independent System 32 rows."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from hettich_ka_5332_cabinet_drawers_generator import (
    HettichKa5332CabinetDrawersGenerator,
)
from hettich_ka_5332_test_support import (
    HettichKa5332StepAssemblyLoaderTestDouble,
    TEST_HETTICH_HARDWARE_DIRECTORY,
)
from panel_hardware_reservation import PanelHardwareReservationStore


class TestHettichKa5332CabinetDrawersSystem32(unittest.TestCase):
    """Protect row snapping and shared reservations across repeated drawers."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_three_drawers_resolve_three_nodes_per_side(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory)
            project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
            (project_root / "aikea.yaml").write_text(
                yaml.safe_dump(project, sort_keys=False),
                encoding="utf-8",
            )
            AssemblyTaxonomyGenerator().generate(project, project_root)

            result = HettichKa5332CabinetDrawersGenerator(
                HettichKa5332StepAssemblyLoaderTestDouble()
            ).generate(
                project_root,
                "tall_storage_01",
                (
                    DrawerLayout("drawer_01", 100.0),
                    DrawerLayout("drawer_02", 270.0),
                    DrawerLayout("drawer_03", 430.0),
                ),
                hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY,
            )

            rows_mm = tuple(
                drawer.hardware_mounting.system_32_row_height_mm
                for drawer in result.plan.drawers
            )
            reservations = PanelHardwareReservationStore().load(
                project_root,
                "tall_storage_01",
            )

            self.assertEqual(rows_mm, (132.0, 292.0, 452.0))
            self.assertEqual(len(reservations), 6)
            self.assertEqual(
                tuple(
                    item.system_32_node_rows_mm[0]
                    for item in reservations
                    if item.side_part_id == "left_side"
                ),
                rows_mm,
            )


if __name__ == "__main__":
    unittest.main()
