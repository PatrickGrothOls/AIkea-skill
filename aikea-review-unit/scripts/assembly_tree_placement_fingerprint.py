"""Scope: Fingerprint every closed physical item path and accumulated frame."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any


@dataclass(frozen=True, slots=True)
class AssemblyTreePlacementFingerprint:
    """Bind one canonical digest to all closed tree paths and placements."""

    sha256: str
    item_count: int


class AssemblyTreePlacementFingerprinter:
    """Serialize recursive physical frames without using review poses."""

    def build(self, visits: tuple[Any, ...]) -> AssemblyTreePlacementFingerprint:
        records = tuple(
            sorted(
                (self._record(item) for item in visits),
                key=lambda item: (item["path"], item["kind"]),
            )
        )
        content = json.dumps(
            records,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        return AssemblyTreePlacementFingerprint(sha256(content).hexdigest(), len(records))

    def _record(self, item: Any) -> dict[str, Any]:
        return {
            "path": "/".join(
                segment.split(":", 1)[-1] for segment in item.path
            ),
            "kind": type(item).__name__,
            "placement": self._placement(item.local_to_root),
        }

    def _placement(self, placement: Any) -> dict[str, Any] | None:
        if placement is None:
            return None
        origin = placement.origin_in_parent
        axes = placement.axis_basis
        return {
            "origin_mm": self._values(origin, ("x_mm", "y_mm", "z_mm")),
            "local_x": self._values(axes.local_x_in_parent, ("x", "y", "z")),
            "local_y": self._values(axes.local_y_in_parent, ("x", "y", "z")),
            "local_z": self._values(axes.local_z_in_parent, ("x", "y", "z")),
        }

    def _values(self, value: Any, names: tuple[str, str, str]) -> list[float]:
        return [self._number(getattr(value, name)) for name in names]

    def _number(self, value: Any) -> float:
        number = float(value)
        return 0.0 if number == 0.0 else number


__all__ = [
    "AssemblyTreePlacementFingerprint",
    "AssemblyTreePlacementFingerprinter",
]
