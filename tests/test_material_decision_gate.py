"""Scope: Verify unresolved material requirements fail before calculation."""

import pytest

from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputReader
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestMaterialDecisionGate:
    """Keep missing, duplicate, and unsupported material choices out of generation."""

    def setup_method(self) -> None:
        self.project = OverallWardrobeTestProject().load_flat()

    def test_unresolved_material_requirement_blocks_calculation(self) -> None:
        self.project["design_decisions"].append(
            {
                "subject": "unresolved_material_requirement",
                "decision": "blocked",
                "design_effect": "book shelf needs a separate checked construction",
                "client_statement": "Use a stronger material for the book shelf.",
            }
        )

        with pytest.raises(
            OverallWardrobeInputError,
            match="material construction is blocked",
        ):
            OverallWardrobeInputReader().read(self.project)

    def test_missing_material_decisions_block_calculation(self) -> None:
        self.project["design_decisions"] = []

        with pytest.raises(OverallWardrobeInputError) as raised:
            OverallWardrobeInputReader().read(self.project)

        assert len(raised.value.problems) == 3
        for subject in (
            "cabinet_carcass_material",
            "door_front_material",
            "back_panel_material",
        ):
            assert f"exactly one confirmed material decision is required: {subject}" in (
                raised.value.problems
            )

    def test_duplicate_material_decision_blocks_calculation(self) -> None:
        self.project["design_decisions"].append(
            dict(self.project["design_decisions"][0])
        )

        with pytest.raises(
            OverallWardrobeInputError,
            match="exactly one confirmed material decision is required",
        ):
            OverallWardrobeInputReader().read(self.project)

    def test_complete_material_decisions_allow_calculation(self) -> None:
        OverallWardrobeInputReader().read(self.project)
