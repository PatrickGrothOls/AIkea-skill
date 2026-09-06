"""Scope: Verify readiness requires the complete authentic fabrication pack."""

from hashlib import sha256
import json
import struct

import cadquery as cq

from fabrication_readiness_gate import FabricationReadinessGate
from fabrication_readiness_test_project import FabricationReadinessTestProject


class TestFabricationReadinessGate:
    """Protect both refusal and successful completion of the full contract."""

    def test_blocks_a_valid_tree_without_manufacturing_outputs(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert not report.is_ready
        assert "pack.part_step_and_drawings" in failed
        assert "pack.complete_bom" in failed
        assert "pack.complete_cut_list" in failed
        assert "pack.machining_declarations" in failed
        assert "validation.full_wardrobe_position" in failed
        assert "approval.current_closed_assembly" in failed

    def test_passes_only_with_complete_current_evidence(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        assert report.is_ready
        assert report.as_dict()["status"] == "fabrication-ready"

    def test_rejects_an_approved_but_empty_closed_scene(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        model.write_bytes(self._empty_scene_glb())
        review = tmp_path / "reviews/fabrication-assembly.json"
        record = json.loads(review.read_text(encoding="utf-8"))
        record["artifact_sha256"] = sha256(model.read_bytes()).hexdigest()
        record["decision_artifact_sha256"] = record["artifact_sha256"]
        project.write_json(review, record)

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert "approval.current_closed_assembly" in failed

    def test_rejects_approval_after_the_built_tree_geometry_changes(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        visits[-1].part.solid = cq.Workplane("XY").box(
            400.0,
            2000.0,
            18.0,
            centered=(False, False, False),
        )

        report = FabricationReadinessGate().evaluate(tmp_path, visits)

        approval = next(
            check
            for check in report.checks
            if check.code == "approval.current_closed_assembly"
        )
        assert not approval.passed

    def _empty_scene_glb(self) -> bytes:
        document = json.dumps(
            {"asset": {"version": "2.0"}, "scene": 0, "scenes": [{}]},
            separators=(",", ":"),
        ).encode("utf-8")
        padding = b" " * ((4 - len(document) % 4) % 4)
        chunk = document + padding
        return (
            struct.pack("<4sII", b"glTF", 2, 20 + len(chunk))
            + struct.pack("<II", len(chunk), 0x4E4F534A)
            + chunk
        )


__all__ = ["TestFabricationReadinessGate"]
