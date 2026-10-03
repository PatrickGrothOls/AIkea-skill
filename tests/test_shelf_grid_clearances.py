"""Scope: Keep support axes on the cabinet grid when shelves have fitting gaps."""
from dataclasses import replace
import importlib
import pytest
from test_cabinet_construction_defaults import TestCabinetConstructionDefaults as CabinetFixtures
from assembly_composition_test_case import AssemblyCompositionTestCase
from adjustable_shelf_support_feature import AdjustableShelfSupportFeature
from part_construction_error import PartConstructionError


class TestShelfGridClearances(AssemblyCompositionTestCase):
    def test_shelf_setback_does_not_shift_side_owned_pin_columns(self, generated_values):
        values,_ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        spec = CabinetFixtures()._shelf_spec(values,panel)
        shelf = spec.part("shelf")
        frame = shelf.local_to_parent
        shelf = replace(shelf, local_size_mm=(567,396,16), local_to_parent=replace(frame,
            origin_in_parent=replace(frame.origin_in_parent,y_mm=2)))
        spec = replace(spec,parts=tuple(shelf if p.part_id=="shelf" else p for p in spec.parts))
        result = AdjustableShelfSupportFeature(("shelf",)).apply(panel.PanelAssemblyBuilder(spec).build())
        assert sorted(p.spec.local_to_parent.origin_in_parent.y_mm
                      for p in result.purchased_hardware) == pytest.approx([37,37,363,363])

    def test_short_shelf_cannot_silently_add_its_own_support_columns(self, generated_values):
        values,_ = generated_values
        panel = importlib.import_module("assemblies.panel_assembly")
        spec = CabinetFixtures()._shelf_spec(values,panel)
        spec = replace(spec,parts=tuple(replace(p,local_size_mm=(567,300,16))
            if p.part_id=="shelf" else p for p in spec.parts))
        with pytest.raises(PartConstructionError,match="support columns"):
            AdjustableShelfSupportFeature(("shelf",)).apply(panel.PanelAssemblyBuilder(spec).build())
