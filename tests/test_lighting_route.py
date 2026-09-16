"""Scope: Prove route placement, exact subtraction, setup faces and rejection boundaries."""

from dataclasses import replace

import cadquery as cq
import pytest

from lighting_route import LightingRoute
from lighting_route_spec import ConnectorPocket, LightingRouteSpec
from panel_machining_feature import PanelMachiningFeature
from panel_setup_checker import PanelSetupChecker
from part_construction_error import PartConstructionError
from recessed_luminaire_profile import DOMUS_APEX_84_HI
from test_shared_surface_drilling import TestSharedSurfaceDrilling as Fixtures


class TestLightingRoute:
    contracts = Fixtures.contracts
    _contracts = Fixtures._contracts

    def _spec(self, face=">Z", end="none"):
        return LightingRouteSpec("lighting_01", "panel", "light", face,
            ((0, 0), (100, 0)), 20, 5, 5, DOMUS_APEX_84_HI, 4300,
            2, 10, 0.5, 6, end, None if end == "none" else ConnectorPocket(20, 8, 9, 1, 18))

    def _base(self, contracts):
        values, panels = contracts
        part = values.PartSpec("panel", "routing coupon", (), values.IDENTITY_LOCAL_TO_PARENT,
                              local_size_mm=(100, 80, 16), material_id="mdf")
        return panels.PanelAssemblyBuilder(panels.PanelAssemblySpec("lighting_01", "custom", (part,))).build()

    @pytest.mark.parametrize("face", ("<Z", ">Z"))
    @pytest.mark.parametrize("end", ("none", "start", "end"))
    def test_exact_geometry_light_alignment_and_setup(self, contracts, face, end):
        base = self._base(contracts)
        resolved = LightingRoute().build(base.spec.parts[0], self._spec(face, end))
        result = PanelMachiningFeature().apply(base, (resolved.machining,))
        # Independent known coupon coordinates: route is x=5..95, y=20.
        lo, hi = (23 if end == "start" else 5), (77 if end == "end" else 95)
        seat = self._pocket(lo-0.5, 20, hi-lo+1, 4, 8, 0.5)
        cable = self._pocket(5, 20, 90, 2, 10, 0.5)
        cutter = seat.fuse(cable)
        if end != "none":
            cutter = cutter.fuse(self._pocket(5 if end == "start" else 75, 20, 20, 8, 9, 1))
        if face == ">Z":
            cutter = cutter.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, 16))
            # The independent inward frame uses -Y; restore physical face-local Y.
            cutter = cutter.translate((0, 40, 0))
        else:
            cutter = cutter.rotate((0, 0, 0), (0, 1, 0), 180).translate((100, 0, 0))
            cutter = cutter.rotate((0, 0, 0), (1, 0, 0), 180)
            cutter = cutter.translate((0, 40, 0))
        blank = base.parts[0].solid.val()
        expected, actual = blank.cut(cutter), result.parts[0].solid.val()
        assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert blank.Volume()-actual.Volume() == pytest.approx(cutter.Volume(), abs=1e-5)
        assert resolved.light_plan.run.start_mm == (lo, 20)
        assert resolved.light_plan.run.end_mm == (hi, 20)
        assert PanelSetupChecker().check(result)["parts"][0]["allowed_faces"] == [face]
        assert len(result.cuts) == 1

    def _pocket(self, x, y, length, width, depth, radius):
        return (cq.Workplane("XY").box(length, width, depth, centered=(False, True, False))
                .edges("|Z").fillet(radius).val().translate((x, y, 0)))

    def test_reversed_front_edge_and_end_assignment(self, contracts):
        base = self._base(contracts)
        spec = replace(self._spec(end="end"), front_edge_mm=((100, 80), (0, 80)))
        result = LightingRoute().build(base.spec.parts[0], spec)
        assert result.route_start_mm == (95, 60)
        assert result.light_plan.run.start_mm == (95, 60)
        assert result.light_plan.run.end_mm == (23, 60)
        PanelMachiningFeature().apply(base, (result.machining,))

    @pytest.mark.parametrize("changes,match", (
        ({"connector_end": "start"}, "together"),
        ({"connector_end": "middle"}, "none, start or end"),
        ({"face": ">X"}, "broad"),
        ({"cable_width_mm": 4}, "shoulders"),
        ({"cable_depth_mm": 8}, "behind"),
        ({"inset_mm": float("nan")}, "finite"),
        ({"cutter_radius_mm": 1}, "radius")))
    def test_invalid_inputs(self, changes, match):
        with pytest.raises(ValueError, match=match):
            replace(self._spec(), **changes)

    @pytest.mark.parametrize("changes,match", (
        ({"minimum_stock_mm": 7}, "remaining stock"),
        ({"start_margin_mm": 60, "end_margin_mm": 50}, "no usable"),
        ({"front_edge_mm": ((0, 10), (100, 10))}, "boundary"),
        ({"inset_mm": 79}, "entry face")))
    def test_unmachinable_routes(self, contracts, changes, match):
        base = self._base(contracts)
        with pytest.raises((ValueError, PartConstructionError), match=match):
            LightingRoute().build(base.spec.parts[0], replace(self._spec(), **changes))

    def test_unrelated_prior_cut_still_rejected(self, contracts):
        base = self._base(contracts)
        route = LightingRoute().build(base.spec.parts[0], self._spec())
        prior = replace(route.machining, machining_id="earlier")
        built = PanelMachiningFeature().apply(base, (prior,))
        with pytest.raises(PartConstructionError, match="clipped|does not machine"):
            PanelMachiningFeature().apply(built, (route.machining,))
