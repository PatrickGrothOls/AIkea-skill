"""Scope: Keep unfinished attachments explicit without allowing unsupported tooling."""

from dataclasses import replace

import pytest

from part_construction_error import PartConstructionError
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestUnresolvedConstructionPreview:
    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    def test_preview_retains_unresolved_joint_and_its_owned_participants(self, contracts):
        values, panels = contracts
        corner = PanelFixture()._corner(contracts)
        attachment = values.JointSpec("attachment", ("seat", "support"), "unfinished attachment")
        spec = replace(corner, joints=(attachment,))
        with pytest.raises(PartConstructionError, match="no machining tool"):
            panels.PanelAssemblyBuilder(spec).build()
        built = panels.PanelAssemblyBuilder(spec, allow_unresolved=True).build()
        assert built.joints == (attachment,)
        assert built.cuts == ()
        assert built.spec.joints == built.joints

    @pytest.mark.parametrize("change, message", [
        (dict(joint_type="invented_tool"), "no machining tool"),
        (dict(participant_ids=("seat", "missing")), "reference owned parts"),
    ])
    def test_preview_does_not_bypass_other_contract_checks(self, contracts, change, message):
        values, panels = contracts
        corner = PanelFixture()._corner(contracts)
        joint = values.JointSpec("attachment", ("seat", "support"), "unfinished attachment")
        spec = replace(corner, joints=(replace(joint, **change),))
        with pytest.raises(PartConstructionError, match=message):
            panels.PanelAssemblyBuilder(spec, allow_unresolved=True).build()
