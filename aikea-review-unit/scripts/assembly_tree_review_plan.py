"""Scope: Declare generic pose, visibility, and overlay changes for one tree review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from unit_mockup import MockupPart, UnitMockupInputError

AssemblyPath = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AssemblyReviewMotion:
    """Apply one review-only local motion after an assembly's saved frame."""

    assembly_path: AssemblyPath
    location: Any


@dataclass(frozen=True, slots=True)
class AssemblyReviewOverlay:
    """Attach non-authoritative visual geometry to one assembly frame."""

    owner_path: AssemblyPath
    parts: tuple[MockupPart, ...]


@dataclass(frozen=True, slots=True)
class AssemblyTreeReviewPlan:
    """Describe presentation changes without changing fabrication geometry."""

    motions: tuple[AssemblyReviewMotion, ...] = ()
    hidden_paths: tuple[AssemblyPath, ...] = ()
    hidden_subtrees: tuple[AssemblyPath, ...] = ()
    overlays: tuple[AssemblyReviewOverlay, ...] = ()

    def __post_init__(self) -> None:
        motion_paths = tuple(item.assembly_path for item in self.motions)
        if len(set(motion_paths)) != len(motion_paths):
            raise UnitMockupInputError(["review motions must target unique assemblies"])

    def motion_for(self, path: AssemblyPath) -> Any | None:
        return next(
            (
                motion.location
                for motion in self.motions
                if motion.assembly_path == path
            ),
            None,
        )

    def hides(self, path: AssemblyPath) -> bool:
        return path in self.hidden_paths or any(
            path[: len(prefix)] == prefix for prefix in self.hidden_subtrees
        )


__all__ = [
    "AssemblyPath",
    "AssemblyReviewMotion",
    "AssemblyReviewOverlay",
    "AssemblyTreeReviewPlan",
]
