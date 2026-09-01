"""Scope: Validate the complete saved full-wardrobe position record shape."""

from __future__ import annotations

from math import isfinite


class FabricationPositionRecordValidator:
    """Reject placeholder coordinates, bounds, parts, and relationships."""

    _ASSEMBLY_KEYS = {
        "local_zero_mm", "global_zero_mm", "local_bounds", "global_bounds",
        "part_positions",
    }
    _PART_KEYS = {
        "role", "local_zero_mm", "assembly_zero_mm", "global_zero_mm",
        "local_axes_in_assembly", "assembly_bounds", "global_bounds",
    }
    _RELATIONSHIP_KEYS = {
        "cabinet_count", "base_top_z_mm", "plinth_front", "plinth_recess_mm",
        "plinth_front_y_mm", "cabinet_gaps_mm", "door_bottoms_z_mm",
    }
    _GLOBAL_COORDINATES = {
        "zero": "front-left floor point of the measured space",
        "positive_x": "right",
        "positive_y": "back",
        "positive_z": "up",
    }

    def valid(self, data, tree) -> bool:
        assemblies = data.get("assemblies") if data else None
        return bool(
            data
            and data.get("global_coordinates") == self._GLOBAL_COORDINATES
            and isinstance(assemblies, dict)
            and set(assemblies) == set(tree.root_child_ids)
            and all(
                self._valid_assembly(
                    assemblies[assembly_id], self._direct_parts(tree, assembly_id)
                )
                for assembly_id in tree.root_child_ids
            )
            and self._valid_relationships(data.get("relationships"), tree)
        )

    def _valid_assembly(self, record, parts: dict[str, str]) -> bool:
        positions = record.get("part_positions") if isinstance(record, dict) else None
        return bool(
            isinstance(record, dict)
            and set(record) == self._ASSEMBLY_KEYS
            and record.get("local_zero_mm") == [0.0, 0.0, 0.0]
            and self._vector(record.get("global_zero_mm"))
            and self._bounds(record.get("local_bounds"))
            and self._bounds(record.get("global_bounds"))
            and isinstance(positions, dict)
            and set(positions) == set(parts)
            and all(
                self._valid_part(positions[part_id], role)
                for part_id, role in parts.items()
            )
        )

    def _valid_part(self, record, role: str) -> bool:
        axes = record.get("local_axes_in_assembly") if isinstance(record, dict) else None
        return bool(
            isinstance(record, dict)
            and set(record) == self._PART_KEYS
            and record.get("role") == role
            and record.get("local_zero_mm") == [0.0, 0.0, 0.0]
            and self._vector(record.get("assembly_zero_mm"))
            and self._vector(record.get("global_zero_mm"))
            and isinstance(axes, dict)
            and set(axes) == {"x", "y", "z"}
            and all(self._vector(value) for value in axes.values())
            and self._bounds(record.get("assembly_bounds"))
            and self._bounds(record.get("global_bounds"))
        )

    def _valid_relationships(self, relationships, tree) -> bool:
        cabinets = tuple(item for item in tree.root_child_ids if item != "base_01")
        return bool(
            isinstance(relationships, dict)
            and set(relationships) == self._RELATIONSHIP_KEYS
            and relationships.get("cabinet_count") == len(cabinets)
            and self._number(relationships.get("base_top_z_mm"))
            and relationships.get("plinth_front") in {"flush", "recessed"}
            and self._number(relationships.get("plinth_recess_mm"))
            and self._number(relationships.get("plinth_front_y_mm"))
            and self._numbers(relationships.get("cabinet_gaps_mm"), len(cabinets) - 1)
            and isinstance(relationships.get("door_bottoms_z_mm"), dict)
            and set(relationships["door_bottoms_z_mm"]) == set(cabinets)
            and all(self._number(value) for value in relationships["door_bottoms_z_mm"].values())
        )

    def _direct_parts(self, tree, assembly_id: str) -> dict[str, str]:
        return {
            item.path.rsplit("/", 1)[-1]: item.part.spec.role
            for item in tree.parts
            if item.path.count("/") == 2 and f"/{assembly_id}/" in item.path
        }

    def _bounds(self, value) -> bool:
        return bool(
            isinstance(value, dict)
            and set(value) == {"minimum_mm", "maximum_mm"}
            and self._vector(value["minimum_mm"])
            and self._vector(value["maximum_mm"])
            and all(
                minimum < maximum
                for minimum, maximum in zip(value["minimum_mm"], value["maximum_mm"])
            )
        )

    def _numbers(self, values, expected_count: int) -> bool:
        return bool(
            isinstance(values, list)
            and len(values) == max(0, expected_count)
            and all(self._number(value) for value in values)
        )

    def _vector(self, value) -> bool:
        return isinstance(value, list) and len(value) == 3 and all(
            self._number(item) for item in value
        )

    def _number(self, value) -> bool:
        return (
            not isinstance(value, bool)
            and isinstance(value, (int, float))
            and isfinite(value)
        )


__all__ = ["FabricationPositionRecordValidator"]
