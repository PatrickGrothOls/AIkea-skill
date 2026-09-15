"""Scope: Consolidate static surfaces within each part/material and prove indexed attributes unchanged."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from static_glb_buffers import StaticGlbBuffers


class ReviewMeshPacker:
    def pack(self, source, output):
        glb = StaticGlbBuffers(source)
        expected = []
        source_count = sum(len(m['primitives']) for m in glb.original['meshes'])
        for mesh in glb.document['meshes']:
            groups = defaultdict(list)
            for primitive in mesh['primitives']:
                if set(primitive)-{'attributes', 'indices', 'material', 'mode'} or primitive.get('mode', 4) != 4:
                    raise ValueError('Packing supports plain static triangle surfaces only')
                signature = [(name, glb.original['accessors'][index]['componentType'],
                              glb.original['accessors'][index]['type'],
                              glb.original['accessors'][index].get('normalized', False))
                             for name,index in sorted(primitive['attributes'].items())]
                groups[(primitive.get('material'), tuple(signature))].append(primitive)
            mesh['primitives'] = []
            for (material, signature), primitives in groups.items():
                merged, proof = self._merge(glb, primitives, material, signature)
                mesh['primitives'].append(merged)
                expected.append(proof)
        glb.write(output)
        checked = StaticGlbBuffers(output)
        actual = [self._proof(checked, p) for m in checked.original['meshes'] for p in m['primitives']]
        if actual != expected or checked.original['nodes'] != glb.original['nodes']:
            raise ValueError('Packed geometry attributes or part transforms changed')
        report = {'status': 'PASS', 'source': str(source), 'output': str(output),
            'source_sha256': glb.source.sha256, 'output_sha256': checked.source.sha256,
            'parts': len(glb.original['meshes']), 'source_draw_primitives': source_count,
            'packed_draw_primitives': len(actual), 'indexed_attributes_bitwise_equal': True,
            'nodes_transforms_and_identities_unchanged': True, 'materials_unchanged':
                checked.original.get('materials') == glb.original.get('materials'),
            'geometry_simplified': False, 'manufacturing_authority': False}
        Path(output).with_suffix('.packing-check.json').write_text(json.dumps(report, indent=2)+'\n')
        return report

    def _merge(self, glb, primitives, material, signature):
        arrays = defaultdict(list)
        indices, proofs, count = [], [], 0
        for primitive in primitives:
            attributes = {name: glb.array(index) for name,index in primitive['attributes'].items()}
            length = len(attributes['POSITION'])
            index = (glb.array(primitive['indices']).reshape(-1).astype(np.uint32)
                     if 'indices' in primitive else np.arange(length, dtype=np.uint32))
            indices.append(index+count)
            proofs.append(self._indexed(attributes, index))
            for name, values in attributes.items():
                arrays[name].append(values)
            count += length
        merged = {'attributes': {}, 'mode': 4}
        if material is not None:
            merged['material'] = material
        for name,component,value_type,normalized in signature:
            merged['attributes'][name] = glb.accessor(np.concatenate(arrays[name]), component, value_type, normalized)
        merged['indices'] = glb.accessor(np.concatenate(indices).reshape(-1, 1), 5125, 'SCALAR')
        # Hash the indexed attributes in material-local triangle order, not vertex buffer layout.
        proof = {name: sha256(b''.join(item[name] for item in proofs)).hexdigest() for name in arrays}
        return merged, proof

    def _indexed(self, attributes, indices):
        return {name: np.ascontiguousarray(values[indices]).tobytes() for name,values in attributes.items()}

    def _proof(self, glb, primitive):
        attrs = {name: glb.array(index) for name,index in primitive['attributes'].items()}
        indices = glb.array(primitive['indices']).reshape(-1)
        return {name: sha256(data).hexdigest() for name,data in self._indexed(attrs, indices).items()}
