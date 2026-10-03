"""Scope: Prove exact drawer hardware frames and classify their CAD overlaps."""

from __future__ import annotations

from typing import Any

from drawer_hardware_overlap_checker import DrawerHardwareOverlapChecker
from drawer_hardware_position_report import DrawerHardwarePositionReport
from hardware_cabinet_frame import HardwareCabinetFrameComposer
from local_to_parent_location import LocalToParentLocation
from movento_mounting_profile import MOVENTO_760H5000S_MOUNTING


class DrawerHardwarePositionChecker:
    """Check one closed runner-and-lock set against its owning wooden parts."""

    _TOLERANCE_MM = 1e-6
    _HANDS = ("left", "right")

    def __init__(self) -> None:
        self.frame_composer = HardwareCabinetFrameComposer()
        self.location = LocalToParentLocation()
        self.overlap_checker = DrawerHardwareOverlapChecker()

    def check(
        self,
        built_cabinet: Any,
        cabinet_parts: tuple[Any, ...],
        drawer_parts: tuple[Any, ...],
        hardware_set: Any,
    ) -> DrawerHardwarePositionReport:
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        runner_specs = self._specs(built_cabinet.purchased_hardware)
        lock_specs = self._specs(child.assembly.purchased_hardware)
        frames, shapes = self._hardware(child, runner_specs, lock_specs, hardware_set)
        wood = {part.name: part.placed_shape() for part in cabinet_parts + drawer_parts}
        contacts = self.overlap_checker.cabinet_side_contacts(shapes, wood)
        lock_relations = self.overlap_checker.locking_device_mounting_relations(
            shapes,
            wood,
            float(child.assembly.spec.box.sizing.bottom_underside_recess_mm),
        )
        wood_overlaps = self.overlap_checker.wood_overlaps(shapes, wood)
        engagements = self.overlap_checker.manufacturer_engagement_overlaps(shapes)
        unintended = tuple(
            overlap
            for overlap in wood_overlaps
            if overlap["classification"] == "unintended_wood_overlap"
        )
        checks = tuple(
            {"name": name, "passed": passed}
            for name, passed in (
                *self._frame_checks(frames),
                *(
                    (
                        f"{contact['hardware_id']} contacts {contact['wood_part_id']} without overlap",
                        contact["contact"] and contact["overlap_volume_mm3"] <= self._TOLERANCE_MM,
                    )
                    for contact in contacts
                ),
                *(
                    (
                        f"{relation['hardware_id']} seats at the drawer front and clears the recessed bottom",
                        self._lock_relation_passes(relation),
                    )
                    for relation in lock_relations
                ),
                ("hardware has no unintended wood overlap", not unintended),
            )
        )
        return DrawerHardwarePositionReport(
            frames={name: frame.as_dict() for name, frame in frames.items()},
            fixing_depths_from_drawer_front_mm=self._fixing_depths(),
            cabinet_side_contacts=contacts,
            locking_device_mounting_relations=lock_relations,
            wood_overlaps=wood_overlaps,
            manufacturer_engagement_overlaps=engagements,
            checks=checks,
        )

    def _specs(self, items: tuple[Any, ...]) -> dict[str, Any]:
        return {item.spec.hardware_id: item.spec for item in items}

    def _hardware(self, child, runner_specs, lock_specs, hardware_set):
        frames, shapes = {}, {}
        child_location = self.location.build(child.spec.local_to_parent)
        for hand in self._HANDS:
            runner_id = f"runner_{hand}"
            lock_id = f"locking_device_{hand}"
            runner = runner_specs[runner_id].local_to_parent
            lock = lock_specs[lock_id].local_to_parent
            frames[runner_id] = self.frame_composer.compose(runner)
            frames[lock_id] = self.frame_composer.compose(
                lock, child.spec.local_to_parent
            )
            shapes[runner_id] = getattr(hardware_set, runner_id).shape.located(
                self.location.build(runner)
            )
            shapes[lock_id] = getattr(hardware_set, lock_id).shape.located(
                child_location * self.location.build(lock)
            )
        return frames, shapes

    def _frame_checks(self, frames):
        return tuple(
            (
                f"{hand} runner and locking-device closed frames align",
                frames[f"runner_{hand}"].matches(
                    frames[f"locking_device_{hand}"], self._TOLERANCE_MM
                ),
            )
            for hand in self._HANDS
        )

    def _lock_relation_passes(self, relation: dict[str, Any]) -> bool:
        return all(
            (
                relation["front_distance_mm"] <= self._TOLERANCE_MM,
                relation["front_overlap_volume_mm3"] <= self._TOLERANCE_MM,
                abs(
                    relation["bottom_clearance_mm"]
                    - relation["expected_bottom_clearance_mm"]
                )
                <= self._TOLERANCE_MM,
                relation["bottom_overlap_volume_mm3"] <= self._TOLERANCE_MM,
            )
        )

    def _fixing_depths(self) -> tuple[float, ...]:
        profile = MOVENTO_760H5000S_MOUNTING
        return tuple(
            profile.drawer_front_to_manufacturer_origin_mm - native_z
            for native_z in profile.runner_screw_native_z_mm
        )

__all__ = ["DrawerHardwarePositionChecker"]
