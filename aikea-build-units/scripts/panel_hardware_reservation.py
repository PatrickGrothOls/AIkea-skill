"""Scope: Reserve System 32 nodes and physical panel space for cabinet hardware."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


class PanelHardwareConflictError(ValueError):
    """Report hardware that shares a fixing node or physical panel space."""


@dataclass(frozen=True, slots=True)
class PanelHardwareReservation:
    """Describe one fitting in canonical front-to-back side-panel coordinates."""

    owner_id: str
    hardware_kind: str
    side_part_id: str
    system_32_node_rows_mm: tuple[float, ...]
    depth_interval_mm: tuple[float, float]
    height_interval_mm: tuple[float, float]

    def conflicts_with(self, other: "PanelHardwareReservation") -> bool:
        if self.side_part_id != other.side_part_id:
            return False
        shared_nodes = set(self.system_32_node_rows_mm).intersection(
            other.system_32_node_rows_mm
        )
        return bool(shared_nodes) or (
            self._overlaps(self.depth_interval_mm, other.depth_interval_mm)
            and self._overlaps(self.height_interval_mm, other.height_interval_mm)
        )

    def _overlaps(
        self,
        first: tuple[float, float],
        second: tuple[float, float],
    ) -> bool:
        return max(first[0], second[0]) < min(first[1], second[1]) - 1e-6


class PanelHardwareReservationPlan:
    """Validate and persist the fittings owned by one cabinet side-panel pair."""

    def require_compatible(
        self,
        candidate: PanelHardwareReservation,
        existing: tuple[PanelHardwareReservation, ...],
    ) -> None:
        conflict = next(
            (item for item in existing if candidate.conflicts_with(item)),
            None,
        )
        if conflict is not None:
            raise PanelHardwareConflictError(
                f"{candidate.owner_id} conflicts with {conflict.owner_id} "
                f"on {candidate.side_part_id}"
            )


class PanelHardwareReservationStore:
    """Read and write the shared project-owned hardware map."""

    _FILENAME = "hardware-reservations.json"

    def path(self, project_root: Path, assembly_id: str) -> Path:
        return project_root / "assemblies" / assembly_id / self._FILENAME

    def load(
        self,
        project_root: Path,
        assembly_id: str,
    ) -> tuple[PanelHardwareReservation, ...]:
        path = self.path(project_root, assembly_id)
        if not path.is_file():
            return ()
        data = json.loads(path.read_text(encoding="utf-8"))
        return tuple(self._reservation(item) for item in data["reservations"])

    def write(
        self,
        project_root: Path,
        assembly_id: str,
        reservations: tuple[PanelHardwareReservation, ...],
    ) -> Path:
        path = self.path(project_root, assembly_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "assembly_id": assembly_id,
            "reservations": [asdict(item) for item in reservations],
        }
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _reservation(self, values: dict) -> PanelHardwareReservation:
        return PanelHardwareReservation(
            owner_id=values["owner_id"],
            hardware_kind=values["hardware_kind"],
            side_part_id=values["side_part_id"],
            system_32_node_rows_mm=tuple(values["system_32_node_rows_mm"]),
            depth_interval_mm=tuple(values["depth_interval_mm"]),
            height_interval_mm=tuple(values["height_interval_mm"]),
        )


__all__ = [
    "PanelHardwareConflictError",
    "PanelHardwareReservation",
    "PanelHardwareReservationPlan",
    "PanelHardwareReservationStore",
]
