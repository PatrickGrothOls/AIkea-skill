"""Scope: Give each connected bake UV island an explicit padded pixel rectangle."""

import json
import numpy as np
from bpy_extras.mesh_utils import mesh_linked_uv_islands
from texture_shelf_layout import TextureShelfLayout


class BakeUvCoverage:
    def __init__(self, panels, size=4096):
        self.panels = panels
        self.size = size

    def islands(self, obj):
        obj.data.uv_layers.active = obj.data.uv_layers['BakedLightingUV']
        for faces in mesh_linked_uv_islands(obj.data):
            yield np.array([loop for face in faces for loop in obj.data.polygons[face].loop_indices])

    def coordinates(self, obj):
        points = np.empty(len(obj.data.loops)*2,dtype=np.float32)
        obj.data.uv_layers['BakedLightingUV'].data.foreach_get('uv',points)
        return points.reshape((-1,2))

    def collect(self):
        charts = []
        for obj in self.panels:
            points = self.coordinates(obj)
            for indices in self.islands(obj):
                values = points[indices].astype(np.float64)
                centered = values-values.mean(axis=0)
                _,axes = np.linalg.eigh(centered.T @ centered)
                local = centered @ axes
                span = np.ptp(local,axis=0)
                assert np.all(span>0),(obj.name,span)
                local -= local.min(axis=0)
                # Tall rectangles pack efficiently in descending-height shelves.
                if span[0]>span[1]:
                    span,local = span[::-1],local[:,::-1]
                charts.append((obj,indices,local/span,span*self.size))
        return charts

    def apply(self, report_path):
        charts = self.collect()
        layout = TextureShelfLayout(self.size)
        result = None
        for scale in [1.0,0.9,0.8,0.7,0.6,0.5]:
            result = layout.pack([chart[3] for chart in charts],scale)
            print('PIXEL_PACK',scale,bool(result),flush=True)
            if result is not None:
                break
        assert result is not None,'No layout fits the bounded texture budget'
        placements,height = result
        buffers = {obj.name:self.coordinates(obj) for obj in self.panels}
        rows = []
        for index,(obj,indices,normalized,original_span) in enumerate(charts):
            x,y,width,chart_height = placements[index]
            buffers[obj.name][indices] = (normalized*(width,chart_height)+(x,y))/self.size
            rows.append({'part':obj.name,'original_width_px':float(original_span.min()),
                         'content_rect_px':[x,y,width,chart_height]})
        for obj in self.panels:
            obj.data.uv_layers['BakedLightingUV'].data.foreach_set('uv',buffers[obj.name].ravel())
        report = {'status':'PASS','atlas_size':self.size,'islands':len(charts),
                  'minimum_content_width_px':layout.minimum,'padding_each_side_px':layout.padding,
                  'broad_surface_scale':scale,'used_height_px':height,'charts':rows}
        report_path.write_text(json.dumps(report,indent=2))
        print('PIXEL_LAYOUT_READY',len(charts),scale,height,flush=True)
