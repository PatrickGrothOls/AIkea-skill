"""Scope: Read static GLB accessors and write compact embedded buffers without changing values."""
from copy import deepcopy
import json
from pathlib import Path
import struct
import numpy as np
from glb_artifact_snapshot import GlbArtifactSnapshot


class StaticGlbBuffers:
    TYPES = {5120: 'i1', 5121: 'u1', 5122: '<i2', 5123: '<u2', 5125: '<u4', 5126: '<f4'}
    WIDTHS = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}

    def __init__(self, path):
        self.source = GlbArtifactSnapshot.load(Path(path))
        raw = self.source.content
        length = struct.unpack_from('<I', raw, 12)[0]
        self.original = json.loads(raw[20:20+length])
        self.source_binary = raw[28+length:]
        self.document = deepcopy(self.original)
        self.binary = bytearray()
        self.document['accessors'] = []
        self.document['bufferViews'] = []
        unsupported = (self.original.get('animations'), self.original.get('skins'),
                       len(self.original['buffers']) != 1,
                       self.original['buffers'][0].get('uri'))
        if any(unsupported):
            raise ValueError('Packing requires a static, unskinned GLB with one embedded buffer')

    def array(self, index):
        accessor = self.original['accessors'][index]
        if 'sparse' in accessor:
            raise ValueError('Sparse accessors are not supported by static review packing')
        view = self.original['bufferViews'][accessor['bufferView']]
        dtype = np.dtype(self.TYPES[accessor['componentType']])
        width = self.WIDTHS[accessor['type']]
        offset = view.get('byteOffset', 0)+accessor.get('byteOffset', 0)
        return np.ndarray((accessor['count'], width), dtype=dtype, buffer=self.source_binary,
            offset=offset, strides=(view.get('byteStride', dtype.itemsize*width), dtype.itemsize)).copy()

    def view(self, content):
        self.binary.extend(b'\0'*(-len(self.binary)%4))
        offset = len(self.binary)
        self.binary.extend(content)
        views = self.document['bufferViews']
        views.append({'buffer': 0, 'byteOffset': offset, 'byteLength': len(content)})
        return len(views)-1

    def accessor(self, values, component_type, value_type, normalized=False):
        values = np.ascontiguousarray(values, dtype=self.TYPES[component_type])
        accessor = {'bufferView': self.view(values.tobytes()), 'componentType': component_type,
                    'count': len(values), 'type': value_type}
        if normalized:
            accessor['normalized'] = True
        if value_type != 'SCALAR':
            accessor.update(min=values.min(axis=0).tolist(), max=values.max(axis=0).tolist())
        self.document['accessors'].append(accessor)
        return len(self.document['accessors'])-1

    def write(self, path):
        for image in self.document.get('images', []):
            if 'bufferView' in image:
                view = self.original['bufferViews'][image['bufferView']]
                start = view.get('byteOffset', 0)
                image['bufferView'] = self.view(self.source_binary[start:start+view['byteLength']])
        self.document['buffers'] = [{'byteLength': len(self.binary)}]
        encoded = json.dumps(self.document, separators=(',', ':')).encode()
        encoded += b' '*(-len(encoded)%4)
        self.binary.extend(b'\0'*(-len(self.binary)%4))
        chunks = struct.pack('<II', len(encoded), 0x4E4F534A)+encoded
        chunks += struct.pack('<II', len(self.binary), 0x004E4942)+self.binary
        Path(path).write_bytes(struct.pack('<4sII', b'glTF', 2, len(chunks)+12)+chunks)
