"""Scope: Verify and import the exact Riex NC70 hinge and H0 plate STEP files."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


class RiexHardwareAssetError(ValueError):
    """Report missing or changed purchased-hardware CAD."""


@dataclass(frozen=True, slots=True)
class RiexNc70HardwareSet:
    """Carry both exact hinge poses and their matching plate."""

    closed_hinge: Any
    open_hinge: Any
    mounting_plate: Any


class RiexNc70HardwareLoader:
    """Load only the registered source bytes in their manufacturer frames."""

    _MANIFEST = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "riex"
        / "nc70"
        / "hardware-assets.json"
    )
    _BOUND_TOLERANCE_MM = 1e-3

    def load(self, hardware_root: Path) -> RiexNc70HardwareSet:
        records = {
            item["asset_id"]: item
            for item in json.loads(self._MANIFEST.read_text(encoding="utf-8"))["assets"]
        }
        return RiexNc70HardwareSet(
            closed_hinge=self._load_asset(
                hardware_root, records["riex-nc70-f000001-closed"]
            ),
            open_hinge=self._load_asset(
                hardware_root, records["riex-nc70-f000001-open"]
            ),
            mounting_plate=self._load_asset(
                hardware_root,
                records["riex-nc70-f000049-h0-euroscrew-plate"],
            ),
        )

    def _load_asset(self, hardware_root: Path, record: dict[str, Any]) -> Any:
        import cadquery as cq

        path = hardware_root / record["relative_path"]
        if not path.is_file():
            raise RiexHardwareAssetError(f"missing registered hardware CAD: {path}")
        actual_sha256 = sha256(path.read_bytes()).hexdigest()
        if actual_sha256 != record["sha256"]:
            raise RiexHardwareAssetError(
                f"hardware checksum differs: {record['asset_id']}"
            )
        shape = cq.importers.importStep(str(path)).val()
        bounds = shape.BoundingBox()
        observed = (
            bounds.xmin,
            bounds.xmax,
            bounds.ymin,
            bounds.ymax,
            bounds.zmin,
            bounds.zmax,
        )
        bounds_match = all(
            abs(actual - expected) <= self._BOUND_TOLERANCE_MM
            for actual, expected in zip(observed, record["bounds_mm"])
        )
        if len(shape.Solids()) != record["solid_count"] or not bounds_match:
            raise RiexHardwareAssetError(
                f"hardware geometry differs: {record['asset_id']}"
            )
        return shape


__all__ = [
    "RiexHardwareAssetError",
    "RiexNc70HardwareLoader",
    "RiexNc70HardwareSet",
]
