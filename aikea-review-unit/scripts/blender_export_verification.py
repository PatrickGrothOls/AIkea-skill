"""Scope: Require matching identified world-space triangles in source and Blender-exported GLBs."""
import json
from glb_world_geometry import GlbWorldGeometry
from oriented_triangle_comparison import OrientedTriangleComparison


class ExportGeometryVerification:
    def run(self, source_path, model_path, report_path, unit_scale):
        source = GlbWorldGeometry(source_path, unit_scale)
        exported = GlbWorldGeometry(model_path, unit_scale)
        if set(source.members) != set(exported.members):
            raise ValueError('Exported physical part identities changed')
        comparison = OrientedTriangleComparison()
        rows = []
        for key in source.members:
            rows.append(comparison.compare(key, source.part(key), exported.part(key)))
            print('GEOMETRY_VERIFIED', key, flush=True)
        report = {'status':'PASS', 'physical_parts':len(rows),
            'triangle_connectivity':'bijective oriented world-space triangles',
            'maximum_vertex_error_mm':max(row['maximum_vertex_error_mm'] for row in rows),
            'tolerance_mm':comparison.tolerance*1000,
            'source_sha256':source.glb.source.sha256, 'exported_sha256':exported.glb.source.sha256,
            'materials':[m.get('name','') for m in exported.glb.original.get('materials',[])],
            'parts':rows}
        report_path.write_text(json.dumps(report,indent=2))
        print(json.dumps({k:v for k,v in report.items() if k!='parts'},indent=2), flush=True)
