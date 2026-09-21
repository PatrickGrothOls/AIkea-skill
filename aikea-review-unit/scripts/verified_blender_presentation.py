"""Scope: Require current Blender bake evidence before exposing a furniture viewer."""

import json
from math import isfinite


class VerifiedBlenderPresentation:
    CHECKS = ("prepared-geometry.json", "all-panel-coverage.json",
              "shaded-geometry.json", "export-geometry.json")
    REMEDY = ("Run bake_furniture_presentation.py at the approved quality, then serve "
              "assembled.glb with --inspection-model pointing to its source GLB.")

    def require(self, assembled, inspection):
        if inspection is None:
            raise ValueError(f"A verified Blender presentation and inspection model are required. {self.REMEDY}")
        directory = assembled.path.parent
        report = self._read(directory / "presentation.json")
        required = {
            "status": "PASS", "presentation_state": "assembled_only",
            "assembled_sha256": assembled.sha256, "source_sha256": inspection.sha256,
            "uncovered_triangle_centroids": 0,
        }
        if any(report.get(key) != value for key, value in required.items()):
            raise ValueError(f"Blender presentation is failed, incomplete or stale. {self.REMEDY}")
        if (not report.get("blender_version") or report.get("checks") != list(self.CHECKS)
                or not self._number(report.get("atlas_size"), 4096, 4096)
                or not self._number(report.get("samples"), 16, 64)
                or not self._number(report.get("physical_parts"), 1, float("inf"))
                or not self._number(report.get("maximum_vertex_error_mm"), 0, 0.002)):
            raise ValueError(f"Blender presentation quality or geometry evidence is incomplete. {self.REMEDY}")
        checks = {name: self._read(directory / name) for name in self.CHECKS}
        if any(check.get("status") != "PASS" for check in checks.values()):
            raise ValueError("A required Blender coverage or geometry check did not pass.")
        flags = ("no_mesh_changes", "source_uvs_unchanged", "no_modifiers",
                 "placements_unchanged_after_import")
        for name in ("prepared-geometry.json", "shaded-geometry.json"):
            check = checks[name]
            if (check.get("source_sha256") != inspection.sha256
                    or check.get("physical_parts") != report["physical_parts"]
                    or any(check.get(flag) is not True for flag in flags)):
                raise ValueError("Blender preparation changed the source geometry or materials' UVs.")
        coverage = checks["all-panel-coverage.json"]
        if (coverage.get("uncovered_centroids") != 0
                or not self._number(coverage.get("triangles"), 1, float("inf"))):
            raise ValueError("Blender coverage check contains missing panel coverage.")
        geometry = checks["export-geometry.json"]
        expected = {"source_sha256": inspection.sha256, "exported_sha256": assembled.sha256,
                    "physical_parts": report["physical_parts"],
                    "triangle_connectivity": "bijective oriented world-space triangles"}
        if (any(geometry.get(key) != value for key, value in expected.items())
                or not self._number(geometry.get("tolerance_mm"), 0, 0.002)
                or not self._number(geometry.get("maximum_vertex_error_mm"), 0, 0.002)
                or geometry["maximum_vertex_error_mm"] != report["maximum_vertex_error_mm"]):
            raise ValueError("Blender export proof does not match the served models or geometry tolerance.")

    def _read(self, path):
        try:
            report = json.loads(path.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError(f"Missing or unreadable Blender evidence: {path.name}. {self.REMEDY}") from error
        if not isinstance(report, dict):
            raise ValueError(f"Blender evidence must be an object: {path.name}")
        return report

    def _number(self, value, minimum, maximum):
        return type(value) in (int, float) and isfinite(value) and minimum <= value <= maximum
