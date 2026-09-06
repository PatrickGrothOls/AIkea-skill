"""Scope: Block calculations that depend on unresolved material construction."""

from __future__ import annotations

from design_decisions import DesignDecision


class MaterialDecisionGate:
    """Require the supported material groups and reject unresolved exceptions."""

    REQUIRED_SUBJECTS = (
        "cabinet_carcass_material",
        "door_front_material",
        "back_panel_material",
    )
    BLOCKER_SUBJECT = "unresolved_material_requirement"
    BLOCKER_DECISION = "blocked"

    def problems(self, decisions: tuple[DesignDecision, ...]) -> tuple[str, ...]:
        counts = {
            subject: sum(decision.subject == subject for decision in decisions)
            for subject in self.REQUIRED_SUBJECTS
        }
        problems = [
            f"exactly one confirmed material decision is required: {subject}"
            for subject, count in counts.items()
            if count != 1
        ]
        problems.extend(
            "material construction is blocked: " + decision.design_effect
            for decision in decisions
            if decision.subject == self.BLOCKER_SUBJECT
            and decision.decision == self.BLOCKER_DECISION
        )
        return tuple(problems)
