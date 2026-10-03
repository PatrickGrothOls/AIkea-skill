"""Scope: Compare pocket cuts with independent rounded solids and protect common validation."""
from dataclasses import replace
from math import pi

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from surface_pocket_spec import SurfacePocketSpec
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from test_shared_surface_drilling import TestSharedSurfaceDrilling as DrillingFixture


class TestSharedSurfacePockets:
    contracts = DrillingFixture.contracts
    _contracts = DrillingFixture._contracts

    @pytest.mark.parametrize('depth', (6, 16))
    @pytest.mark.parametrize('top', (False, True))
    def test_blind_and_through_pockets_match_independent_geometry(self, contracts, depth, top):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        axes = DrillingFixture()._surface(values, top).axis_basis
        request = replace(request, depth_mm=depth, surface_to_part=values.LocalToParentPlacement(
            values.Point3D(10, 50, 16 if top else 0), axes))
        built = panels.PanelAssemblyBuilder(replace(spec, machining=(request,))).build()
        featured = PanelMachiningFeature().apply(panels.PanelAssemblyBuilder(spec).build(), (request,))
        cutter = self._rounded_opening(depth).translate((10,20,16-depth if top else 0))
        expected = cq.Solid.makeBox(100, 100, 16).cut(cutter)
        for result in (built, featured):
            actual = result.parts[0].solid.val()
            assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
            assert actual.Volume() == pytest.approx(160000-(80*60-(4-pi)*4**2)*depth)
            assert ConstructionResultValidator().validate(result) == ()
        changed = replace(built.spec, machining=(replace(request, corner_radius_mm=5),))
        with pytest.raises(PartConstructionError, match='cutter differs'):
            ConstructionResultValidator().validate(replace(built, spec=changed))

    @pytest.mark.parametrize('radius', (-1, 30, float('nan'), float('inf')))
    def test_invalid_corner_radii_fail(self, contracts, radius):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        with pytest.raises(PartConstructionError, match='radius'):
            panels.PanelAssemblyBuilder(replace(spec, machining=(replace(request, corner_radius_mm=radius),))).build()

    @pytest.mark.parametrize('origin,depth,message', (((10,50,4), 6, 'entry face'),
        ((-1,50,0), 6, 'entry face'), ((10,50,0), 17, 'clipped')))
    def test_pocket_entry_and_depth_must_match_stock(self, contracts, origin, depth, message):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        request = replace(request, depth_mm=depth, surface_to_part=values.LocalToParentPlacement(values.Point3D(*origin), values.IDENTITY_AXIS_BASIS))
        with pytest.raises(PartConstructionError, match=message):
            panels.PanelAssemblyBuilder(replace(spec, machining=(request,))).build()

    def test_square_pocket_and_prior_cut_collision(self, contracts):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        square = panels.PanelAssemblyBuilder(replace(spec, machining=(replace(request, corner_radius_mm=0),))).build()
        assert square.parts[0].solid.val().Volume() == pytest.approx(160000-80*60*6)
        hole = SurfaceDrillingSpec('prior', 'panel', values.IDENTITY_LOCAL_TO_PARENT, (SurfaceHole('fix', 50, 50, 3, 10),))
        before = panels.PanelAssemblyBuilder(replace(spec, machining=(hole,))).build()
        with pytest.raises(PartConstructionError, match='clipped'):
            PanelMachiningFeature().apply(before, (request,))

    def _spec(self, values, panels):
        part = values.PartSpec('panel', 'custom', (), values.IDENTITY_LOCAL_TO_PARENT,
                              local_size_mm=(100,100,16), material_id='mdf')
        surface = values.LocalToParentPlacement(values.Point3D(10,50,0), values.IDENTITY_AXIS_BASIS)
        return panels.PanelAssemblySpec('pocket_01', 'custom', (part,), requirements=()), SurfacePocketSpec('opening', 'panel', surface, 80,60,6,4)

    def _rounded_opening(self, depth):
        solids = [cq.Solid.makeBox(72,60,depth,cq.Vector(4,0,0)), cq.Solid.makeBox(80,52,depth,cq.Vector(0,4,0))]
        solids.extend(cq.Solid.makeCylinder(4,depth,cq.Vector(x,y,0)) for x in (4,76) for y in (4,56))
        return solids[0].fuse(*solids[1:]).clean()
