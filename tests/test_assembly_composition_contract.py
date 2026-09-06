"""Scope: Verify nested assemblies and purchased hardware match declared frames."""

from __future__ import annotations

import importlib

from assembly_composition_test_case import AssemblyCompositionTestCase


class TestAssemblyCompositionContract(AssemblyCompositionTestCase):
    """Protect the generic composition boundary used by future child assemblies."""

    def test_existing_specs_keep_empty_composition(self, generated_values) -> None:
        specification, project_root = generated_values
        spec_module = importlib.import_module("assemblies.tall_storage_01.spec")
        empty_spec = self.fixture_assembly_spec("empty_01", "empty", (), ())
        built = specification.BuiltAssembly(empty_spec, (), ())

        assert spec_module.SPEC.child_assemblies == ()
        assert spec_module.SPEC.purchased_hardware == ()
        assert built.child_assemblies == ()
        assert built.purchased_hardware == ()
        assert specification.IDENTITY_LOCAL_TO_PARENT.origin_in_parent.x_mm == 0.0
        assert (project_root / "assemblies/assembly_composition.py").is_file()
        assert (project_root / "assemblies/assembly_placement.py").is_file()
        assert (project_root / "assemblies/assembly_tree.py").is_file()

    def test_child_and_hardware_keep_explicit_local_to_parent_frames(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        identity = values.IDENTITY_LOCAL_TO_PARENT
        drawer_placement = values.LocalToParentPlacement(
            origin_in_parent=values.Point3D(18.0, 12.0, 640.0),
            axis_basis=values.AxisBasis(
                local_x_in_parent=values.AxisDirection(1.0, 0.0, 0.0),
                local_y_in_parent=values.AxisDirection(0.0, 0.0, 1.0),
                local_z_in_parent=values.AxisDirection(0.0, -1.0, 0.0),
            ),
        )
        runner = values.PurchasedHardwareSpec(
            hardware_id="runner_left",
            manufacturer="Blum",
            product_code="760H5500S-left",
            hardware_asset_id="movento-760h5500s-runner-left",
            local_to_parent=identity,
        )
        drawer_spec = self.fixture_assembly_spec(
            "drawer_01", "drawer", (), (runner,)
        )
        built_runner = values.BuiltPurchasedHardware(runner, object())
        built_drawer = values.BuiltAssembly(
            drawer_spec,
            (),
            (),
            purchased_hardware=(built_runner,),
        )
        child_spec = values.ChildAssemblySpec(
            "drawer_01", "drawer", drawer_placement
        )
        built_child = values.BuiltChildAssembly(child_spec, built_drawer)
        cabinet_spec = self.fixture_assembly_spec(
            "cabinet_01",
            "storage",
            (child_spec,),
            (),
        )

        built_cabinet = values.BuiltAssembly(
            cabinet_spec,
            (),
            (),
            child_assemblies=(built_child,),
        )

        assert built_cabinet.child_assemblies[0].spec.local_to_parent == drawer_placement
        assert runner.hardware_asset_id == "movento-760h5500s-runner-left"
        assert not hasattr(runner, "cad_asset_path")
        assert built_drawer.purchased_hardware[0].spec.local_to_parent == identity
        assert built_drawer.purchased_hardware[0].has_geometry
