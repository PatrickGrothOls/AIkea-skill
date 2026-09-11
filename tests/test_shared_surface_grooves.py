"""Scope: Prove surface-groove parity, ownership and current-material rejection in the shared path."""

from dataclasses import replace

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from surface_groove_spec import SurfaceGrooveSpec
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from test_shared_surface_drilling import TestSharedSurfaceDrilling as DrillingFixture


class TestSharedSurfaceGrooves:
    contracts = DrillingFixture.contracts
    _contracts = DrillingFixture._contracts

    @pytest.mark.parametrize('top', (False, True))
    def test_common_build_and_feature_match_independent_groove(self, contracts, top):
        values, panels = contracts
        z, y = (16, 80) if top else (0, 20)
        axes = DrillingFixture()._surface(values, top).axis_basis
        surface = values.LocalToParentPlacement(values.Point3D(10, y, z), axes)
        request = SurfaceGrooveSpec('slot', 'panel', surface, 80, 4, 8)
        part = values.PartSpec('panel', 'arbitrary label', (), values.IDENTITY_LOCAL_TO_PARENT,
                              local_size_mm=(100, 100, 16), material_id='mdf')
        base = panels.PanelAssemblySpec('groove_01', 'custom', (part,), requirements=())
        built = panels.PanelAssemblyBuilder(replace(base, machining=(request,))).build()
        featured = PanelMachiningFeature().apply(panels.PanelAssemblyBuilder(base).build(), (request,))
        expected = cq.Solid.makeBox(100, 100, 16).cut(cq.Solid.makeBox(80, 4, 8, cq.Vector(10, y-2, 8 if top else 0)))
        for result in (built, featured):
            actual = result.parts[0].solid.val()
            assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
            assert ConstructionResultValidator().validate(result) == ()
            assert [(cut.joint_id, cut.part_id) for cut in result.cuts] == [('slot', 'panel')]
        changed = replace(built.spec, machining=(replace(request, width_mm=6),))
        with pytest.raises(PartConstructionError, match='cutter differs'):
            ConstructionResultValidator().validate(replace(built, spec=changed))

    @pytest.mark.parametrize('origin,depth,message', (((10, 20, 4), 8, 'entry face'),
        ((-1, 20, 0), 8, 'entry face'), ((10, 20, 0), 17, 'clipped')))
    def test_inaccessible_or_clipped_groove_rejected(self, contracts, origin, depth, message):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        moved = replace(request, depth_mm=depth, surface_to_part=values.LocalToParentPlacement(values.Point3D(*origin), values.IDENTITY_AXIS_BASIS))
        with pytest.raises(PartConstructionError, match=message):
            panels.PanelAssemblyBuilder(replace(spec, machining=(moved,))).build()

    def test_existing_hole_cannot_be_hidden_by_later_groove(self, contracts):
        values, panels = contracts
        spec, groove = self._spec(values, panels)
        hole = SurfaceDrillingSpec('prior', 'panel', values.IDENTITY_LOCAL_TO_PARENT, (SurfaceHole('fix', 50, 20, 3, 10),))
        before = panels.PanelAssemblyBuilder(replace(spec, machining=(hole,))).build()
        with pytest.raises(PartConstructionError, match='clipped'):
            PanelMachiningFeature().apply(before, (groove,))

    @pytest.mark.parametrize('size', (0, -1, float('nan'), float('inf')))
    def test_invalid_dimensions_fail_at_boundary(self, contracts, size):
        values, panels = contracts
        spec, request = self._spec(values, panels)
        with pytest.raises(PartConstructionError, match='finite and positive'):
            panels.PanelAssemblyBuilder(replace(spec, machining=(replace(request, width_mm=size),))).build()

    def _spec(self, values, panels):
        part = values.PartSpec('panel', 'custom', (), values.IDENTITY_LOCAL_TO_PARENT,
                              local_size_mm=(100, 100, 16), material_id='mdf')
        surface = values.LocalToParentPlacement(values.Point3D(10, 20, 0), values.IDENTITY_AXIS_BASIS)
        return panels.PanelAssemblySpec('groove_01', 'custom', (part,)), SurfaceGrooveSpec('slot', 'panel', surface, 80, 4, 8)
