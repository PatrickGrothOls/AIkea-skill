"""Scope: Show one explicitly illustrative 90-degree door endpoint without inventing hinge articulation."""
from pathlib import Path
import hashlib,json,struct,sys
import numpy as np
sys.path.insert(0,str(Path.cwd()/'aikea-review-unit/scripts'))
from glb_world_geometry import GlbWorldGeometry


class FirstDoorIllustration:
    def run(self):
        root=Path('local-evidence/fresh-project/reviews')
        source=root/'grass-v3-materials-packed.glb';output=root/'grass-v3-first-door-open-illustrative.glb'
        raw=source.read_bytes();size=struct.unpack_from('<I',raw,12)[0]
        doc=json.loads(raw[20:20+size]);binary_chunk=raw[20+size:]
        original=json.loads(json.dumps(doc));moved=[];omitted=[]
        # Native Z-up coordinates. The source supports lateral flush at90deg.
        # Fore/aft hinge-edgeY=0 is a DISPLAY ASSUMPTION, not a vendor datum.
        pose=np.array(((0,1,0,16),(-1,0,0,1),(0,0,1,0),(0,0,0,1)),dtype=float)
        for i,node in enumerate(doc['nodes']):
            path=node.get('extras',{}).get('aikea',{}).get('inspection_path',[])
            if path[:2]!=['cabinet_01','door_panel']:
                continue
            assert i in doc['nodes'][0]['children'],'Expected direct native-frame review nodes'
            if len(path)==3 and path[-1].endswith('_grass_hinge'):
                del node['mesh'];omitted.append('/'.join(path));continue
            matrix=pose@GlbWorldGeometry.matrix(node)
            for name in ('rotation','translation','scale'):node.pop(name,None)
            node['matrix']=matrix.T.reshape(-1).tolist();moved.append('/'.join(path))
        assert len(omitted)==5 and len(moved)==11
        changed=set(moved+omitted)
        for before,after in zip(original['nodes'],doc['nodes']):
            path='/'.join(before.get('extras',{}).get('aikea',{}).get('inspection_path',[]))
            if path not in changed:assert before==after
        note='ILLUSTRATIVE 90-degree cabinet1 door endpoint; fore/aft position unverified; five fused hinge bodies omitted; no motion or fit proof.'
        doc.setdefault('extras',{})['aikea_pose_note']=note
        encoded=json.dumps(doc,separators=(',',':')).encode();encoded+=b' '*(-len(encoded)%4)
        payload=struct.pack('<II',len(encoded),0x4e4f534a)+encoded+binary_chunk
        output.write_bytes(struct.pack('<4sII',b'glTF',2,len(payload)+12)+payload)
        report=dict(status='ILLUSTRATIVE_ONLY',source=str(source),source_sha256=hashlib.sha256(raw).hexdigest(),
            output=str(output),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
            authority='GRASS2026.27 page518: K3+3mm plate, lateral zero protrusion at90 degrees only.',
            source_url='https://mediacenter.grass.eu/Katalog/EN/518/',
            missing_datum='Door hinge-side edge fore/aft displacement relative to carcass front at90degrees.',
            display_assumption='Native door rear face aligned X16; hinge-side edge placed atY0. Z unchanged.',
            native_endpoint_matrix=pose.tolist(),moved=moved,omitted=omitted,
            other_nodes_unchanged=True,all_mesh_and_material_buffers_unchanged=True,
            fixed_plates_and_their_screws_unchanged=True,doors_2_to_4_closed_unchanged=True,
            articulation_verified=False,motion_verified=False,manufacturing_authority=False,note=note)
        output.with_suffix('.pose.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))


if __name__=='__main__':
    FirstDoorIllustration().run()
