"""Scope: Verify fitted doors become registered recursive assembly features."""

from __future__ import annotations

from dataclasses import replace
import importlib
import json
from pathlib import Path
import sys

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
from door_hinge_plan import DoorHingePlacement, DoorHingePlan
from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY


class TestDoorFeatureGeneration:
    """Protect saved machining plans and exact hardware tree ownership."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_generates_repeatable_door_feature_and_hardware_specs(self, tmp_path) -> None:
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        assembly = CabinetAssemblySpecLoader().load(tmp_path, "tall_storage_01")
        plan = self._plan(assembly)
        installation = (
            tmp_path
            / "assemblies/tall_storage_01/door_hinges/installation.json"
        )
        plan.write(installation)
        generator = CabinetDoorFeatureGenerator()

        generator.generate(tmp_path, assembly, plan, RIEX_NC70_FULL_OVERLAY)
        generator.generate(tmp_path, assembly, plan, RIEX_NC70_FULL_OVERLAY)

        root = tmp_path / "assemblies/tall_storage_01"
        assert (root / "door_hinges/feature.py").is_file()
        assert (root / "door_hinges/review.py").is_file()
        assert (root / "with_door_builder.py").is_file()
        compile(
            (root / "door_hinges/feature.py").read_text(encoding="utf-8"),
            "door_hinges/feature.py",
            "exec",
        )
        manifest = json.loads((root / "features.json").read_text(encoding="utf-8"))
        assert manifest["features"] == [
            {
                "module": "door_hinges.feature",
                "order": 20,
                "review_module": "door_hinges.review",
                "affected_manufactured_part_paths": [
                    "door_panel",
                    "left_side",
                ],
            }
        ]
        specification, hardware, loaded_plan, tree = self._load_generated(tmp_path)
        assert loaded_plan.PLAN == plan
        assert len(hardware.DOOR_HARDWARE) == 2
        hinge, plate = hardware.DOOR_HARDWARE
        assert hinge.hardware_asset_id == "riex-nc70-f000001-closed"
        assert plate.hardware_asset_id == "riex-nc70-f000049-h0-euroscrew-plate"
        assert hinge.local_to_parent.origin_in_parent.z_mm == (
            assembly.door_bottom_mm + 500.0
        )

        parts = tuple(specification.BuiltPart(part, object()) for part in assembly.parts)
        door_spec = replace(
            assembly,
            purchased_hardware=assembly.purchased_hardware + hardware.DOOR_HARDWARE,
        )
        built_hardware = tuple(
            specification.BuiltPurchasedHardware(item, None)
            for item in hardware.DOOR_HARDWARE
        )
        built = specification.BuiltAssembly(
            door_spec,
            parts,
            assembly.joints,
            purchased_hardware=built_hardware,
        )
        visits = tree.AssemblyTreeWalker().walk(built)
        assert sum(type(item).__name__ == "AssemblyTreeHardware" for item in visits) == 2

    def _plan(self, assembly) -> DoorHingePlan:
        door = {name: float(value) for name, value in assembly.part("door_panel").dimensions_mm}
        return DoorHingePlan(
            assembly_id=assembly.assembly_id,
            profile_id=RIEX_NC70_FULL_OVERLAY.profile_id,
            relationship="full_overlay",
            hinge_side=DoorHingeSide.LEFT,
            door_width_mm=door["width"],
            door_height_mm=door["left_height"],
            door_thickness_mm=door["thickness"],
            door_mass_kg=20.0,
            overlay_mm=17.0,
            placements=(DoorHingePlacement("hinge_01", 500.0, 500.0, (480.0, 512.0)),),
            compatibility_issues=(),
        )

    def _load_generated(self, project_root: Path):
        sys.path.insert(0, str(project_root))
        try:
            specification = importlib.import_module("assemblies.specification")
            hardware = importlib.import_module(
                "assemblies.tall_storage_01.door_hinges.hardware"
            )
            plan = importlib.import_module("assemblies.tall_storage_01.door_hinges.plan")
            tree = importlib.import_module("assemblies.assembly_tree")
            return specification, hardware, plan, tree
        finally:
            sys.path.remove(str(project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
