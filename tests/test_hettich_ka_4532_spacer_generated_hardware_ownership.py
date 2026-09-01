"""Scope: Verify generated exact runner members retain articulated ownership."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from cabinet_drawer_plan import DrawerLayout
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_4532_spacer_cabinet_drawer_generator import (
    HettichKa4532SpacerCabinetDrawerGenerator,
)
from hettich_ka_4532_spacer_geometry_provider import (
    HettichKa4532SpacerGeometryProvider,
)
from hettich_ka_4532_spacer_mounting_test_support import (
    HettichKa4532StepSetLoaderProbe,
)
from purchased_hardware_hydrator import PurchasedHardwareHydrator


class TestHettichKa4532SpacerGeneratedHardwareOwnership:
    """Protect the distinct fixed and drawer-following source-CAD frames."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_hydrates_fixed_and_moving_members_at_the_saved_depths(
        self,
        tmp_path,
    ) -> None:
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        (tmp_path / "aikea.yaml").write_text(
            yaml.safe_dump(project, sort_keys=False),
            encoding="utf-8",
        )
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        loader = HettichKa4532StepSetLoaderProbe()
        result = HettichKa4532SpacerCabinetDrawerGenerator(loader).generate(
            tmp_path,
            "tall_storage_01",
            DrawerLayout("drawer_01", 356.0, box_height_mm=150.0, box_depth_mm=500.0),
            hardware_directory=tmp_path / "hardware",
            cabinet_front_mm=0.0,
            drawer_front_mm=18.0,
        )
        assembly_loader = GeneratedAssemblyBuilderLoader()
        cabinet = assembly_loader.load_assembly(tmp_path, "tall_storage_01")
        geometry = HettichKa4532SpacerGeometryProvider(loader)
        hydrated = PurchasedHardwareHydrator(geometry).hydrate(tmp_path, cabinet)
        rendered = AssemblyTreeReviewGeometry().build(
            assembly_loader.walk(tmp_path, hydrated),
            {},
        )
        by_name = {part.name: part for part in rendered}
        bounds = {part.name: part.placed_shape().BoundingBox() for part in rendered}

        fixed = bounds["drawer_01_runner_left_fixed"]
        moving = bounds["drawer_01__drawer_01_runner_left_moving"]
        assert (fixed.ymin, fixed.ymax) == pytest.approx((2.0, 504.483917))
        assert (moving.ymin, moving.ymax) == pytest.approx((20.0, 525.04))
        reserved = result.plan.hardware_reservations[0].depth_interval_mm
        assert reserved[0] <= min(fixed.ymin, moving.ymin)
        assert reserved[1] >= max(fixed.ymax, moving.ymax)
        selectors = {
            "drawer_01_spacer_left": None,
            "drawer_01_spacer_right": None,
            "drawer_01_runner_left_fixed": "left-fixed",
            "drawer_01__drawer_01_runner_left_moving": "left-moving",
        }
        for name, selector in selectors.items():
            part = by_name[name]
            assert part.source_hardware_asset_id.startswith("hettich-")
            assert part.source_geometry_selector == selector
