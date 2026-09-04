"""Scope: Verify one exact KA 4532 spacer drawer becomes a generated feature."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_4532_spacer_cabinet_drawer_generator import (
    HettichKa4532SpacerCabinetDrawerGenerator,
)
from hettich_ka_4532_spacer_mounting_test_support import (
    HettichKa4532StepSetLoaderProbe,
)


class TestHettichKa4532SpacerCabinetDrawerGenerator:
    """Protect generated ownership, exact identities, and the proof-only gate."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_generates_one_recursive_child_and_exact_purchased_instances(
        self,
        tmp_path,
    ) -> None:
        loader = self._project(tmp_path)
        result = self._generate(tmp_path, loader)
        cabinet = GeneratedAssemblyBuilderLoader().load_assembly(
            tmp_path,
            "tall_storage_01",
        )

        assert loader.hardware_roots == [tmp_path / "hardware"]
        assert len(cabinet.child_assemblies) == 1
        drawer = cabinet.child_assemblies[0].assembly
        assert len(drawer.parts) == 5
        assert len(cabinet.purchased_hardware) == 4
        specs = tuple(item.spec for item in cabinet.purchased_hardware)
        runners = tuple(item for item in specs if "runner" in item.hardware_id)
        spacers = tuple(item for item in specs if "spacer" in item.hardware_id)
        moving = tuple(item.spec for item in drawer.purchased_hardware)
        assert tuple(item.geometry_selector for item in runners) == (
            "left-fixed",
            "right-fixed",
        )
        assert tuple(item.geometry_selector for item in moving) == (
            "left-moving",
            "right-moving",
        )
        assert {item.hardware_asset_id for item in spacers} == {
            "hettich-13952-spacer-profile"
        }
        assert spacers[0].local_to_parent != spacers[1].local_to_parent
        assert result.plan.hardware_step.spacer_solid is not None
        installation = self._installation(tmp_path)
        assert installation.MOUNTING_PLAN.spacer_left_in_cabinet.origin_mm == (
            18.0,
            10.0,
            454.0,
        )

    def test_saves_feature_registration_limits_and_explicit_machining_blocker(
        self,
        tmp_path,
    ) -> None:
        self._generate(tmp_path, self._project(tmp_path))
        root = tmp_path / "assemblies/tall_storage_01"
        layout = yaml.safe_load((root / "drawer-layout.yaml").read_text())
        authority = yaml.safe_load(
            (root / "drawers/machining-authority.json").read_text()
        )
        features = yaml.safe_load((root / "features.json").read_text())

        assert layout["purchased_set"]["spacer"]["instances"] == 2
        assert layout["purchased_set"]["combined_load_capacity_kg"] == 20.0
        assert layout["purchased_set"]["minimum_cabinet_depth_mm"] == 504.0
        assert authority["manufacturing_authority"] is False
        assert authority["cabinet_id"] == "tall_storage_01"
        assert authority["reason"] == (
            "blocked_missing_longer_screw_and_cabinet_pilot"
        )
        resolved = authority["resolved_authority"]
        assert resolved["rail_fixed_member_hole_pattern"][
            "cabinet_depth_axes_from_front_mm"
        ] == [37.0, 165.0, 261.0, 325.0]
        assert resolved["spacer_support_corridor"][
            "preformed_spacer_openings_used"
        ] is False
        assert authority["missing_authority"] == [
            "longer_rail_through_spacer_screw_identity",
            "longer_rail_through_spacer_screw_length_mm",
            "cabinet_pilot_diameter_mm",
            "cabinet_pilot_depth_mm",
        ]
        assert features["features"][0]["module"] == "drawers.feature"
        assert features["features"][0]["review_module"] == "drawers.review"
        assert "drawer_01/left_side" in features["features"][0][
            "affected_manufactured_part_paths"
        ]

    def test_keeps_repetition_disabled_until_this_cabinet_is_proven(
        self,
        tmp_path,
    ) -> None:
        loader = self._project(tmp_path)
        self._generate(tmp_path, loader)

        with pytest.raises(ValueError, match="repetition remains disabled"):
            HettichKa4532SpacerCabinetDrawerGenerator(loader).generate(
                tmp_path,
                "tall_storage_01",
                DrawerLayout("drawer_02", 356.0, box_depth_mm=500.0),
                hardware_directory=tmp_path / "hardware",
                cabinet_front_mm=0.0,
                drawer_front_mm=18.0,
            )

    def _project(self, root):
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        (root / "aikea.yaml").write_text(
            yaml.safe_dump(project, sort_keys=False),
            encoding="utf-8",
        )
        AssemblyTaxonomyGenerator().generate(project, root)
        return HettichKa4532StepSetLoaderProbe()

    def _generate(self, root, loader):
        return HettichKa4532SpacerCabinetDrawerGenerator(loader).generate(
            root,
            "tall_storage_01",
            DrawerLayout("drawer_01", 356.0, box_height_mm=150.0, box_depth_mm=500.0),
            hardware_directory=root / "hardware",
            cabinet_front_mm=0.0,
            drawer_front_mm=18.0,
        )

    def _installation(self, root):
        from generated_project_module_runtime import GeneratedProjectModuleRuntime
        import importlib

        return GeneratedProjectModuleRuntime().execute(
            root,
            lambda: importlib.import_module(
                "assemblies.tall_storage_01.drawer_installation"
            ),
        )

__all__ = ["TestHettichKa4532SpacerCabinetDrawerGenerator"]
