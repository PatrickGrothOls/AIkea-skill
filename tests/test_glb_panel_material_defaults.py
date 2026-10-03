"""Scope: Preserve explicit materials and shared hardware while fixing CAD panel defaults."""

from copy import deepcopy

from glb_panel_material_defaults import GlbPanelMaterialDefaults


class TestGlbPanelMaterialDefaults:
    def fixture(self, metallic=None):
        pbr = {'baseColorFactor': [0.6, 0.5, 0.3, 1]}
        if metallic is not None:
            pbr['metallicFactor'] = metallic
        return dict(nodes=[
            dict(mesh=0, extras=dict(aikea=dict(kind='panel'))),
            dict(mesh=0, extras=dict(aikea=dict(kind='hardware')))],
            meshes=[dict(primitives=[dict(material=0, attributes=dict(POSITION=0))])],
            materials=[dict(pbrMetallicRoughness=pbr)])

    def test_shared_hardware_retains_original_material_and_geometry(self):
        document = self.fixture()
        original = deepcopy(document)
        GlbPanelMaterialDefaults().apply(document)
        panel = document['meshes'][document['nodes'][0]['mesh']]['primitives'][0]
        assert document['materials'][panel['material']]['pbrMetallicRoughness']['metallicFactor'] == 0
        assert panel['attributes'] == original['meshes'][0]['primitives'][0]['attributes']
        assert document['meshes'][0] == original['meshes'][0]
        assert document['materials'][0] == original['materials'][0]
        once = deepcopy(document)
        GlbPanelMaterialDefaults().apply(document)
        assert document == once

    def test_declared_metalness_is_not_overwritten(self):
        document = self.fixture(metallic=0.7)
        original = deepcopy(document)
        GlbPanelMaterialDefaults().apply(document)
        assert document == original
