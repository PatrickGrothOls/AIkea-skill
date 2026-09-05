"""Scope: Verify unresolved material requirements fail before calculation."""

import pytest

from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputReader
from overall_wardrobe_test_project import OverallWardrobeTestProject


class TestMaterialDecisionGate:
    """Keep unsupported part-specific material choices out of generation."""

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

    def test_resolved_material_decisions_do_not_block_calculation(self) -> None:
        self.project["design_decisions"].append(
            {
                "subject": "cabinet_carcass_material",
                "decision": "confirmed product A",
                "design_effect": "use the confirmed face and edge treatment",
                "client_statement": "Use product A for the cabinet.",
            }
        )

        OverallWardrobeInputReader().read(self.project)
