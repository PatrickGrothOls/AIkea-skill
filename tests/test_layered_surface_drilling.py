"""Scope: Prove layer splitting against one independent cutter and fail material gaps."""
from dataclasses import replace

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from layered_surface_drilling import LayeredSurfaceDrilling
from local_to_parent_location import LocalToParentLocation
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from surface_hole_pattern import SurfaceHole
from framed_front_test_support import FramedFrontTestSupport


class TestLayeredSurfaceDrilling(FramedFrontTestSupport):
    @pytest.mark.parametrize("reverse", (False, True))
    @pytest.mark.parametrize("translated", (False, True))
    def test_pattern_is_split_into_real_material(self, contracts, reverse, translated):
        _, builders, values, _, panels = contracts
        built = builders.FramedFrontBuilder(self.front(contracts)).build()
        surface = values.IDENTITY_LOCAL_TO_PARENT
        if reverse:
            surface = values.LocalToParentPlacement(values.Point3D(0, 0, 16),
                values.AxisBasis(values.AxisDirection(1,0,0), values.AxisDirection(0,-1,0), values.AxisDirection(0,0,-1)))
        if translated:
            parent = values.LocalToParentPlacement(values.Point3D(200,400,60),
                values.AxisBasis(values.AxisDirection(0,0,1), values.AxisDirection(1,0,0), values.AxisDirection(0,1,0)))
            parts = tuple(replace(part.spec, local_to_parent=parent.compose_child(part.spec.local_to_parent)) for part in built.parts)
            surface = parent.compose_child(surface)
            built = replace(built, spec=replace(built.spec, parts=parts), parts=tuple(
                replace(part, spec=spec) for part, spec in zip(built.parts, parts)))
        holes = (SurfaceHole("cup", 22, -140 if reverse else 140, 35, 11.5),
                 SurfaceHole("fix", 22, -180 if reverse else 180, 2.5, 10))
        requests = LayeredSurfaceDrilling().build("hinge", built.spec.parts, surface, holes)
        result = PanelMachiningFeature().apply(built, requests)
        assert {item.part_id for item in requests} == {"backing", "frame"}
        assert ConstructionResultValidator().validate(result) == ()
        for before, after in zip(built.parts, result.parts):
            frame = LocalToParentLocation().build(before.spec.local_to_parent)
            local = frame.inverse * LocalToParentLocation().build(surface)
            expected = before.solid.val()
            for hole in holes:
                expected = expected.cut(cq.Solid.makeCylinder(hole.diameter_mm/2, hole.depth_mm,
                    cq.Vector(hole.x_mm, hole.y_mm, 0)).located(local))
            actual = after.solid.val()
            assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)

    @pytest.mark.parametrize("offset", (-1, 1))
    def test_gaps_and_overlapping_layers_fail(self, contracts, offset):
        _, builders, values, _, _ = contracts
        recipe = builders.FramedFrontBuilder(self.front(contracts)).recipe()
        frame = recipe.parts[1]
        moved = replace(frame, local_to_parent=replace(frame.local_to_parent,
            origin_in_parent=values.Point3D(0,0,9+offset)))
        with pytest.raises(PartConstructionError, match="gap or overlap"):
            LayeredSurfaceDrilling().build("hinge", (recipe.parts[0], moved), values.IDENTITY_LOCAL_TO_PARENT,
                (SurfaceHole("cup",22,140,35,11.5),))

    @pytest.mark.parametrize("x,depth", ((10,11.5), (22,17), (100,11.5)))
    def test_edge_depth_and_frame_opening_fail(self, contracts, x, depth):
        _, builders, values, _, _ = contracts
        built = builders.FramedFrontBuilder(self.front(contracts)).build()
        with pytest.raises(PartConstructionError):
            requests = LayeredSurfaceDrilling().build("hinge", built.spec.parts, values.IDENTITY_LOCAL_TO_PARENT,
                (SurfaceHole("cup",x,140,35,depth),))
            PanelMachiningFeature().apply(built, requests)
