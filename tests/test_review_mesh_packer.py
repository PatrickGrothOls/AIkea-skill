"""Scope: Protect exact triangle attributes, material boundaries and embedded images during packing."""
import json
import struct
import numpy as np
import pytest
from review_mesh_packer import ReviewMeshPacker
from static_glb_buffers import StaticGlbBuffers


class TestReviewMeshPacker:
    def test_consolidates_shared_material_preserving_all_indexed_values(self, tmp_path):
        source = self._source(tmp_path, same_material=True)
        output = tmp_path/'packed.glb'
        report = ReviewMeshPacker().pack(source, output)
        before, after = StaticGlbBuffers(source), StaticGlbBuffers(output)
        assert report['source_draw_primitives'] == 2
        assert report['packed_draw_primitives'] == 1
        primitive = after.original['meshes'][0]['primitives'][0]
        for name in ('POSITION', 'NORMAL', 'TEXCOORD_0'):
            expected = np.concatenate([before.array(p['attributes'][name])
                for p in before.original['meshes'][0]['primitives']])
            assert np.array_equal(after.array(primitive['attributes'][name]), expected)
        assert after.array(primitive['indices']).reshape(-1).tolist() == [0,1,2,3,4,5]
        assert before.original['nodes'] == after.original['nodes']
        image = after.original['images'][0]
        view = after.original['bufferViews'][image['bufferView']]
        assert after.source_binary[view['byteOffset']:view['byteOffset']+view['byteLength']] == b'image-bytes'

    def test_material_boundaries_remain_separate_and_packing_is_repeatable(self, tmp_path):
        source = self._source(tmp_path, same_material=False)
        first, second = tmp_path/'first.glb', tmp_path/'second.glb'
        report = ReviewMeshPacker().pack(source, first)
        assert report['packed_draw_primitives'] == 2
        ReviewMeshPacker().pack(first, second)
        assert first.read_bytes() == second.read_bytes()
        assert [p['material'] for p in StaticGlbBuffers(second).original['meshes'][0]['primitives']] == [0,1]

    def test_rejects_animation_instead_of_discarding_it(self, tmp_path):
        with pytest.raises(ValueError, match='static, unskinned'):
            ReviewMeshPacker().pack(self._source(tmp_path, True, animated=True), tmp_path/'bad.glb')

    def _source(self, root, same_material, animated=False):
        binary = bytearray()
        views, accessors, primitives = [], [], []
        for offset in (0,10):
            attributes = {}
            values = {'POSITION': [[offset,0,0],[offset+1,0,0],[offset,1,0]],
                      'NORMAL': [[0,0,1]]*3, 'TEXCOORD_0': [[0,0],[1,0],[0,1]]}
            for name,array in values.items():
                raw = np.array(array, dtype='<f4').tobytes()
                views.append({'buffer':0,'byteOffset':len(binary),'byteLength':len(raw)})
                binary.extend(raw)
                attributes[name] = len(accessors)
                accessors.append({'bufferView':len(views)-1,'componentType':5126,'count':3,
                                  'type':'VEC2' if name == 'TEXCOORD_0' else 'VEC3'})
            primitives.append({'attributes':attributes,'material':0 if same_material or offset == 0 else 1})
        views.append({'buffer':0,'byteOffset':len(binary),'byteLength':11})
        binary.extend(b'image-bytes')
        document = {'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],
            'nodes':[{'mesh':0,'name':'panel','translation':[4,5,6],
                      'extras':{'aikea':{'kind':'panel','inspection_path':['unit','panel']}}}],
            'meshes':[{'primitives':primitives}], 'materials':[{'name':'a'},{'name':'b'}],
            'images':[{'bufferView':len(views)-1,'mimeType':'image/png'}],
            'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors}
        if animated:
            document['animations'] = [{'channels':[]}]
        encoded = json.dumps(document).encode()
        encoded += b' '*(-len(encoded)%4)
        binary.extend(b'\0'*(-len(binary)%4))
        chunks = struct.pack('<II',len(encoded),0x4E4F534A)+encoded
        chunks += struct.pack('<II',len(binary),0x004E4942)+binary
        path = root/'source.glb'
        path.write_bytes(struct.pack('<4sII',b'glTF',2,len(chunks)+12)+chunks)
        return path
