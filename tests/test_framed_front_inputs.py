"""Scope: Reject impossible front inputs and preserve project-local customizations."""

import pytest
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from cnc_work_area import CncWorkAreaError
from framed_front_test_support import FramedFrontTestSupport
from init_framed_door_design import FramedDoorDesignProject


class TestFramedFrontInputs(FramedFrontTestSupport):
    @pytest.mark.parametrize("changes", [
        {"width_mm": 0}, {"height_mm": float("inf")},
        {"backing_thickness_mm": -1}, {"frame_thickness_mm": float("nan")},
        {"opening_corner_radius_mm": -1}, {"opening_corner_radius_mm": 300},
    ])
    def test_rejects_impossible_dimensions(self, contracts, changes):
        with pytest.raises(ValueError):
            self.front(contracts, **changes)

    def test_rejects_borders_without_an_opening(self, contracts):
        specs = contracts[0]
        with pytest.raises(ValueError, match="positive opening"):
            self.front(contracts, borders=specs.FrameBorders(210, 210, 50, 50))

    def test_rejects_oversized_blank_even_with_large_opening(self, contracts):
        with pytest.raises(CncWorkAreaError, match="CNC work area"):
            contracts[1].FramedFrontBuilder(self.front(contracts, width_mm=2491)).build()

    def test_reinitialization_preserves_custom_geometry(self, tmp_path):
        project = FramedDoorDesignProject()
        project.initialize(tmp_path)
        assert project.initialize(tmp_path) == ()
        builder = tmp_path / "assemblies/applied_frame_front.py"
        custom = builder.read_text()+"\n# Deliberate local profile customization.\n"
        builder.write_text(custom)
        with pytest.raises(AssemblyTaxonomyConflict):
            project.initialize(tmp_path)
        assert builder.read_text() == custom
