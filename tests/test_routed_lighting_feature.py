"""Scope: Check routed light composition, slope orientation and manufacturing audit integrity."""

from dataclasses import replace
from math import sqrt
from pathlib import Path

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from local_to_parent_location import LocalToParentLocation
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from routed_lighting_feature import RoutedLightingFeature
from lighting_route import LightingRoute
from lighting_component_feature import LightingComponentFeature
from stepped_surface_recess import RecessRegion, SteppedSurfaceRecessSpec
from test_lighting_route import TestLightingRoute as RouteFixtures


class TestRoutedLightingFeature:
    contracts = RouteFixtures.contracts
    _contracts = RouteFixtures._contracts

    def test_purchase_fits_cut_and_keeps_services_unresolved(self, contracts):
        base = RouteFixtures()._base(contracts)
        base = replace(base, spec=replace(base.spec, requirements=()))
        result = self._apply(contracts, base, RouteFixtures()._spec(end="start"))
        assert len(result.cuts) == len(result.purchased_hardware) == 1
        hardware = result.purchased_hardware[0]
        installed = hardware.solid.val().located(LocalToParentLocation().build(hardware.spec.local_to_parent))
        assert installed.intersect(result.parts[0].solid.val()).Volume() == pytest.approx(0, abs=1e-5)
        assert result.spec.requirements[-1].disposition == "unresolved"
        assert ConstructionResultValidator().validate(result) == ()

    def test_changed_recess_cannot_reuse_old_solid(self, contracts):
        base = RouteFixtures()._base(contracts)
        result = self._apply(contracts, base, RouteFixtures()._spec())
        request = result.spec.machining[0]
        regions = (replace(request.regions[0], width_mm=5), *request.regions[1:])
        changed = replace(result, spec=replace(result.spec, machining=(replace(request, regions=regions),)))
        with pytest.raises(PartConstructionError, match="cutter differs"):
            ConstructionResultValidator().validate(changed)

    def test_slope_edge_in_polygon(self, contracts):
        values, panels = contracts
        base = RouteFixtures()._base(contracts)
        # The blank's front edge itself is oblique in its own machining plane.
        point_type = values.BoundaryPoint
        part = replace(base.spec.parts[0], local_size_mm=(100, 150, 16),
            outline_mm=tuple(point_type(x, y) for x, y in ((0, 0), (100, 50), (100, 150), (0, 100))))
        base = panels.PanelAssemblyBuilder(replace(base.spec, parts=(part,))).build()
        spec = replace(RouteFixtures()._spec(end="start"), front_edge_mm=((0, 0), (100, 50)), start_margin_mm=20)
        resolved = LightingRoute().build(part, spec)
        actual = resolved.light_plan.run.start_mm
        assert actual == pytest.approx(((38*2-20)/sqrt(5), (38+20*2)/sqrt(5)))
        result = PanelMachiningFeature().apply(base, (resolved.machining,))
        assert ConstructionResultValidator().validate(result) == ()

    def test_generic_union_volume_without_double_counting(self, contracts):
        values, _ = contracts
        base = RouteFixtures()._base(contracts)
        request = SteppedSurfaceRecessSpec("stepped", "panel", values.IDENTITY_LOCAL_TO_PARENT,
            (RecessRegion((10, 20), 60, 10, 6, 0), RecessRegion((10, 20), 60, 4, 10, 0)))
        result = PanelMachiningFeature().apply(base, (request,))
        assert base.parts[0].solid.val().Volume()-result.parts[0].solid.val().Volume() == pytest.approx(60*10*6+60*4*4)

    def test_wrong_owner_rejected(self, contracts):
        base = RouteFixtures()._base(contracts)
        with pytest.raises(ValueError, match="owning assembly"):
            RoutedLightingFeature(replace(RouteFixtures()._spec(), assembly_id="other")).apply(base)

    def test_machining_cannot_target_a_different_light_host(self, contracts):
        base = RouteFixtures()._base(contracts)
        resolved = LightingRoute().build(base.spec.parts[0], RouteFixtures()._spec())
        feature = LightingComponentFeature(resolved.light_plan, replace(resolved.machining, part_id="other"))
        root = Path(contracts[0].__file__).parents[1]
        with pytest.raises(ValueError, match="share their host"):
            GeneratedProjectModuleRuntime().execute(root, lambda: feature.apply(base))

    def _apply(self, contracts, base, spec):
        root = Path(contracts[0].__file__).parents[1]
        return GeneratedProjectModuleRuntime().execute(root, lambda: RoutedLightingFeature(spec).apply(base))
