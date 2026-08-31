"""Scope: Define the generic contract for feature-owned assembly review poses."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from assembly_tree_review_plan import AssemblyTreeReviewPlan


@dataclass(frozen=True, slots=True)
class AssemblyFeatureReviewContext:
    """Give one feature its owner without exposing orchestration mechanics."""

    project_root: Path
    owner_path: tuple[str, ...]
    assembly: Any


class AssemblyFeatureReview(Protocol):
    """Contribute review-only changes for one requested named state."""

    def plan(
        self,
        context: AssemblyFeatureReviewContext,
        state: str,
    ) -> AssemblyTreeReviewPlan: ...


@dataclass(frozen=True, slots=True)
class RegisteredAssemblyFeatureReview:
    """Bind one stable feature selector to its review implementation."""

    feature_id: str
    feature: AssemblyFeatureReview


__all__ = [
    "AssemblyFeatureReview",
    "AssemblyFeatureReviewContext",
    "RegisteredAssemblyFeatureReview",
]
