"""Scope: Preserve client-confirmed decisions that direct later design work."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DesignDecision:
    subject: str
    decision: str
    design_effect: str
    client_statement: str


class DesignDecisionReader:
    """Turn global-specification decision records into checked values."""

    _TEXT_FIELDS = ("subject", "decision", "design_effect", "client_statement")

    def read(
        self, data: dict[str, Any], problems: list[str]
    ) -> tuple[DesignDecision, ...]:
        entries = data.get("design_decisions")
        if not isinstance(entries, list):
            problems.append("design_decisions is required and must be a list")
            return ()

        decisions: list[DesignDecision] = []
        for index, entry in enumerate(entries):
            path = f"design_decisions[{index}]"
            if not isinstance(entry, dict):
                problems.append(f"{path} must be a mapping")
                continue
            values = self._read_text_fields(entry, path, problems)
            if values is not None:
                decisions.append(DesignDecision(**values))
        return tuple(decisions)

    def _read_text_fields(
        self, entry: dict[str, Any], path: str, problems: list[str]
    ) -> dict[str, str] | None:
        values = {field: entry.get(field) for field in self._TEXT_FIELDS}
        invalid_fields = [
            field
            for field, value in values.items()
            if not isinstance(value, str) or not value.strip()
        ]
        for field in invalid_fields:
            problems.append(f"{path}.{field} is required and must be non-empty text")
        if invalid_fields:
            return None
        return {field: value.strip() for field, value in values.items()}
