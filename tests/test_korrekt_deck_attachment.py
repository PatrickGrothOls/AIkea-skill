"""Scope: Keep each Korrekt pair attached to its declared deck without changing its placement or purchase."""
from types import SimpleNamespace
import pytest
from assembly_composition_test_case import AssemblyCompositionTestCase
from assembly_taxonomy import BaseModuleTaxonomy, PartTaxonomy
from korrekt_base_feature import KorrektBaseFeature
from korrekt_base_layout import KorrektBaseLayout
from korrekt_mounting_profile import KorrektMountingProfile
from part_construction_error import PartConstructionError


class TestKorrektDeckAttachment(AssemblyCompositionTestCase):
    def test_each_pair_follows_its_declared_deck_with_unchanged_native_placement(self,generated_values):
        _,_root = generated_values
        spec = self._spec()
        layout = KorrektBaseLayout(95,15)
        component = KorrektBaseFeature(layout).feature(spec)
        assert len(component.stations) == 8
        assert [s.plate.mounting_part_id for s in component.stations] == ["deck_01"]*4+["deck_02"]*4
        profile = KorrektMountingProfile()
        for station in component.stations:
            assert station.plate.mounting_part_id == station.foot.mounting_part_id
            plate,foot = (p.local_to_parent.origin_in_parent for p in (station.plate,station.foot))
            assert plate.z_mm == 80 and foot.z_mm == 53.5
            assert plate.x_mm+profile.socket_axis_xy_mm[0] == pytest.approx(foot.x_mm)
            assert plate.y_mm+profile.socket_axis_xy_mm[1] == pytest.approx(foot.y_mm)
            assert station.plate.purchase.purchase_id == station.plate.hardware_id
            assert station.foot.purchase.purchase_id == station.foot.hardware_id

    def test_custom_station_spans_use_module_ownership_and_missing_deck_fails(self,generated_values):
        _,_root = generated_values
        spec = self._spec()
        feature = KorrektBaseFeature(KorrektBaseLayout(95,15),((0,300),(300,600),(600,900),(900,1200)))
        stations = feature.feature(spec).stations
        assert len(stations) == 16
        assert {s.plate.mounting_part_id for s in stations[:8]} == {"deck_01"}
        assert {s.plate.mounting_part_id for s in stations[8:]} == {"deck_02"}
        spec.parts = spec.parts[:1]
        with pytest.raises(PartConstructionError,match="no declared deck deck_02"):
            feature.feature(spec)

    def _spec(self):
        return SimpleNamespace(depth_mm=416,plinth_recess_mm=14,
            modules=(BaseModuleTaxonomy("base_module_01",0,600),BaseModuleTaxonomy("base_module_02",600,1200)),
            parts=(PartTaxonomy("deck_01","base_deck",()),PartTaxonomy("deck_02","base_deck",())))
