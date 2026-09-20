"""Scope: Allow prerequisite component proofs without weakening finished-layout reviews."""
import json
import cadquery as cq
from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
from complete_assembly_review_report import CompleteAssemblyReviewReport
from cadquery_glb_exporter import CadQueryGlbExporter
from unit_mockup import MockupPart
from test_complete_assembly_review_generator import (
    DrawerReviewLoaderProbe, ReviewFeatureLoaderProbe, ReviewFeatureProbe,
    HydratorProbe, GeometryProbe, ExporterProbe,
)


class ProofReporter:
    def write(self, assembly_id, output, parts, states, *, component_proof=False):
        assert component_proof is True
        return output.with_suffix(".review.json")


class TestComponentProofReviewScope:
    def test_prerequisite_proof_can_export_with_explicit_scope(self, tmp_path):
        exporter = ExporterProbe()
        generator = CompleteAssemblyReviewGenerator(loader=DrawerReviewLoaderProbe(),
            feature_loader=ReviewFeatureLoaderProbe(ReviewFeatureProbe()),
            hydrator=HydratorProbe(), geometry=GeometryProbe(), exporter=exporter,
            reporter=ProofReporter())
        generator.generate(tmp_path, "cabinet_01", tmp_path/"proof.glb", component_proof=True)
        assert exporter.call is not None

    def test_component_artifact_is_identified_and_never_manufacturing_authority(self, tmp_path):
        part = MockupPart("marker", cq.Workplane("XY").box(5, 6, 7), cq.Location(), (1, 1, 1, 1))
        output = tmp_path/"proof.glb"
        CadQueryGlbExporter().export("cabinet_01", (part,), output)
        path = CompleteAssemblyReviewReport().write("cabinet_01", output, (part,), {}, component_proof=True)
        report = json.loads(path.read_text())
        assert report["review_type"] == "component_proof"
        assert report["manufacturing_authority"] is False
