"""Scope: Compose routed machining and its matching purchased light into an assembly."""

from dataclasses import dataclass

from lighting_component_feature import LightingComponentFeature
from lighting_route import LightingRoute
from lighting_route_spec import LightingRouteSpec


@dataclass(frozen=True)
class RoutedLightingFeature:
    route: LightingRouteSpec

    def apply(self, assembly):
        if assembly.spec.assembly_id != self.route.assembly_id:
            raise ValueError("lighting route and owning assembly differ")
        host = assembly.spec.part(self.route.part_id)
        resolved = LightingRoute().build(host, self.route)
        return LightingComponentFeature(resolved.light_plan, resolved.machining).apply(assembly)
