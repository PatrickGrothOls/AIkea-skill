"""Scope: Record explicit construction obligations independently of executed work."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConstructionRequirementSpec:
    """Refer to owner-relative tree paths and record a solution or an open question."""

    requirement_id: str
    description: str
    subject_paths: tuple[str, ...]
    operation_paths: tuple[str, ...] = ()
    disposition: str = "unresolved"
    basis: str = ""
