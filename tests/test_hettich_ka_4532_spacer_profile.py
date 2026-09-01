"""Scope: Protect the sourced KA 4532 runner and spacer sizing contract."""

from pathlib import Path

from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from hardware_asset_manifest import HardwareAssetManifest, HardwareAssetState
from hettich_ka_4532_spacer_drawer_box_profile import (
    HettichKa4532SpacerDrawerBoxProfileAdapter,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class TestHettichKa4532SpacerManifest:
    """Keep both exact purchased components discoverable without CAD bytes."""

    _SKILL_ROOT = Path(__file__).parents[1] / "aikea-build-drawers"
    _MANIFEST = (
        _SKILL_ROOT
        / "assets"
        / "hettich"
        / "ka-4532-spacer"
        / "hardware-assets.json"
    )

    def test_manifest_registers_runner_pair_and_spacer(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST)

        assert manifest.vendor == "Hettich"
        assert {asset.asset_id for asset in manifest.assets} == {
            "hettich-ka-4532-500-runner-pair",
            "hettich-13952-spacer-profile",
        }
        assert all(asset.state is HardwareAssetState.READY for asset in manifest.assets)
        assert manifest.asset("hettich-ka-4532-500-runner-pair").native_step_observation.solid_count == 4
        assert manifest.asset("hettich-13952-spacer-profile").native_step_observation.solid_count == 1

    def test_public_skill_contains_no_vendor_step_bytes(self) -> None:
        assert not tuple(self._SKILL_ROOT.rglob("*.step"))
        assert not tuple(self._SKILL_ROOT.rglob("*.stp"))


class TestHettichKa4532SpacerDrawerSizing:
    """Protect the paired side-space relationship approved in visual review."""

    def test_profile_includes_one_spacer_and_runner_per_side(self) -> None:
        profile = HETTICH_KA_4532_500_WITH_13952

        assert profile.hardware_width_per_side_mm == 37.7
        assert profile.spacer_item_number == "13952"
        assert profile.runner_item_number == "9114276"
        assert profile.minimum_cabinet_depth_mm == 504.0
        assert profile.combined_load_capacity_kg == 20.0

    def test_approved_opening_resolves_the_proven_drawer_width(self) -> None:
        sizing = HettichKa4532SpacerDrawerBoxProfileAdapter().build(
            HETTICH_KA_4532_500_WITH_13952,
            side_thickness_mm=15.0,
            front_back_thickness_mm=15.0,
            bottom_thickness_mm=9.0,
            bottom_underside_recess_mm=13.0,
            box_height_mm=170.0,
        )

        box = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(clear_width_mm=559.0, inside_depth_mm=564.0),
            sizing,
        )

        assert sizing.drawer_inside_width_reduction_mm == 105.4
        assert box.clear_inside_width_mm == 453.6
        assert box.outside_width_mm == 483.6
        assert box.outside_depth_mm == 530.0
