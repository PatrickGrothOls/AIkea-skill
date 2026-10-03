"""Scope: Read and validate the ordered assembly run from aikea.yaml."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from assembly_taxonomy import AssemblyTaxonomyInputError


@dataclass(frozen=True)
class AssemblyRunItem:
    assembly_id: str
    purpose: str
    width_share: float


@dataclass(frozen=True)
class AssemblyRun:
    left_clearance: float
    right_clearance: float
    gap: float
    ceiling_clearance: float
    assemblies: tuple[AssemblyRunItem, ...]


class AssemblyRunReader:
    """Turn the saved run into one checked ordered value."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def read(self, project: dict[str, Any]) -> AssemblyRun:
        problems: list[str] = []
        settings = project.get("design_settings")
        if not isinstance(settings, dict):
            raise AssemblyTaxonomyInputError(["design_settings must be an object"])
        if "cabinet_run" in settings:
            problems.append("replace cabinet_run with one complete assembly_run first")
        raw_run = settings.get("assembly_run")
        if not isinstance(raw_run, dict):
            raise AssemblyTaxonomyInputError(problems + ["assembly_run must be an object"])
        numbers = tuple(
            self._read_number(raw_run, name, problems)
            for name in (
                "left_clearance",
                "right_clearance",
                "gap",
                "ceiling_clearance",
            )
        )
        assemblies = self._read_assemblies(raw_run.get("assemblies"), problems)
        if problems:
            raise AssemblyTaxonomyInputError(problems)
        return AssemblyRun(*numbers, assemblies)

    def _read_number(
        self, raw_run: dict[str, Any], name: str, problems: list[str]
    ) -> float:
        value = raw_run.get(name)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            problems.append(f"assembly_run.{name} must be zero or greater")
            return 0.0
        return float(value)

    def _read_assemblies(
        self, raw_assemblies: Any, problems: list[str]
    ) -> tuple[AssemblyRunItem, ...]:
        if not isinstance(raw_assemblies, list) or not raw_assemblies:
            problems.append("assembly_run.assemblies must contain at least one assembly")
            return ()
        items = tuple(
            self._read_item(raw, index, problems)
            for index, raw in enumerate(raw_assemblies)
        )
        ids = [item.assembly_id for item in items if item]
        if len(ids) != len(set(ids)):
            problems.append("assembly_run assembly ids must be unique")
        return tuple(item for item in items if item)

    def _read_item(
        self, raw: Any, index: int, problems: list[str]
    ) -> AssemblyRunItem | None:
        path = f"assembly_run.assemblies[{index}]"
        if not isinstance(raw, dict):
            problems.append(f"{path} must be an object")
            return None
        assembly_id = raw.get("id")
        purpose = raw.get("purpose")
        share = raw.get("width_share")
        if not isinstance(assembly_id, str) or not self._ID_PATTERN.fullmatch(assembly_id):
            problems.append(f"{path}.id must be a stable lowercase id with a two-digit suffix")
        if not isinstance(purpose, str) or not purpose.strip():
            problems.append(f"{path}.purpose must be a non-empty name")
        if isinstance(share, bool) or not isinstance(share, (int, float)) or share <= 0:
            problems.append(f"{path}.width_share must be greater than zero")
        if any(problem.startswith(path) for problem in problems):
            return None
        return AssemblyRunItem(assembly_id, purpose, float(share))
