"""Scope: Protect completely fresh AIkea runs from prior-project value reuse."""

from pathlib import Path


class TestFreshProjectIsolationContract:
    """Keep one shared rule active through every routed construction stage."""

    def test_shared_conversation_contract_forbids_opening_other_projects(self) -> None:
        path = Path(__file__).parents[1] / "aikea/references/client-conversation.md"
        contract = " ".join(path.read_text(encoding="utf-8").split())

        assert "Do not search, open, or copy another client project's folders" in contract
        assert "Memory may restore reusable procedure" in contract
        assert "never project-specific values" in contract
