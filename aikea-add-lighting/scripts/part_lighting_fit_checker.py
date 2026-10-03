"""Scope: Check one grooved part, purchased light, and cabinet-facing direction."""

from __future__ import annotations

from typing import Any

from cabinet_lighting_placement import CabinetLightingPlacement
from lighting_run_boundary_checker import LightingRunBoundaryChecker
from part_lighting_builder import BuiltPartLighting
from part_lighting_fit_report import PartLightingFitReport
from part_lighting_plan import PartLightingPlan


class PartLightingFitChecker:
    """Prove the approved run fits without crossing existing panel machining."""

    VOLUME_TOLERANCE_MM3 = 0.01

    def __init__(self) -> None:
        self.boundary = LightingRunBoundaryChecker()

    def check(
        self,
        assembly: Any,
        original_part: Any,
        lighting: BuiltPartLighting,
        plan: PartLightingPlan,
        placement: CabinetLightingPlacement,
        other_parts: tuple[Any, ...] = (),
    ) -> PartLightingFitReport:
        face = lighting.face_frame
        run_inside = self.boundary.is_inside(face.width_mm, face.height_mm, plan.run)
        remaining = face.material_depth_mm - plan.run.profile.groove_depth_mm
        groove_within = remaining >= 0.0
        placed_cutter = lighting.groove_cutter.val().located(
            lighting.lighting_in_part
        )
        cutter_volume = placed_cutter.Volume()
        available_volume = original_part.solid.val().intersect(placed_cutter).Volume()
        existing_overlap = max(0.0, cutter_volume - available_volume)
        avoids_existing = existing_overlap <= self.VOLUME_TOLERANCE_MM3
        placed_body = lighting.luminaire_body.val().located(
            lighting.lighting_in_part
        )
        body_overlap = lighting.part.solid.val().intersect(placed_body).Volume()
        body_fits = body_overlap <= self.VOLUME_TOLERANCE_MM3
        body_in_cabinet = lighting.luminaire_body.val().located(
            placement.luminaire_location
        )
        other_overlap = sum(
            body_in_cabinet.intersect(part.placed_shape()).Volume()
            for part in other_parts
        )
        avoids_other_parts = other_overlap <= self.VOLUME_TOLERANCE_MM3
        points_inward = self._points_into_cabinet(assembly, placement)
        passed = all(
            (
                run_inside,
                groove_within,
                avoids_existing,
                body_fits,
                avoids_other_parts,
                points_inward,
            )
        )
        return PartLightingFitReport(
            status="pass" if passed else "fail",
            run_inside_host_face=run_inside,
            groove_within_host_thickness=groove_within,
            groove_avoids_existing_machining=avoids_existing,
            purchased_body_fits_groove=body_fits,
            purchased_body_avoids_other_parts=avoids_other_parts,
            emission_points_into_cabinet=points_inward,
            remaining_material_mm=remaining,
            existing_machining_overlap_mm3=existing_overlap,
            purchased_body_overlap_mm3=body_overlap,
            other_part_overlap_mm3=other_overlap,
            frame_path=placement.as_record(),
        )

    def _points_into_cabinet(
        self,
        assembly: Any,
        placement: CabinetLightingPlacement,
    ) -> bool:
        origin = placement.luminaire_in_cabinet.origin_mm
        normal = placement.luminaire_in_cabinet.local_z_in_parent
        cabinet_center = (
            float(assembly.width_mm) / 2.0,
            float(assembly.inside_depth_mm) / 2.0,
            float(assembly.base_height_mm) + max(point.height_mm for point in assembly.top) / 2.0,
        )
        toward_center = tuple(center - start for center, start in zip(cabinet_center, origin))
        return sum(component * direction for component, direction in zip(toward_center, normal)) > 0.0


__all__ = ["PartLightingFitChecker"]
