"""Scope: Verify Korrekt ownership, removal, registration and exact-source rejection."""

from dataclasses import dataclass, replace
from hashlib import sha256
import importlib
import json

import cadquery as cq
import pytest

from assembly_composition_test_case import AssemblyCompositionTestCase
from construction_input_fingerprint import ConstructionInputFingerprinter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_korrekt_geometry_provider import HettichKorrektGeometryProvider
from korrekt_component_feature import KorrektComponentFeature, KorrektStation
from physical_item_counter import PhysicalItemCounter
from purchased_hardware_spec import HardwarePurchaseSpec
from part_construction_error import PartConstructionError
from project_hardware_geometry_resolver import ProjectHardwareGeometryError, ProjectHardwareGeometryResolver
from test_korrekt_mounting_geometry import TestKorrektMountingGeometry as DeckFixture


@dataclass
class SavedBase:
    assembly: object

    def build(self):
        return self.assembly


class TestKorrektComponentFeature(AssemblyCompositionTestCase):
    _deck = DeckFixture._deck

    def test_optional_feature_removal_restores_base_and_exact_manifest_scope(self, generated_values):
        values, root = generated_values
        base, feature = self._feature(values)
        composition = importlib.import_module('assemblies.assembly_feature')
        built = composition.FeatureComposedAssemblyBuilder(SavedBase(base), (feature,)).build()
        assert len(built.purchased_hardware) == 2 and len(built.cuts) == 1
        assert {item.spec.product_code for item in built.purchased_hardware} == {'61854', '70151'}
        inventory = PhysicalItemCounter().count(GeneratedAssemblyBuilderLoader().walk(root, built))
        assert {row['product_code']: row['quantity'] for row in inventory['purchased_summary']} == {'61854': 1, '70151': 1}
        assert not any(item['code'] == 'hardware.purchase_undefined' for item in inventory['unresolved'])
        assert len(built.spec.requirements) == 3
        assert built.spec.requirements[-1].disposition == 'unresolved'
        feature.register(root, built)
        manifest = json.loads((root/'assemblies/base_01/features.json').read_text())['features'][0]
        assert manifest['affected_manufactured_part_paths'] == ['deck']
        assert manifest['affected_purchased_hardware_paths'] == ['plate', 'foot']
        assert manifest['qualified_joint_ids'] == ['korrekt_mounting_plate_deck']
        removed = composition.FeatureComposedAssemblyBuilder(SavedBase(base), ()).build()
        assert removed is base and not removed.cuts and not removed.purchased_hardware
        assert removed.parts[0].solid.val().Volume() > built.parts[0].solid.val().Volume()
        assert not removed.spec.requirements

    def test_duplicate_ownership_and_wrong_article_fail(self, generated_values):
        values, _ = generated_values
        base, feature = self._feature(values)
        with pytest.raises(PartConstructionError, match='newly owned'):
            feature.apply(feature.apply(base))
        station = feature.stations[0]
        bad = replace(feature, stations=(replace(station, foot=replace(station.foot, product_code='61851')),))
        with pytest.raises(PartConstructionError, match='exact placed'):
            bad.apply(base)
        with pytest.raises(PartConstructionError, match='before registering'):
            feature.register(generated_values[1], base)

    def test_explicit_purchase_metadata_survives_and_invalid_grouping_fails(self, generated_values):
        values, _ = generated_values
        base, feature = self._feature(values)
        station = feature.stations[0]
        purchase = HardwarePurchaseSpec('plate', '61854', 'piece', 'plate', ('plate',), mounting_fasteners_included=False)
        custom = replace(feature, stations=(replace(station, plate=replace(station.plate, purchase=purchase)),))
        assert custom.apply(base).purchased_hardware[0].spec.purchase == purchase
        wrong = replace(custom.stations[0].plate, purchase=replace(purchase, purchase_id='foot'))
        with pytest.raises(PartConstructionError, match='one-piece purchase'):
            replace(feature, stations=(replace(station, plate=wrong),)).apply(base)

    def test_station_alignment_and_changed_layout_evidence(self, generated_values):
        values, root = generated_values
        base, feature = self._feature(values)
        station = feature.stations[0]
        misplaced = replace(station.foot.local_to_parent, origin_in_parent=values.Point3D(215, 100, 23))
        bad = replace(feature, stations=(replace(station, foot=replace(station.foot, local_to_parent=misplaced)),))
        with pytest.raises(PartConstructionError, match='socket axis'):
            bad.apply(base)
        first = feature.apply(base)
        moved = []
        for item in (station.plate, station.foot):
            frame = item.local_to_parent
            moved.append(replace(item, local_to_parent=replace(frame,
                origin_in_parent=replace(frame.origin_in_parent, x_mm=frame.origin_in_parent.x_mm+10))))
        second = replace(feature, stations=(KorrektStation(*moved),)).apply(base)
        loader, fingerprint = GeneratedAssemblyBuilderLoader(), ConstructionInputFingerprinter()
        assert fingerprint.build(root, loader.walk(root, first)) != fingerprint.build(root, loader.walk(root, second))

    def test_provider_rechecks_bytes_and_article_on_every_resolution(self, generated_values, monkeypatch):
        values, root = generated_values
        _, feature = self._feature(values)
        item = feature.stations[0].plate
        provider = HettichKorrektGeometryProvider()
        assert ProjectHardwareGeometryResolver().providers[-1].supports(item.hardware_asset_id)
        with pytest.raises(ProjectHardwareGeometryError, match='Missing or changed'):
            provider.resolve(root, item)
        source = root/'hardware/hettich/korrekt/61854/source/61854.stp'
        source.parent.mkdir(parents=True)
        cq.exporters.export(cq.Workplane('XY').box(5, 6, 7), str(source), exportType='STEP')
        monkeypatch.setattr(provider, 'SOURCES', {item.hardware_asset_id: ('61854', sha256(source.read_bytes()).hexdigest())})
        assert provider.resolve(root, item).val().Volume() == pytest.approx(210)
        with pytest.raises(ProjectHardwareGeometryError, match='disagree'):
            provider.resolve(root, replace(item, product_code='70151'))
        source.write_bytes(source.read_bytes()+b'changed')
        with pytest.raises(ProjectHardwareGeometryError, match='Missing or changed'):
            provider.resolve(root, item)

    def _feature(self, values):
        built = self._deck(values, 18, 0)
        plate = replace(built.spec.purchased_hardware[0], hardware_asset_id='hettich_korrekt_61854')
        origin = values.Point3D(216, 100, 23)
        foot = replace(plate, hardware_id='foot', product_code='70151', hardware_asset_id='hettich_korrekt_70151',
                       local_to_parent=replace(plate.local_to_parent, origin_in_parent=origin))
        panels = importlib.import_module('assemblies.panel_assembly')
        spec = panels.PanelAssemblySpec('base_01', 'platform', built.spec.parts, (), requirements=())
        return replace(built, spec=spec, purchased_hardware=()), KorrektComponentFeature(('deck',), (KorrektStation(plate, foot),), 10)
