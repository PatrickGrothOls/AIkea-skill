"""Scope: Guard physical adjustable shelves, underside fixed choices and Korrekt-only base defaults."""
from dataclasses import replace
from math import pi
import importlib
import pytest
from assembly_composition_test_case import AssemblyCompositionTestCase
from adjustable_shelf_support_feature import AdjustableShelfSupportFeature
from base_taxonomy_builder import BaseTaxonomyBuilder
from base_part_placement_resolver import BasePartPlacementResolver
from configured_unit_builder import ConfiguredUnitBuilder
from korrekt_base_feature import KorrektBaseFeature
from korrekt_base_layout import KorrektBaseLayout
from korrekt_floor_access_feature import KorrektFloorAccessFeature
from part_construction_error import PartConstructionError
from storage_shelf_policy import FixedShelfChoice, StorageShelfPolicy


class TestCabinetConstructionDefaults(AssemblyCompositionTestCase):
    def test_floor_base_has_decks_kickboards_and_no_brace_substitution(self):
        base = BaseTaxonomyBuilder().build(((0,2475),),416,95,15,"recessed",14)
        placed = BasePartPlacementResolver().resolve(base)
        assert {p.role for p in placed.parts} == {"base_deck","base_kickboard"}
        assert placed.parts[0].local_to_parent.origin_in_parent_mm[2] == 80
        assert all(j.joint_type == "unresolved" for j in placed.joints)
        with pytest.raises(PartConstructionError,match="no brace-base fallback"):
            BaseTaxonomyBuilder().build(((0,600),),416,60,16,"recessed",14)

    def test_95mm_with_16mm_deck_rejects_unadjusted_source_pose(self):
        layout = KorrektBaseLayout(95,16)
        layout.check_adjustment_range()  # Physical product range and available CAD pose are distinct.
        with pytest.raises(PartConstructionError,match="intrudes into the deck"):
            KorrektBaseFeature(layout).feature(None)

    def test_whole_plate_margins_and_front_foot_clear_kickboard(self):
        layout = KorrektBaseLayout(95,15)
        axes = layout.station_axes(0,618.75,416,29)
        assert len(axes) == 4
        assert min(x for x,y in axes)-39.50498 >= 15
        assert 618.75-max(x for x,y in axes)-55.4975 >= 15-1e-6
        assert min(y for x,y in axes)-40.15 >= 31

    def test_shelf_has_four_purchases_real_support_geometry_and_blind_holes(self,generated_values):
        values, _ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        spec = self._shelf_spec(values,panel)
        before = panel.PanelAssemblyBuilder(spec).build()
        result = AdjustableShelfSupportFeature(("shelf",)).apply(before)
        assert len(result.purchased_hardware) == 4
        assert {p.spec.product_code for p in result.purchased_hardware} == {"46642"}
        assert all(p.has_geometry for p in result.purchased_hardware)
        assert len(result.cuts) == 2
        assert len({p.spec.purchase.purchase_id for p in result.purchased_hardware}) == 4
        removed = sum(p.solid.val().Volume() for p in before.parts)-sum(p.solid.val().Volume() for p in result.parts)
        assert removed == pytest.approx(4*pi*2.5**2*13)
        assert all(p.solid.val().isValid() for p in result.parts)
        assert result.spec.part("shelf").local_size_mm[0] == 567
        with pytest.raises(PartConstructionError,match="distinct owned"):
            AdjustableShelfSupportFeature(("shelf",)).apply(result)

    def test_configured_cabinet_cannot_emit_floating_shelf(self,generated_values):
        values, _ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        result = ConfiguredUnitBuilder(self._shelf_spec(values,panel),"cabinet").build()
        assert len(result.purchased_hardware) == 4 and len(result.cuts) == 2

    def test_fixed_shelf_requires_deliberate_reason_and_underside(self,generated_values):
        values, _ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        spec = self._shelf_spec(values,panel)
        joint = values.CabineoJointSpec("fixed","shelf","left_side",">Z","<X","single_center")
        spec = replace(spec,joints=(joint,))
        policy = StorageShelfPolicy()
        with pytest.raises(PartConstructionError,match="deliberate"):
            policy.adjustable_ids(spec)
        choice = (FixedShelfChoice("shelf","Deliberate structural divider"),)
        with pytest.raises(PartConstructionError,match="hidden underside"):
            policy.adjustable_ids(spec,choice)
        assert policy.adjustable_ids(replace(spec,joints=(replace(joint,source_face="<Z"),)),choice) == ()
        floor = replace(spec,parts=tuple(replace(p,role="floor_panel") if p.part_id == "shelf" else p for p in spec.parts))
        assert policy.adjustable_ids(floor) == ()

    def test_floor_access_is_separate_aligned_through_machining(self,generated_values):
        v,_ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        floor = v.PartSpec("floor","floor_panel",(),v.LocalToParentPlacement(v.Point3D(16,0,95),v.IDENTITY_AXIS_BASIS),
            local_size_mm=(568,400,16),inside_face=">Z")
        original = panel.PanelAssemblyBuilder(panel.PanelAssemblySpec("cab","storage",(floor,),requirements=())).build()
        result = KorrektFloorAccessFeature("floor",((100,100),(500,300))).apply(original)
        assert original.parts[0].solid.val().Volume()-result.parts[0].solid.val().Volume() == pytest.approx(2*pi*4**2*16)
        assert len(result.cuts) == 1
        assert result.spec.machining[0].holes[0].x_mm == 84
        assert result.spec.machining[0].holes[0].y_mm == -100

    def _shelf_spec(self,v,panel):
        # A local fixture converter keeps its only caller and coordinate contract together.
        def frame(origin,x,y,z):
            return v.LocalToParentPlacement(v.Point3D(*origin),v.AxisBasis(
                v.AxisDirection(*x),v.AxisDirection(*y),v.AxisDirection(*z)))
        parts = (
            v.PartSpec("left_side","side_panel",(),frame((0,0,0),(0,1,0),(0,0,1),(1,0,0)),local_size_mm=(400,500,16),inside_face=">Z"),
            v.PartSpec("right_side","side_panel",(),frame((600,400,0),(0,-1,0),(0,0,1),(-1,0,0)),local_size_mm=(400,500,16),inside_face=">Z"),
            v.PartSpec("shelf","shelf_panel",(),frame((16.5,0,202.5),(1,0,0),(0,1,0),(0,0,1)),local_size_mm=(567,400,16),inside_face=">Z"),
        )
        return panel.PanelAssemblySpec("cabinet","storage",parts,requirements=())
