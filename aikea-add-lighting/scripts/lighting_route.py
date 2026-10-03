"""Scope: Resolve one front-edge route into its light plan and common stepped machining."""

from dataclasses import dataclass

import cadquery as cq

from lighting_machining_recipe import LightingMachiningRecipe
from lighting_run import LightingRun
from panel_blank_builder import PanelBlankBuilder
from part_face_frame import PartFaceFrameBuilder
from part_lighting_plan import PartLightingPlan
from stepped_surface_recess import RecessRegion, SteppedSurfaceRecessBuilder, SteppedSurfaceRecessSpec


@dataclass(frozen=True)
class ResolvedLightingRoute:
    light_plan: PartLightingPlan
    machining: SteppedSurfaceRecessSpec
    route_start_mm: tuple[float, float]
    route_end_mm: tuple[float, float]


class LightingRoute:
    """Start/end follow the supplied front edge; its left normal points into the panel."""

    def build(self, part, spec):
        if part.part_id != spec.part_id:
            raise ValueError("lighting route and host part differ")
        face = PartFaceFrameBuilder().build(part, spec.face)
        self._check_front_edge(part, face, spec.front_edge_mm)
        a, b = spec.front_edge_mm
        dx, dy = (b[0]-a[0])/spec.edge_length_mm, (b[1]-a[1])/spec.edge_length_mm
        start = (a[0]-dy*spec.inset_mm+dx*spec.start_margin_mm,
                 a[1]+dx*spec.inset_mm+dy*spec.start_margin_mm)
        length = spec.edge_length_mm-spec.start_margin_mm-spec.end_margin_mm
        pocket = spec.connector_pocket
        setback = pocket.light_setback_mm if pocket else 0
        if length <= max(setback, pocket.length_mm if pocket else 0):
            raise ValueError("end margins and connector leave no usable light run")
        light_start = setback if spec.connector_end == "start" else 0
        light_end = length-setback if spec.connector_end == "end" else length
        run = LightingRun(spec.run_id, start, (start[0]+dx*length, start[1]+dy*length),
                          spec.color_temperature_k, spec.profile)
        full_plan = PartLightingPlan(spec.assembly_id, spec.part_id, spec.face, run)
        frame = LightingMachiningRecipe().build(part, full_plan).surface_to_part
        profile = spec.profile
        radius = spec.cutter_radius_mm
        regions = [RecessRegion((light_start-radius, 0), light_end-light_start+2*radius,
            profile.groove_width_mm, profile.groove_depth_mm, spec.cutter_radius_mm),
            RecessRegion((0, 0), length, spec.cable_width_mm,
                         spec.cable_depth_mm, spec.cutter_radius_mm)]
        if pocket:
            x = 0 if spec.connector_end == "start" else length-pocket.length_mm
            regions.append(RecessRegion((x, 0), pocket.length_mm, pocket.width_mm,
                                        pocket.depth_mm, pocket.corner_radius_mm))
        if max(r.depth_mm for r in regions)+spec.minimum_stock_mm > face.material_depth_mm:
            raise ValueError("lighting recess violates the specified remaining stock")
        request = SteppedSurfaceRecessSpec(spec.run_id+"_route", spec.part_id, frame, tuple(regions))
        cutter, location = SteppedSurfaceRecessBuilder().build(part, request)
        blank = PanelBlankBuilder().build(part).val()
        if cutter.located(location).cut(blank).Volume() > 1e-5:
            raise ValueError("lighting recess leaves the actual panel outline or stock")
        light = LightingRun(spec.run_id,
            (start[0]+dx*light_start, start[1]+dy*light_start),
            (start[0]+dx*light_end, start[1]+dy*light_end), spec.color_temperature_k, profile)
        return ResolvedLightingRoute(PartLightingPlan(spec.assembly_id, spec.part_id, spec.face, light),
                                     request, start, run.end_mm)

    def _check_front_edge(self, part, face, endpoints):
        edge = cq.Edge.makeLine(*(cq.Vector(x, y, 0) for x, y in endpoints)).located(face.location())
        boundary = cq.Compound.makeCompound(PanelBlankBuilder().build(part).val().Edges())
        if sum(segment.Length() for segment in edge.cut(boundary).Edges()) > 1e-6:
            raise ValueError("front edge must lie on the selected face's actual panel boundary")
