"""Scope: Measure and classify exact drawer-hardware CAD overlaps."""

from __future__ import annotations

from typing import Any

from runner_back_preparation_zone import RunnerBackPreparationZone


class DrawerHardwareOverlapChecker:
    """Separate known preparation and engagement from unintended overlap."""

    _TOLERANCE_MM = 1e-6
    _LOCKING_DEVICE_PAD_RELIEF_MM = 0.2
    _HANDS = ("left", "right")

    def __init__(self) -> None:
        self.rear_preparation = RunnerBackPreparationZone()

    def cabinet_side_contacts(
        self,
        shapes: dict[str, Any],
        wood: dict[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        contacts = []
        for hand in self._HANDS:
            hardware_id = f"runner_{hand}"
            wood_id = f"{hand}_side"
            distance_mm = shapes[hardware_id].distance(wood[wood_id])
            contacts.append(
                {
                    "hardware_id": hardware_id,
                    "wood_part_id": wood_id,
                    "distance_mm": distance_mm,
                    "overlap_volume_mm3": self.overlap(
                        shapes[hardware_id], wood[wood_id]
                    ),
                    "contact": distance_mm <= self._TOLERANCE_MM,
                }
            )
        return tuple(contacts)

    def locking_device_mounting_relations(
        self,
        shapes: dict[str, Any],
        wood: dict[str, Any],
        bottom_underside_recess_mm: float,
    ) -> tuple[dict[str, Any], ...]:
        front_id = next(name for name in wood if name.endswith("__front"))
        bottom_id = next(name for name in wood if name.endswith("__bottom"))
        expected_bottom_clearance_mm = (
            bottom_underside_recess_mm + self._LOCKING_DEVICE_PAD_RELIEF_MM
        )
        relations = []
        for hand in self._HANDS:
            hardware_id = f"locking_device_{hand}"
            relations.append(
                {
                    "hardware_id": hardware_id,
                    "front_part_id": front_id,
                    "front_distance_mm": shapes[hardware_id].distance(wood[front_id]),
                    "front_overlap_volume_mm3": self.overlap(
                        shapes[hardware_id], wood[front_id]
                    ),
                    "bottom_part_id": bottom_id,
                    "bottom_clearance_mm": shapes[hardware_id].distance(
                        wood[bottom_id]
                    ),
                    "expected_bottom_clearance_mm": expected_bottom_clearance_mm,
                    "bottom_overlap_volume_mm3": self.overlap(
                        shapes[hardware_id], wood[bottom_id]
                    ),
                    "relation": "front_contact_with_recessed_bottom_clearance",
                }
            )
        return tuple(relations)

    def wood_overlaps(
        self,
        shapes: dict[str, Any],
        wood: dict[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        overlaps = []
        for hardware_id, hardware_shape in shapes.items():
            for wood_id, wood_shape in wood.items():
                volume = self.overlap(hardware_shape, wood_shape)
                if volume <= self._TOLERANCE_MM:
                    continue
                rear_preparation = self.rear_preparation.contains(
                    hardware_id, wood_id, hardware_shape, wood_shape
                )
                overlaps.append(
                    {
                        "hardware_id": hardware_id,
                        "wood_part_id": wood_id,
                        "overlap_volume_mm3": volume,
                        "classification": (
                            "rear_preparation_required"
                            if rear_preparation
                            else "unintended_wood_overlap"
                        ),
                    }
                )
        return tuple(overlaps)

    def manufacturer_engagement_overlaps(
        self,
        shapes: dict[str, Any],
    ) -> tuple[dict[str, Any], ...]:
        return tuple(
            {
                "runner_id": f"runner_{hand}",
                "locking_device_id": f"locking_device_{hand}",
                "overlap_volume_mm3": self.overlap(
                    shapes[f"runner_{hand}"], shapes[f"locking_device_{hand}"]
                ),
                "classification": "manufacturer_engagement_overlap",
            }
            for hand in self._HANDS
        )

    def overlap(self, left: Any, right: Any) -> float:
        if not self._bounding_boxes_overlap(left, right):
            return 0.0
        return left.intersect(right).Volume()

    def _bounding_boxes_overlap(self, left: Any, right: Any) -> bool:
        left_bounds = left.BoundingBox()
        right_bounds = right.BoundingBox()
        separated = (
            left_bounds.xmax < right_bounds.xmin - self._TOLERANCE_MM,
            right_bounds.xmax < left_bounds.xmin - self._TOLERANCE_MM,
            left_bounds.ymax < right_bounds.ymin - self._TOLERANCE_MM,
            right_bounds.ymax < left_bounds.ymin - self._TOLERANCE_MM,
            left_bounds.zmax < right_bounds.zmin - self._TOLERANCE_MM,
            right_bounds.zmax < left_bounds.zmin - self._TOLERANCE_MM,
        )
        return not any(separated)


__all__ = ["DrawerHardwareOverlapChecker"]
