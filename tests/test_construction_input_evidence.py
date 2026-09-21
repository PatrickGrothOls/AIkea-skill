"""Scope: Reject evidence after construction edits that need not change a rendered image."""

import json

import pytest

from construction_input_fingerprint import ConstructionInputFingerprinter
from fabrication_assembly_review_record import FabricationAssemblyReviewRecord
from fabrication_closed_assembly_approval_checker import FabricationClosedAssemblyApprovalChecker
from fabrication_readiness_test_project import FabricationReadinessTestProject
from review_server_session import ReviewServerSession
from review_decision_store import ReviewDecisionConflict
from blender_presentation_test_evidence import BlenderPresentationTestEvidence


class TestConstructionInputEvidence:
    @pytest.mark.parametrize("field,value", [("material_id", "MDF"), ("local_size_mm", (500, 2000, 16))])
    def test_changed_part_inputs_invalidate_unchanged_model(self, tmp_path, field, value):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        assert FabricationClosedAssemblyApprovalChecker().check(tmp_path, visits).passed
        setattr(visits[-1].part.spec, field, value)
        assert not FabricationClosedAssemblyApprovalChecker().check(tmp_path, visits).passed

    def test_changed_requirements_invalidate_an_unchanged_model(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        visits[1].assembly.spec.requirements[0].description = "Must support a person"
        assert not FabricationClosedAssemblyApprovalChecker().check(tmp_path, visits).passed

    def test_updated_inputs_create_a_new_proposal_for_identical_glb(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        visits[-1].part.spec.material_id = "birch"
        digest = ConstructionInputFingerprinter().build(tmp_path, visits)
        record = FabricationAssemblyReviewRecord().write_proposal(
            tmp_path, tmp_path / "assemblies/full_wardrobe_review.glb", digest,
        )
        assert json.loads(record.read_text())["status"] == "proposed"
        assert json.loads(record.read_text())["construction_sha256"] == digest

    def test_source_and_selected_product_changes_invalidate_context(self, tmp_path):
        project = FabricationReadinessTestProject()
        visits = project.visits()
        fingerprinter = ConstructionInputFingerprinter()
        original = fingerprinter.build(tmp_path, visits)
        sources = fingerprinter.source_inputs(tmp_path)
        (tmp_path / "aikea.yaml").write_text("hardware: {product: selected_runner}\n")
        assert fingerprinter.build(tmp_path, visits) != original
        with pytest.raises(ValueError, match="inputs changed during the build"):
            fingerprinter.require_unchanged_sources(tmp_path, sources)
        assert fingerprinter.build(tmp_path, tuple(reversed(visits))) == fingerprinter.build(tmp_path, visits)

    def test_open_viewer_cannot_approve_replaced_inputs_with_identical_glb(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        record = tmp_path / "reviews/fabrication-assembly.json"
        writer = FabricationAssemblyReviewRecord()
        self._position(tmp_path, "old-inputs")
        writer.write_proposal(tmp_path, model, "old-inputs")
        BlenderPresentationTestEvidence().write(model, model)
        session = ReviewServerSession(model, record, model)
        self._position(tmp_path, "new-inputs")
        writer.write_proposal(tmp_path, model, "new-inputs")
        with pytest.raises(ReviewDecisionConflict, match="inputs changed"):
            session.decide("approved", session.token)
        assert json.loads(record.read_text())["status"] == "proposed"

    def _position(self, root, digest):
        (root / "assemblies/construction-position-check.json").write_text(json.dumps(
            {"schema_version": 2, "status": "valid", "construction_sha256": digest}))

    def test_drawer_policy_changes_invalidate_unchanged_geometry(self,tmp_path):
        project=FabricationReadinessTestProject();visits=project.visits()
        path=tmp_path/'assemblies/drawer-layout-policy.json';path.parent.mkdir()
        path.write_text('{"schema_version":1,"stacks":[]}')
        original=ConstructionInputFingerprinter().build(tmp_path,visits)
        path.write_text('{"schema_version":1,"stacks":[],"changed_exception":true}')
        assert ConstructionInputFingerprinter().build(tmp_path,visits)!=original
