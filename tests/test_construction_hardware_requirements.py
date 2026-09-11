"""Scope: Bind installed purchased items to their exact feature installation evidence."""

from dataclasses import replace

import cadquery as cq

from construction_extension_fixture import ConstructionExtensionFixture
from construction_feature_qualification import ConstructionFeatureQualification
from construction_requirement_checker import ConstructionRequirementChecker
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestConstructionHardwareRequirements:
    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    def test_selected_hardware_can_be_covered_by_its_installation_feature(self, tmp_path, contracts):
        project = self._project(tmp_path, contracts)
        project.write_evidence(hardware=("pin",))
        _, features = self._resolve(project)
        assert "unit_01/hardware:pin" in features["unit_01/feature:paired_pocket.feature"]
        assert all(check.passed for check in ConstructionRequirementChecker().check(project.visits, features))

    def test_evidence_cannot_claim_another_hardware_item(self, tmp_path, contracts):
        project = self._project(tmp_path, contracts)
        project.write_evidence(hardware=("wrong_pin",))
        _, features = self._resolve(project)
        assert not ConstructionRequirementChecker().check(project.visits, features)[0].passed

    def test_product_change_invalidates_installation_evidence(self, tmp_path, contracts):
        project = self._project(tmp_path, contracts)
        project.write_evidence(hardware=("pin",))
        visit = project.visits[-1]
        changed = replace(visit.hardware, spec=replace(visit.hardware.spec, product_code="different-product"))
        project.visits = (*project.visits[:-1], replace(visit, hardware=changed))
        assert not self._resolve(project)[1]

    def _project(self, root, contracts):
        values, _ = contracts
        project = ConstructionExtensionFixture().build(root, contracts)
        hardware = values.PurchasedHardwareSpec(
            "pin", "Test fixture", "test-pin", "fixture-pin", values.IDENTITY_LOCAL_TO_PARENT)
        requirement = values.ConstructionRequirementSpec(
            "pin_installation", "Install the selected pin into its paired pockets",
            ("part:lower", "part:upper", "hardware:pin"),
            ("feature:paired_pocket.feature",), "operations")
        spec = replace(project.built.spec, purchased_hardware=(hardware,),
                       requirements=(*project.built.spec.requirements, requirement))
        pin = values.BuiltPurchasedHardware(hardware, cq.Workplane("XY").circle(3).extrude(8))
        project.built = replace(project.built, spec=spec, purchased_hardware=(pin,))
        walker = GeneratedProjectModuleRuntime().execute(root, project._walker)
        project.visits = walker.walk(project.built)
        return project

    def _resolve(self, project):
        tree = FabricationTreeEvidenceBuilder().build(project.visits)
        return ConstructionFeatureQualification().resolve(project.root, tree, project.visits)
