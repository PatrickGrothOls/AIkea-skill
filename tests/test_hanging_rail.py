"""Scope: Verify opposite support mounting, physical drilling and rail quantities."""
from dataclasses import replace
from math import pi
import importlib
import pytest
from assembly_composition_test_case import AssemblyCompositionTestCase
from test_cabinet_construction_defaults import TestCabinetConstructionDefaults as CabinetFixture
from hanging_rail_feature import HangingRailFeature
from hanging_rail_layout import HangingRailLayout


class TestHangingRail(AssemblyCompositionTestCase):
    def cabinet(self, generated_values):
        values, _ = generated_values
        panels = importlib.import_module('assemblies.panel_assembly')
        spec = CabinetFixture()._shelf_spec(values, panels)
        return panels.PanelAssemblyBuilder(spec).build()

    def feature(self, **changes):
        return HangingRailFeature(replace(HangingRailLayout('hanging_01', 'left_side',
                                  'right_side', 200, 350), **changes))

    def test_complete_installation_cuts_six_blind_holes_and_preserves_shelf(self, generated_values):
        before = self.cabinet(generated_values)
        feature = self.feature()
        built = feature.apply(before)
        assert len(built.purchased_hardware) == 3
        assert sorted(h.spec.product_code for h in built.purchased_hardware) == ['70664','70664','9000894']
        removed = sum(p.solid.val().Volume() for p in before.parts)-sum(p.solid.val().Volume() for p in built.parts)
        assert removed == pytest.approx(6*pi*1.5**2*13)
        assert built.parts[2].solid is before.parts[2].solid
        assert feature.cut_list(before)['cut_length_mm'] == 561
        assert [h.spec.mounting_part_id for h in built.purchased_hardware[:2]] == ['left_side','right_side']
        for operation in built.spec.machining:
            assert [hole.y_mm for hole in operation.holes] == [-350,-359.5,-382]
        assert all(p.solid.val().isValid() for p in built.parts)
        assert any(r.requirement_id.endswith('_source_cad') for r in built.spec.requirements)
        with pytest.raises(ValueError, match='already exist'):
            feature.apply(built)

    @pytest.mark.parametrize('changes', [dict(depth_position_mm=5), dict(lower_screw_height_mm=490),
        dict(pilot_depth_mm=16), dict(pilot_diameter_mm=4), dict(lower_screw_height_mm=202)])
    def test_rejects_edge_overhang_and_bad_pilots(self, generated_values, changes):
        with pytest.raises(ValueError):
            self.feature(**changes).apply(self.cabinet(generated_values))

    def test_nested_component_cannot_occupy_rail_space(self, generated_values):
        values, _ = generated_values
        panels = importlib.import_module('assemblies.panel_assembly')
        before = self.cabinet(generated_values)
        part = replace(before.parts[2].spec, part_id='obstruction', local_size_mm=(100,100,16),
            local_to_parent=values.LocalToParentPlacement(values.Point3D(200,150,350),
                                                         values.IDENTITY_AXIS_BASIS))
        child = panels.PanelAssemblyBuilder(panels.PanelAssemblySpec('insert_01', 'insert',
                    (part,), requirements=())).build()
        child_spec = values.ChildAssemblySpec('insert_01','insert',values.IDENTITY_LOCAL_TO_PARENT)
        built_child = values.BuiltChildAssembly(child_spec,child)
        nested = replace(before, spec=replace(before.spec, child_assemblies=(child_spec,)),
                         child_assemblies=(built_child,))
        with pytest.raises(ValueError, match='insert_01/part:obstruction'):
            self.feature().apply(nested)
