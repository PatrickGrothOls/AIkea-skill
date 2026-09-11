"""Scope: Prevent exact contact allowances from hiding other intersections or stale evidence."""

from dataclasses import replace

import pytest

from construction_contact_fixture import ConstructionContactFixture
from construction_position_evidence import ConstructionPositionEvidence
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestConstructionContacts:
    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    def test_exact_qualified_contact_passes_and_is_reported(self, tmp_path, contracts):
        project = ConstructionContactFixture().build(tmp_path, contracts)
        project.write_evidence()
        report = self._write(project)
        assert report["status"] == "valid"
        assert report["geometry"]["overlaps"] == []
        assert report["geometry"]["allowed_overlaps"][0]["volume_mm3"] == pytest.approx(100)
        tree = FabricationTreeEvidenceBuilder().build(project.visits)
        assert ConstructionPositionEvidence().check(tmp_path, tree, project.visits).passed

    def test_allowance_without_current_feature_proof_stays_blocked(self, tmp_path, contracts):
        project = ConstructionContactFixture().build(tmp_path, contracts)
        report = self._write(project)
        assert report["status"] == "invalid"
        assert report["contact_evidence_problems"]
        assert report["geometry"]["overlaps"]

    @pytest.mark.parametrize("minimum_x,maximum_volume", [(9.5, 100), (9, 99)])
    def test_region_and_volume_are_independently_enforced(self, tmp_path, contracts, minimum_x, maximum_volume):
        project = ConstructionContactFixture().build(tmp_path, contracts, minimum_x, maximum_volume)
        project.write_evidence()
        report = self._write(project)
        assert report["status"] == "invalid"
        assert not report["contact_evidence_problems"]
        assert report["geometry"]["overlaps"]

    def test_changed_region_cannot_borrow_old_evidence(self, tmp_path, contracts):
        project = ConstructionContactFixture().build(tmp_path, contracts)
        project.write_evidence()
        project.allowance = replace(project.allowance, maximum_volume_mm3=101)
        assert self._write(project)["contact_evidence_problems"]

    def test_allowance_cannot_borrow_a_feature_for_another_pair(self, tmp_path, contracts):
        project = ConstructionContactFixture().build(tmp_path, contracts)
        project.write_evidence()
        project.allowance = replace(project.allowance, subject_paths=("unit_01/part:left", "unit_01/part:other"))
        assert self._write(project)["status"] == "invalid"

    def _write(self, project):
        return ConstructionPositionEvidence().write(project.root, project.visits, project.envelope, (project.allowance,))
