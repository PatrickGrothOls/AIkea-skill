"""Scope: Bake the prepared panels as one temporary mesh, then measure texture coverage."""

from pathlib import Path
import json
import bpy
import numpy as np
from baked_lighting_signal import BakedLightingSignal


class PanelBakePass:
    def __init__(self, root, threads=3, samples=16):
        self.root = Path(root)
        self.threads = threads
        self.lighting_samples = samples

    def white_material(self, image):
        material = bpy.data.materials.new('Constant white coverage test')
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1,1,1,1)
        material.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
        target = nodes.new('ShaderNodeTexImage')
        target.image = image
        nodes.active = target
        return material

    def samples(self, panels):
        samples = []
        for obj in panels:
            mesh = obj.data
            mesh.calc_loop_triangles()
            indices = np.empty(len(mesh.loop_triangles)*3,dtype=np.int32)
            mesh.loop_triangles.foreach_get('loops',indices)
            uv = np.empty(len(mesh.loops)*2,dtype=np.float32)
            mesh.uv_layers['BakedLightingUV'].data.foreach_get('uv',uv)
            triangles = uv.reshape((-1,2))[indices.reshape((-1,3))]
            samples.append((obj.name,triangles.mean(axis=1)))
        return samples

    def check(self, image, samples):
        size = image.size[0]
        pixels = np.empty(size*size*4,dtype=np.float32)
        image.pixels.foreach_get(pixels)
        pixels = pixels.reshape((size,size,4))
        rows = []
        for name, uv in samples:
            xy = np.clip(np.floor(uv*size).astype(int),0,size-1)
            values = pixels[xy[:,1],xy[:,0],:3].min(axis=1)
            rows.append({'part':name,'triangle_centroids':len(values),
                         'uncovered':int((values < 0.95).sum()),'minimum':float(values.min())})
        missing = sum(row['uncovered'] for row in rows)
        report = {'status':'PASS' if missing==0 else 'FAIL','uncovered_centroids':missing,
                  'panels':len(rows),'triangles':sum(row['triangle_centroids'] for row in rows),'parts':rows}
        (self.root/'all-panel-coverage.json').write_text(json.dumps(report,indent=2))
        print('COVERAGE',json.dumps({k:v for k,v in report.items() if k!='parts'}),flush=True)
        assert missing == 0, [row for row in rows if row['uncovered']]

    def run(self, white=False):
        bpy.ops.wm.open_mainfile(filepath=str(self.root/'bake-ready.blend'))
        panels = [obj for obj in bpy.context.scene.objects if obj.type=='MESH'
                  and obj.get('aikea',{}).get('kind')=='panel']
        samples = self.samples(panels)
        image = bpy.data.images['Assembled diffuse lighting']
        if white:
            material = self.white_material(image)
            for obj in panels:
                obj.data.materials.clear()
                obj.data.materials.append(material)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in panels:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = panels[0]
        # This joined mesh exists only for baking. Final export reloads the
        # unchanged prepared scene and attaches the resulting image.
        bpy.ops.object.join()
        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 1 if white else self.lighting_samples
        scene.cycles.use_denoising = False
        scene.render.threads_mode = 'FIXED'
        scene.render.threads = self.threads
        print('BAKE_START', 'white' if white else 'lighting',flush=True)
        options = {'type':'EMIT'} if white else {'type':'DIFFUSE','pass_filter':{'DIRECT','INDIRECT','COLOR'}}
        result = bpy.ops.object.bake(**options,use_clear=True,uv_layer='BakedLightingUV',
                                     margin=8,margin_type='EXTEND')
        assert result=={'FINISHED'},result
        image.filepath_raw = str(self.root/('all-panel-white.png' if white else 'assembled-lighting.png'))
        image.file_format = 'PNG'
        image.save()
        if white:
            self.check(image,samples)
        else:
            self.check_lighting(image, samples)
        print('BAKE_COMPLETE',flush=True)

    def check_lighting(self, image, samples):
        width, height = image.size
        pixels = np.empty(width*height*4, dtype=np.float32)
        image.pixels.foreach_get(pixels)
        pixels = pixels.reshape((height, width, 4))
        uv = np.concatenate([points for _, points in samples])
        xy = np.clip(np.floor(uv*[width, height]).astype(int), 0, [width-1, height-1])
        report = BakedLightingSignal().measure(pixels[xy[:, 1], xy[:, 0], :3])
        (self.root/'lighting-signal.json').write_text(json.dumps(report, indent=2))
        if report['status'] != 'PASS':
            raise ValueError('Empty or invalid panel lighting bake; inspect source material metalness and studio lights')
