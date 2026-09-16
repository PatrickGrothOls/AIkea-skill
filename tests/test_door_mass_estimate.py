"""Scope: Protect sloped/material-specific mass and unknown finished-mass handling."""
from types import SimpleNamespace
import pytest
from door_mass_estimate import DoorMassEstimator
from door_host_test_support import DoorHostTestSupport
from door_hinge_plan import DoorHingePlanner
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY


class TestDoorMassEstimate:
    def test_sloped_panel_uses_polygon_instead_of_tall_bounding_rectangle(self):
        points = tuple(SimpleNamespace(x_mm=x, height_mm=y)
                       for x,y in ((0,0),(600,0),(600,1000),(0,2000)))
        host = SimpleNamespace(door=SimpleNamespace(local_size_mm=(600,2000,18),
            outline_mm=points, material_id="painted_mdf"))
        estimate = DoorMassEstimator().estimate(host, {"painted_mdf": 750},
            {"painted_mdf": 0}, basis="Test density; uncoated", attached_hardware_kg=0.5)
        assert estimate.panel_and_finish_kg == pytest.approx(12.15)
        assert estimate.total_kg == pytest.approx(12.65)

    def test_unknown_hardware_mass_is_not_zero(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        estimate = DoorMassEstimator().estimate(host, {"mdf": 750}, {"mdf": .25},
            basis="Unselected MDF and paint estimates")
        assert estimate.panel_and_finish_kg > 6.75
        assert estimate.total_kg is None
        plan = DoorHingePlanner().plan(host, RIEX_NC70_FULL_OVERLAY, mass_estimate=estimate)
        assert plan.door_mass_kg is None
        assert not plan.fabrication_ready
        assert plan.mass_basis == estimate.basis

    def test_absent_material_inputs_do_not_fall_back_to_plywood(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        plan = DoorHingePlanner().plan(host, RIEX_NC70_FULL_OVERLAY)
        assert plan.door_mass_kg is None
        assert any("mass unresolved" in issue for issue in plan.compatibility_issues)

    def test_known_mass_does_not_qualify_height_only_hinge_count(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        estimate = DoorMassEstimator().estimate(host, {"mdf": 750}, {"mdf": .25},
            attached_hardware_kg=0.5, basis="Explicit synthetic mass")
        plan = DoorHingePlanner().plan(host, RIEX_NC70_FULL_OVERLAY, mass_estimate=estimate)
        assert plan.door_mass_kg == estimate.total_kg
        assert not plan.fabrication_ready
        assert any("load/count qualification unresolved" in issue for issue in plan.compatibility_issues)
