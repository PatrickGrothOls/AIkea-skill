"""Scope: Exercise requirement coverage independently of plausible geometry."""

from types import SimpleNamespace

from construction_requirement_checker import ConstructionRequirementChecker
from fabrication_readiness_test_project import FabricationReadinessTestProject


class TestConstructionRequirements:
    def test_intentionally_loose_panel_has_explicit_coverage(self):
        checks = ConstructionRequirementChecker().check(FabricationReadinessTestProject().visits())
        assert all(check.passed for check in checks)

    def test_absent_assessment_is_not_an_empty_approved_brief(self):
        visits = FabricationReadinessTestProject().visits()
        visits[1].assembly.spec.requirements = None
        check = ConstructionRequirementChecker().check(visits)[0]
        assert not check.passed
        assert any("not been assessed" in problem for problem in check.problems)

    def test_missing_required_operation_is_visible_even_if_tree_omits_it(self):
        visits = FabricationReadinessTestProject().visits()
        requirement = visits[1].assembly.spec.requirements[0]
        requirement.disposition = "operations"
        requirement.operation_paths = ("joint:mounting",)
        check = ConstructionRequirementChecker().check(visits)[0]
        assert not check.passed
        assert any("required operation is missing" in problem for problem in check.problems)

    def test_unrelated_operation_cannot_satisfy_a_requirement(self):
        visits = FabricationReadinessTestProject().visits()
        requirement = visits[1].assembly.spec.requirements[0]
        requirement.disposition = "operations"
        requirement.operation_paths = ("feature:hinges",)
        operations = {"wardrobe_01/cabinet_01/feature:hinges": {"wardrobe_01/cabinet_01/part:other"}}
        check = ConstructionRequirementChecker().check(visits, operations)[0]
        assert not check.passed
        assert "do not cover every required participant" in check.problems[0]

    def test_empty_requirements_do_not_cover_a_real_part(self):
        visits = FabricationReadinessTestProject().visits()
        visits[1].assembly.spec.requirements = ()
        assert not ConstructionRequirementChecker().check(visits)[0].passed

    def test_floor_contact_requires_a_reason_and_no_machining_claim(self):
        visits = FabricationReadinessTestProject().visits()
        requirement = visits[1].assembly.spec.requirements[0]
        requirement.disposition = "floor_contact"
        requirement.basis = ""
        assert not ConstructionRequirementChecker().check(visits)[0].passed
        requirement.basis = "This is a loose floor protector resting on the floor"
        assert ConstructionRequirementChecker().check(visits)[0].passed

    def test_duplicate_requirement_ids_and_unknown_subjects_are_reported(self):
        visits = FabricationReadinessTestProject().visits()
        requirement = visits[1].assembly.spec.requirements[0]
        requirement.subject_paths = ("part:missing",)
        visits[1].assembly.spec.requirements = (requirement, requirement)
        check = ConstructionRequirementChecker().check(visits)[0]
        assert any("duplicate requirement IDs" in problem for problem in check.problems)
        assert any("existing owner-relative" in problem for problem in check.problems)

    def test_missing_material_is_separate_from_support_coverage(self):
        visits = FabricationReadinessTestProject().visits()
        visits[-1].part.spec.material_id = ""
        coverage, identity = ConstructionRequirementChecker().check(visits)
        assert coverage.passed and not identity.passed

    def test_hardware_requires_exact_identity_and_installation(self):
        visits = FabricationReadinessTestProject().visits()
        hardware = SimpleNamespace(path=("wardrobe_01", "hardware:foot"),
                                   hardware=SimpleNamespace(spec=SimpleNamespace(
                                       manufacturer="", product_code="", hardware_asset_id="")))
        coverage, identity = ConstructionRequirementChecker().check((*visits, hardware))
        assert not coverage.passed and not identity.passed
