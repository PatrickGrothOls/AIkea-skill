"""Scope: Require current participant-scoped evidence for custom operation qualification."""

from dataclasses import replace

from construction_extension_fixture import ConstructionExtensionFixture
from construction_feature_qualification import ConstructionFeatureQualification
from construction_requirement_checker import ConstructionRequirementChecker
from construction_tree_checker import ConstructionTreeChecker
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestConstructionExtensionQualification:
    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    def test_valid_geometry_needs_separate_extension_evidence(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        applied, qualified = ConstructionTreeChecker().check(project.visits)
        assert applied.passed and not qualified.passed
        project.write_evidence()
        operations, features = self._resolve(project)
        assert operations == {"unit_01/joint:pair"}
        assert all(check.passed for check in ConstructionTreeChecker().check(project.visits, operations))
        assert all(check.passed for check in ConstructionRequirementChecker().check(project.visits, features))

    def test_evidence_for_one_part_does_not_qualify_a_two_part_operation(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        project.write_evidence(participants=("lower",))
        assert not self._resolve(project)[0]

    def test_failed_check_does_not_qualify_extension(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        project.write_evidence()
        project.data["checks"][0]["passed"] = False
        project.save()
        assert not self._resolve(project)[0]

    def test_geometry_or_material_edits_invalidate_qualification(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        project.write_evidence()
        part = project.built.parts[0]
        changed = replace(part, spec=replace(part.spec, material_id="birch"))
        project.visits = (project.visits[0], replace(project.visits[1], part=changed), project.visits[2])
        assert not self._resolve(project)[0]

    def test_stale_export_hash_is_not_accepted(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        project.write_evidence()
        project.data["part_artifacts"][0]["step_sha256"] = "stale"
        project.save()
        assert not self._resolve(project)[0]

    def test_qualifying_evidence_cannot_hide_a_missing_cut(self, tmp_path, contracts):
        project = ConstructionExtensionFixture().build(tmp_path, contracts)
        project.write_evidence()
        operations, _ = self._resolve(project)
        altered = replace(project.built, cuts=project.built.cuts[:-1])
        visits = (replace(project.visits[0], assembly=altered), *project.visits[1:])
        applied, _ = ConstructionTreeChecker().check(visits, operations)
        assert not applied.passed

    def _resolve(self, project):
        tree = FabricationTreeEvidenceBuilder().build(project.visits)
        return ConstructionFeatureQualification().resolve(project.root, tree, project.visits)
