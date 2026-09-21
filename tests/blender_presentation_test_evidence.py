"""Scope: Supply synthetic bake reports for viewer contract tests, never render evidence."""

from hashlib import sha256
import json


class BlenderPresentationTestEvidence:
    def write(self, model, inspection):
        source_hash = sha256(inspection.read_bytes()).hexdigest()
        output_hash = sha256(model.read_bytes()).hexdigest()
        geometry = dict(status="PASS", source_sha256=source_hash, physical_parts=1,
                        no_mesh_changes=True, source_uvs_unchanged=True,
                        no_modifiers=True, placements_unchanged_after_import=True)
        reports = {
            "prepared-geometry.json": geometry,
            "all-panel-coverage.json": dict(status="PASS", uncovered_centroids=0, triangles=12),
            "shaded-geometry.json": geometry,
            "export-geometry.json": dict(status="PASS", physical_parts=1,
                source_sha256=source_hash, exported_sha256=output_hash,
                triangle_connectivity="bijective oriented world-space triangles",
                maximum_vertex_error_mm=0.0, tolerance_mm=0.002),
        }
        reports["presentation.json"] = dict(status="PASS", presentation_state="assembled_only",
            source_sha256=source_hash, assembled_sha256=output_hash,
            uncovered_triangle_centroids=0, physical_parts=1, maximum_vertex_error_mm=0.0,
            atlas_size=4096, samples=16, blender_version="synthetic test fixture",
            checks=list(reports))
        for name, report in reports.items():
            (model.parent / name).write_text(json.dumps(report))
