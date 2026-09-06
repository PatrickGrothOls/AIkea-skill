"""Scope: Prove exact KA 4532 hardware hydrates and places at tree depth."""

from types import SimpleNamespace

import cadquery as cq
import pytest

import hettich_ka_4532_spacer_step_set as step_set_module
from assembly_composition_test_case import AssemblyCompositionTestCase
from local_to_parent_location import LocalToParentLocation
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from purchased_hardware_hydrator import PurchasedHardwareHydrator


class TestHettichKa4532RecursiveHydration(AssemblyCompositionTestCase):
    """Protect exact selectors and rigid placements in a nested assembly."""

    def test_hydrates_right_runner_and_same_spacer_without_scaling(
        self, generated_values, monkeypatch
    ) -> None:
        specification, project_root = generated_values
        step_set = self._step_set()
        monkeypatch.setattr(
            step_set_module.HettichKa4532SpacerStepSetLoader,
            "load",
            lambda _loader, _hardware_root: step_set,
        )
        runner_frame = self._placement(specification, (499.0, 11.5, 23.0))
        spacer_frame = self._placement(
            specification,
            (725.0, 10.0, 50.0),
            axes=((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)),
        )
        hardware_specs = (
            specification.PurchasedHardwareSpec(
                "runner_right", "Hettich", "KA 4532",
                "hettich-ka-4532-500-runner-pair", runner_frame,
                geometry_selector="right",
            ),
            specification.PurchasedHardwareSpec(
                "spacer_right", "Hettich", "13952",
                "hettich-13952-spacer-profile", spacer_frame,
            ),
        )
        child = self._nested_child(specification, hardware_specs)

        hydrated = PurchasedHardwareHydrator(
            ProjectHardwareGeometryResolver()
        ).hydrate(project_root, child)

        runner, spacer = hydrated.child_assemblies[0].assembly.purchased_hardware
        assert len(runner.solid.val().Solids()) == 2
        assert spacer.solid.val().isSame(step_set.spacer_solid)
        self._assert_rigid_bounds(runner.solid.val(), runner_frame, 683.5, 704.0)
        self._assert_rigid_bounds(spacer.solid.val(), spacer_frame, 700.0, 725.0)

    def _step_set(self):
        fixed = cq.Workplane("XY").box(8.0, 10.0, 4.0).val().located(
            cq.Location(cq.Vector(201.0, -9.5, 0.0))
        )
        moving = cq.Workplane("XY").box(8.0, 10.0, 4.0).val().located(
            cq.Location(cq.Vector(188.5, -6.5, 0.0))
        )
        spacer = cq.Workplane("XY").box(
            25.0, 10.0, 50.0, centered=(False, False, False)
        ).val()
        side = SimpleNamespace(fixed_member=fixed, moving_member=moving)
        return SimpleNamespace(runner_left=side, runner_right=side, spacer_solid=spacer)

    def _nested_child(self, values, hardware_specs):
        identity = values.IDENTITY_LOCAL_TO_PARENT
        drawer_spec = self.fixture_assembly_spec("drawer_01", "drawer", (), hardware_specs)
        drawer = values.BuiltAssembly(
            drawer_spec, (), (),
            purchased_hardware=tuple(
                values.BuiltPurchasedHardware(spec, None) for spec in hardware_specs
            ),
        )
        child_spec = values.ChildAssemblySpec("drawer_01", "drawer", identity)
        cabinet_spec = self.fixture_assembly_spec(
            "cabinet_01", "cabinet", (child_spec,), ()
        )
        return values.BuiltAssembly(
            cabinet_spec, (), (),
            child_assemblies=(values.BuiltChildAssembly(child_spec, drawer),),
        )

    def _placement(self, values, origin, axes=None):
        basis = axes or ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        return values.LocalToParentPlacement(
            values.Point3D(*origin),
            values.AxisBasis(*(values.AxisDirection(*axis) for axis in basis)),
        )

    def _assert_rigid_bounds(self, shape, frame, expected_xmin, expected_xmax):
        source_volume = shape.Volume()
        placed = shape.located(LocalToParentLocation().build(frame))
        bounds = placed.BoundingBox()
        assert bounds.xmin == pytest.approx(expected_xmin)
        assert bounds.xmax == pytest.approx(expected_xmax)
        assert placed.Volume() == pytest.approx(source_volume)
