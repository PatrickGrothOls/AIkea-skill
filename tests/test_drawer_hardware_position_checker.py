"""Scope: Prove downloaded MOVENTO hardware fits its saved cabinet frames."""

from importlib.util import find_spec
import json
import os
from pathlib import Path
from types import SimpleNamespace
from tempfile import TemporaryDirectory
import unittest

import yaml

from hardware_cabinet_frame import HardwareCabinetFrameComposer


class TestHardwareCabinetFrameComposer(unittest.TestCase):
    """Protect local hardware placement through a rotated owner frame."""

    def test_composes_origin_and_native_axes_into_cabinet_coordinates(self) -> None:
        owner = self._placement(
            (10.0, 20.0, 30.0),
            ((0.0, 1.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
        )
        hardware = self._placement(
            (2.0, 3.0, 4.0),
            ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, -1.0, 0.0)),
        )

        frame = HardwareCabinetFrameComposer().compose(hardware, owner)

        self.assertEqual(frame.origin_mm, (7.0, 22.0, 34.0))
        self.assertEqual(frame.x_axis, (0.0, 1.0, 0.0))
        self.assertEqual(frame.y_axis, (0.0, 0.0, 1.0))
        self.assertEqual(frame.z_axis, (1.0, 0.0, 0.0))

    def _placement(self, origin, axes):
        directions = tuple(SimpleNamespace(x=x, y=y, z=z) for x, y, z in axes)
        return SimpleNamespace(
            origin_in_parent=SimpleNamespace(
                x_mm=origin[0], y_mm=origin[1], z_mm=origin[2]
            ),
            axis_basis=SimpleNamespace(
                local_x_in_parent=directions[0],
                local_y_in_parent=directions[1],
                local_z_in_parent=directions[2],
            ),
        )


@unittest.skipUnless(
    find_spec("cadquery") and os.environ.get("AIKEA_BLUM_DOWNLOAD_DIR"),
    "requires CadQuery and AIKEA_BLUM_DOWNLOAD_DIR",
)
class TestDownloadedDrawerHardwarePosition(unittest.TestCase):
    """Protect closed-frame alignment and named manufacturer CAD overlaps."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_exact_hardware_fits_the_first_generated_cabinet(self) -> None:
        from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
        from cabinet_drawer_generator import CabinetDrawerGenerator
        from cabinet_drawer_plan import DrawerLayout
        from cabinet_review_geometry import CabinetReviewGeometry
        from door_review_state import DoorReviewState
        from drawer_hardware_position_checker import DrawerHardwarePositionChecker
        from drawer_hardware_set_verifier import DrawerHardwareSetVerifier
        from drawer_review_geometry import DrawerReviewGeometry
        from drawer_review_state import DrawerReviewState
        from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
        from movento_runner_catalog import MOVENTO_760H5000S

        with TemporaryDirectory() as path:
            project_root = Path(path)
            project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
            hardware_directory = Path(os.environ["AIKEA_BLUM_DOWNLOAD_DIR"])
            AssemblyTaxonomyGenerator().generate(project, project_root)
            CabinetDrawerGenerator().generate(
                project_root,
                "tall_storage_01",
                DrawerLayout("drawer_01", bottom_height_mm=356.0),
                hardware_directory=hardware_directory,
            )
            cabinet = GeneratedAssemblyBuilderLoader().load_assembly(
                project_root,
                "tall_storage_01",
                "with_drawers_builder",
            )
            hardware = DrawerHardwareSetVerifier(hardware_directory).verify(
                MOVENTO_760H5000S
            )
            report = DrawerHardwarePositionChecker().check(
                cabinet,
                CabinetReviewGeometry().build(cabinet, DoorReviewState.CLOSED),
                DrawerReviewGeometry().build(cabinet, DrawerReviewState.CLOSED),
                hardware,
            )
            report_path = project_root / "drawer-hardware-position-check.json"
            report.write(report_path)

            self.assertTrue(report.is_valid, report.failed_check_names())
            self.assertEqual(
                report.fixing_depths_from_drawer_front_mm,
                (37.0, 293.0),
            )
            self.assertTrue(
                all(contact["contact"] for contact in report.cabinet_side_contacts)
            )
            self.assertTrue(
                all(
                    relation["front_distance_mm"] == 0.0
                    and relation["front_overlap_volume_mm3"] == 0.0
                    and abs(relation["bottom_clearance_mm"] - 13.2) <= 1e-6
                    for relation in report.locking_device_mounting_relations
                )
            )
            self.assertEqual(
                {
                    (overlap["hardware_id"], overlap["classification"])
                    for overlap in report.wood_overlaps
                },
                {
                    ("runner_left", "rear_preparation_required"),
                    ("runner_right", "rear_preparation_required"),
                },
            )
            self.assertTrue(
                all(
                    overlap["classification"] == "manufacturer_engagement_overlap"
                    and overlap["overlap_volume_mm3"] > 0.0
                    for overlap in report.manufacturer_engagement_overlaps
                )
            )
            self.assertEqual(
                json.loads(report_path.read_text(encoding="utf-8"))["status"],
                "valid",
            )


if __name__ == "__main__":
    unittest.main()
