"""Scope: Verify saved custom lighting owns its groove, purchase and removable requirements."""

from dataclasses import replace
import json

import cadquery as cq
import pytest

from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from cabinet_feature_manifest import CabinetFeatureManifest
from cabinet_lighting_generator import CabinetLightingGenerator
from construction_input_fingerprint import ConstructionInputFingerprinter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from lighting_run import LightingRun
from lighting_test_project import LightingTestProject
from physical_item_counter import PhysicalItemCounter
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class TestLightingSharedConstruction:
    def test_custom_frame_common_cuts_purchase_and_removal(self, tmp_path):
        root = LightingTestProject().create(tmp_path)
        loader = GeneratedAssemblyBuilderLoader()
        base = loader.load_assembly(root, 'custom_01')
        self._generate(root)
        lit = loader.load_assembly(root, 'custom_01')
        original, actual = base.parts[0].solid.val(), lit.parts[0].solid.val()
        expected = original.cut(cq.Solid.makeBox(600, 4, 8, cq.Vector(50, 198, 8)))
        assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert [cut.joint_id for cut in lit.cuts] == ['service', 'shelf_light_01_groove']
        assert len(lit.spec.requirements) == 3 and lit.spec.requirements[-1].disposition == 'unresolved'
        hardware = lit.purchased_hardware[0].spec
        assert hardware.local_to_parent.origin_in_parent == replace(hardware.local_to_parent.origin_in_parent,
            x_mm=116, y_mm=250, z_mm=250)
        assert hardware.local_to_parent.axis_basis.local_z_in_parent.x == 1
        inventory = PhysicalItemCounter().count(loader.walk(root, lit))
        assert len(inventory['purchased_summary']) == 1 and inventory['purchased_summary'][0]['quantity'] == 1
        assert '600 mm / 3200 K' in inventory['purchased_summary'][0]['product_code']
        CabinetFeatureManifest().unregister(root, 'custom_01', 'lighting.feature')
        for module in ('complete_builder', 'with_lighting_builder'):
            removed = loader.load_assembly(root, 'custom_01', module)
            assert [cut.joint_id for cut in removed.cuts] == ['service']
            assert removed.parts[0].solid.val().Volume() == pytest.approx(original.Volume())
            assert not removed.purchased_hardware and not removed.spec.requirements
        assert (root/'assemblies/custom_01/parts/host/lighting.yaml').is_file()
        manifest = json.loads((root/'assemblies/custom_01/features.json').read_text())
        assert [item['module'] for item in manifest['features']] == ['service.feature']

    def test_regeneration_rebuilds_changed_run_without_reusing_old_groove(self, tmp_path):
        root = LightingTestProject().create(tmp_path)
        self._generate(root)
        loader = GeneratedAssemblyBuilderLoader()
        first = loader.load_assembly(root, 'custom_01')
        fingerprint = ConstructionInputFingerprinter().build(root, loader.walk(root, first))
        self._generate(root, end=(550, 200))
        second = loader.load_assembly(root, 'custom_01')
        assert second.parts[0].solid.val().Volume()-first.parts[0].solid.val().Volume() == pytest.approx(100*4*8)
        assert '500 mm' in second.purchased_hardware[0].spec.product_code
        assert fingerprint != ConstructionInputFingerprinter().build(root, loader.walk(root, second))
        assert len(second.cuts) == 2 and len(second.purchased_hardware) == 1

    def test_preserves_authored_plan_and_refuses_private_base_wrapper(self, tmp_path):
        root = LightingTestProject().create(tmp_path)
        self._generate(root)
        path = root/'assemblies/custom_01/parts/host/lighting.yaml'
        content = path.read_text()+'# owner adjustment\n'
        path.write_text(content)
        with pytest.raises(AssemblyTaxonomyConflict):
            self._generate(root, end=(550, 200))
        assert path.read_text() == content
        with pytest.raises(ValueError, match='Move existing features'):
            self._generate(root, base_builder_module='private_base')

    @pytest.mark.parametrize('run_id,end,message', (('bad-name', (650, 200), 'stable'),
        ('valid', (float('nan'), 200), 'finite'), ('valid', (float('inf'), 200), 'finite')))
    def test_invalid_run_inputs_fail_before_generation(self, run_id, end, message):
        with pytest.raises(ValueError, match=message):
            LightingRun(run_id, (50, 200), end, 3200, DOMUS_APEX_84_HI)

    def _generate(self, root, end=(650, 200), base_builder_module='complete_builder'):
        run = LightingRun('shelf_light_01', (50, 200), end, 3200, DOMUS_APEX_84_HI)
        return CabinetLightingGenerator().generate(root, 'custom_01', 'host', run,
                                                    base_builder_module=base_builder_module)
