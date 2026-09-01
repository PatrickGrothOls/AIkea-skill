"""Scope: Verify readiness requires the complete authentic fabrication pack."""

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


__all__ = ["TestFabricationReadinessGate"]
