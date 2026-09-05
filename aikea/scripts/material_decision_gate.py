"""Scope: Block calculations that depend on unresolved material construction."""

from __future__ import annotations

from design_decisions import DesignDecision


class MaterialDecisionGate:
    """Reject the stable marker for a material need the schema cannot represent."""

    SUBJECT = "unresolved_material_requirement"
    DECISION = "blocked"

    def problems(self, decisions: tuple[DesignDecision, ...]) -> tuple[str, ...]:
        return tuple(
            "material construction is blocked: " + decision.design_effect
            for decision in decisions
            if decision.subject == self.SUBJECT and decision.decision == self.DECISION
        )
