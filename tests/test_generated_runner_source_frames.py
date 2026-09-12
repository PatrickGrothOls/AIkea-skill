"""Scope: Preserve planned hardware frames when source CAD carries its own native placement."""
import cadquery as cq
import pytest

from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from test_hettich_ka_4532_spacer_cabinet_drawer_generator import (
    TestHettichKa4532SpacerCabinetDrawerGenerator as GeneratorFixture,
)


class TestGeneratedRunnerSourceFrames:
    def test_generated_hardware_frames_match_mounting_plan_with_native_source_location(self, tmp_path):
        fixture = GeneratorFixture()
        result = fixture._generate(tmp_path, fixture._project(tmp_path))
        source = result.plan.hardware_step.runner_left.moving_member
        assert source.location().toTuple() != cq.Location().toTuple()
        cabinet = GeneratedAssemblyBuilderLoader().load_assembly(tmp_path, "tall_storage_01")
        drawer = cabinet.child_assemblies[0].assembly
        planned_names = {
            f"drawer_01_{kind}_{side}_{state}": f"{state}_runner_{side}_in_{owner}"
            for side in ("left", "right")
            for kind, state, owner in (("runner", "fixed", "cabinet"), ("runner", "moving", "drawer"))
        }
        planned_names.update({f"drawer_01_spacer_{side}": f"spacer_{side}_in_cabinet"
                              for side in ("left", "right")})
        hardware = (*cabinet.purchased_hardware, *drawer.purchased_hardware)
        assert len(hardware) == len(planned_names) == 6
        for item in hardware:
            actual = item.spec.local_to_parent
            expected = getattr(result.plan.hardware_mounting, planned_names[item.spec.hardware_id])
            origin = actual.origin_in_parent
            assert (origin.x_mm, origin.y_mm, origin.z_mm) == pytest.approx(expected.origin_mm)
            for name, vector in (("x", expected.local_x_in_owner), ("y", expected.local_y_in_owner),
                                 ("z", expected.local_z_in_owner)):
                axis = getattr(actual.axis_basis, f"local_{name}_in_parent")
                assert (axis.x, axis.y, axis.z) == pytest.approx(vector)
