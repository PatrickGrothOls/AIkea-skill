"""Scope: Define the generated files from one structural-base visual review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BaseReviewResult:
    base_assembly_id: str
    cabinet_assembly_id: str
    base_glb_path: Path
    cabinet_with_base_glb_path: Path
    position_report_path: Path


__all__ = ["BaseReviewResult"]
