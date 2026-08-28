"""Scope: Attach checked physical and posed review parts to one cabinet."""

from __future__ import annotations

from dataclasses import dataclass

from unit_mockup import MockupPart


@dataclass(frozen=True, slots=True)
class CabinetReviewAddition:
    """Keep one cabinet's fit geometry separate from its presentation pose."""

    assembly_id: str
    physical_parts: tuple[MockupPart, ...]
    review_parts: tuple[MockupPart, ...]


__all__ = ["CabinetReviewAddition"]
