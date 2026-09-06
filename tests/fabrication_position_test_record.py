"""Scope: Build one structurally complete saved position report for gate tests."""

from __future__ import annotations

from assembly_tree_placement_fingerprint import AssemblyTreePlacementFingerprinter


class FabricationPositionTestRecord:
    """Provide realistic position evidence without copying it between tests."""

    def build(self, visits, part_path: str, role: str) -> dict[str, object]:
        assembly_id = part_path.split("/")[-2]
        part_id = part_path.rsplit("/", 1)[-1]
        fingerprint = AssemblyTreePlacementFingerprinter().build(visits)
        return {
            "schema_version": 1,
            "status": "valid",
            "global_coordinates": {
                "zero": "front-left floor point of the measured space",
                "positive_x": "right",
                "positive_y": "back",
                "positive_z": "up",
            },
            "assemblies": {
                assembly_id: {
                    "local_zero_mm": [0.0, 0.0, 0.0],
                    "global_zero_mm": [0.0, 0.0, 0.0],
                    "local_bounds": self._bounds(),
                    "global_bounds": self._bounds(),
                    "part_positions": {
                        part_id: self._part_position(role),
                    },
                }
            },
            "relationships": {
                "cabinet_count": 1,
                "base_top_z_mm": 0.0,
                "plinth_front": "flush",
                "plinth_recess_mm": 0.0,
                "plinth_front_y_mm": 0.0,
                "cabinet_gaps_mm": [],
                "door_bottoms_z_mm": {assembly_id: 0.0},
            },
            "checks": [{"name": "cabinet occupies its saved span", "passed": True}],
            "closed_tree_placement_sha256": fingerprint.sha256,
            "closed_tree_item_count": fingerprint.item_count,
        }

    def _part_position(self, role: str) -> dict[str, object]:
        return {
            "role": role,
            "local_zero_mm": [0.0, 0.0, 0.0],
            "assembly_zero_mm": [0.0, 0.0, 0.0],
            "global_zero_mm": [0.0, 0.0, 0.0],
            "local_axes_in_assembly": {
                "x": [1.0, 0.0, 0.0],
                "y": [0.0, 1.0, 0.0],
                "z": [0.0, 0.0, 1.0],
            },
            "assembly_bounds": self._bounds(),
            "global_bounds": self._bounds(),
        }

    def _bounds(self) -> dict[str, list[float]]:
        return {
            "minimum_mm": [0.0, 0.0, 0.0],
            "maximum_mm": [500.0, 2000.0, 18.0],
        }


__all__ = ["FabricationPositionTestRecord"]
