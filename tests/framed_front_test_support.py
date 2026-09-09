"""Scope: Load optional front helpers inside isolated synthetic project contracts."""

import importlib
import pytest
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from init_framed_door_design import FramedDoorDesignProject


class FramedFrontTestSupport:
    @pytest.fixture
    def contracts(self, tmp_path):
        FramedDoorDesignProject().initialize(tmp_path)
        return GeneratedProjectModuleRuntime().execute(tmp_path, self._load)

    def _load(self):
        return tuple(importlib.import_module("assemblies."+name) for name in (
            "framed_front_spec", "applied_frame_front", "specification",
            "assembly_tree", "panel_assembly"))

    def front(self, contracts, **changes):
        spec, _, _, _, _ = contracts
        values = dict(assembly_id="door_01", width_mm=420, height_mm=720,
                      backing_thickness_mm=9, frame_thickness_mm=7,
                      borders=spec.FrameBorders(45, 55, 70, 40),
                      opening_corner_radius_mm=4)
        return spec.FramedFrontSpec(**(values | changes))
