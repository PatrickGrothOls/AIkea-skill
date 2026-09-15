"""Scope: Add representative stock materials and local UVs without touching CAD buffers."""
from pathlib import Path
import hashlib
import json
import struct
import numpy as np


class MaterialPreparation:
    def run(self,source,output):
        raw=source.read_bytes();length=struct.unpack_from('<I',raw,12)[0]
        document=json.loads(raw[20:20+length]);binary=bytearray(raw[28+length:])
        original_binary=bytes(binary)
        materials=[];lookup={}
        for node in document['nodes']:
            if 'mesh' not in node:
                continue
            identity=node.get('extras',{}).get('aikea',{})
            name=node.get('name','')
            material=self._material(name,identity.get('kind'))
            key=material['name']
            if key not in lookup:
                lookup[key]=len(materials);materials.append(material)
            for primitive in document['meshes'][node['mesh']]['primitives']:
                primitive['material']=lookup[key]
                if identity.get('kind')=='panel':
                    positions=self._accessor(document,binary,primitive['attributes']['POSITION'])
                    normals=self._accessor(document,binary,primitive['attributes']['NORMAL'])
                    major=int(np.argmax(np.mean(np.abs(normals),axis=0)))
                    axes=[axis for axis in range(3) if axis!=major]
                    uv=np.ascontiguousarray(positions[:,axes]/1000,dtype='<f4')
                    while len(binary)%4:binary.append(0)
                    offset=len(binary);data=uv.tobytes();binary.extend(data)
                    view=len(document['bufferViews']);document['bufferViews'].append(
                        {'buffer':0,'byteOffset':offset,'byteLength':len(data),'target':34962})
                    accessor=len(document['accessors']);document['accessors'].append(
                        {'bufferView':view,'componentType':5126,'count':len(uv),'type':'VEC2'})
                    primitive['attributes']['TEXCOORD_0']=accessor
        document['materials']=materials
        document['buffers'][0]['byteLength']=len(binary)
        encoded=json.dumps(document,separators=(',',':')).encode();encoded+=b' '*(-len(encoded)%4)
        binary.extend(b'\0'*(-len(binary)%4))
        payload=struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(binary),0x004e4942)+binary
        output.write_bytes(struct.pack('<4sII',b'glTF',2,len(payload)+12)+payload)
        if bytes(binary[:len(original_binary)])!=original_binary:
            raise ValueError('Original CAD binary changed during material preparation')
        output.with_suffix('.materials.json').write_text(json.dumps({
            'status':'PASS','source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'original_position_normal_index_buffers_unchanged':True,'node_transforms_and_identities_unchanged':True,
            'materials':'Representative white painted MDF, birch plywood, HDF and metal. Supplier finishes remain unselected.',
            'lighting':'Shared lighting feature supplies real emitter faces; power and wiring qualification remain open.',
            'uv_units':'Part-local coordinates in metres; existing CAD topology and geometry are preserved.'},indent=2))

    def _accessor(self,document,binary,index):
        accessor=document['accessors'][index];view=document['bufferViews'][accessor['bufferView']]
        offset=view.get('byteOffset',0)+accessor.get('byteOffset',0)
        width={'VEC2':2,'VEC3':3}[accessor['type']]
        return np.ndarray((accessor['count'],width),dtype='<f4',buffer=binary,offset=offset,
            strides=(view.get('byteStride',4*width),4)).copy()

    def _material(self,name,kind):
        label='white-painted-mdf';color=[.82,.81,.77,1];metal=0;rough=.7;emission=None
        if kind=='hardware':
            label='nickel-hardware';color=[.5,.52,.54,1];metal=.8;rough=.3
            if any(token in name for token in ('foot_','plate_','connector')):
                label='black-polymer';color=[.035,.04,.045,1];metal=0;rough=.65
            if name.endswith('_insert'):
                label='brass-insert';color=[.64,.45,.15,1];metal=.85
            if 'light_source__' in name:
                label='neutral-white-led';color=[1,.98,.94,1];metal=0;emission=[1,.98,.94]
        elif 'captured_bottom' in name:
            label='hdf-bottom';color=[.5,.37,.23,1]
        elif any(token in name for token in ('support','deck')):
            label='birch-plywood';color=[.73,.63,.45,1]
        material={'name':label,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':metal,'roughnessFactor':rough}}
        if emission is not None:
            material['emissiveFactor']=emission
        return material


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    MaterialPreparation().run(root/'reviews/furniture_01-lit.glb',root/'reviews/materials.glb')
