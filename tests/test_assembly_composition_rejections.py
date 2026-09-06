"""Scope: Reject nested assemblies and hardware that differ from saved specs."""

from __future__ import annotations

import pytest

from assembly_composition_test_case import AssemblyCompositionTestCase


class TestAssemblyCompositionRejections(AssemblyCompositionTestCase):
    """Keep built composition synchronized with its owning specification."""

    def test_built_parts_must_match_declared_specs(self, generated_values) -> None:
        values, _ = generated_values
        placement = values.IDENTITY_LOCAL_TO_PARENT
        declared = values.PartSpec("left_side", "side_panel", (), placement)
        different = values.PartSpec("right_side", "side_panel", (), placement)
        spec = self.fixture_assembly_spec(
            "cabinet_01", "storage", (), (), (declared,)
        )

        with pytest.raises(
            values.AssemblyCompositionError,
            match="built parts",
        ):
            values.BuiltAssembly(spec, (values.BuiltPart(different, object()),), ())

    def test_built_child_rejects_a_different_declared_placement(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        identity = values.IDENTITY_LOCAL_TO_PARENT
        drawer_spec = self.fixture_assembly_spec("drawer_01", "drawer", (), ())
        built_drawer = values.BuiltAssembly(drawer_spec, (), ())
        declared = values.ChildAssemblySpec("drawer_01", "drawer", identity)
        shifted = values.ChildAssemblySpec(
            "drawer_01",
            "drawer",
            values.LocalToParentPlacement(
                values.Point3D(10.0, 0.0, 0.0),
                identity.axis_basis,
            ),
        )
        built_child = values.BuiltChildAssembly(shifted, built_drawer)
        cabinet_spec = self.fixture_assembly_spec(
            "cabinet_01", "storage", (declared,), ()
        )

        with pytest.raises(
            values.AssemblyCompositionError,
            match="declared placements",
        ):
            values.BuiltAssembly(
                cabinet_spec,
                (),
                (),
                child_assemblies=(built_child,),
            )

    def test_built_child_rejects_a_different_identity(self, generated_values) -> None:
        values, _ = generated_values
        drawer_spec = self.fixture_assembly_spec("drawer_02", "drawer", (), ())
        built_drawer = values.BuiltAssembly(drawer_spec, (), ())
        declared = values.ChildAssemblySpec(
            "drawer_01", "drawer", values.IDENTITY_LOCAL_TO_PARENT
        )

        with pytest.raises(
            values.AssemblyCompositionError,
            match="child identity",
        ):
            values.BuiltChildAssembly(declared, built_drawer)

    def test_built_hardware_rejects_a_different_declared_instance(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        declared = values.PurchasedHardwareSpec(
            "runner_left",
            "Blum",
            "760H5500S-left",
            "movento-760h5500s-runner-left",
            values.IDENTITY_LOCAL_TO_PARENT,
        )
        different = values.PurchasedHardwareSpec(
            "runner_left",
            "Blum",
            "760H5500S-left",
            "movento-760h5500s-runner-left",
            values.LocalToParentPlacement(
                values.Point3D(1.0, 0.0, 0.0),
                values.IDENTITY_AXIS_BASIS,
            ),
        )
        drawer_spec = self.fixture_assembly_spec(
            "drawer_01", "drawer", (), (declared,)
        )

        with pytest.raises(
            values.AssemblyCompositionError,
            match="purchased hardware",
        ):
            values.BuiltAssembly(
                drawer_spec,
                (),
                (),
                purchased_hardware=(
                    values.BuiltPurchasedHardware(different, object()),
                ),
            )

    @pytest.mark.parametrize(
        ("x_axis", "y_axis", "z_axis"),
        (
            ((1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0)),
            ((2.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        ),
    )
    def test_saved_axis_basis_rejects_non_rigid_frames(
        self,
        generated_values,
        x_axis,
        y_axis,
        z_axis,
    ) -> None:
        values, _ = generated_values

        with pytest.raises(
            values.AssemblyPlacementError,
            match="orthonormal right-handed",
        ):
            values.AxisBasis(
                values.AxisDirection(*x_axis),
                values.AxisDirection(*y_axis),
                values.AxisDirection(*z_axis),
            )
