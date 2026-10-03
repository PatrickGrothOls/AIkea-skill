"""Scope: Verify generic traversal and placement across arbitrary assembly depth."""

from __future__ import annotations

import importlib

import pytest

from assembly_composition_test_case import AssemblyCompositionTestCase


class TestAssemblyTreeWalker(AssemblyCompositionTestCase):
    """Protect the recursive physical spine independently of furniture type."""

    def test_accumulates_nested_frames_in_stable_tree_order(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        identity = values.IDENTITY_LOCAL_TO_PARENT
        cabinet_frame = values.LocalToParentPlacement(
            values.Point3D(100.0, 0.0, 0.0),
            values.IDENTITY_AXIS_BASIS,
        )
        drawer_frame = values.LocalToParentPlacement(
            values.Point3D(10.0, 0.0, 0.0),
            values.AxisBasis(
                values.AxisDirection(0.0, 1.0, 0.0),
                values.AxisDirection(-1.0, 0.0, 0.0),
                values.AxisDirection(0.0, 0.0, 1.0),
            ),
        )
        part_frame = values.LocalToParentPlacement(
            values.Point3D(5.0, 0.0, 0.0),
            values.IDENTITY_AXIS_BASIS,
        )
        hardware_frame = values.LocalToParentPlacement(
            values.Point3D(0.0, 2.0, 0.0),
            values.IDENTITY_AXIS_BASIS,
        )
        part_spec = values.PartSpec(
            "drawer_side", "drawer_side", (), part_frame
        )
        part = values.BuiltPart(part_spec, object())
        hardware_spec = values.PurchasedHardwareSpec(
            "runner_left", "Hettich", "9057405", "ka-5332-left", hardware_frame
        )
        drawer_spec = self.fixture_assembly_spec(
            "drawer_01", "drawer", (), (hardware_spec,), (part_spec,)
        )
        drawer = values.BuiltAssembly(
            drawer_spec,
            (part,),
            (),
            purchased_hardware=(values.BuiltPurchasedHardware(hardware_spec, object()),),
        )
        drawer_child = values.ChildAssemblySpec("drawer_01", "drawer", drawer_frame)
        cabinet_spec = self.fixture_assembly_spec(
            "cabinet_01", "cabinet", (drawer_child,), ()
        )
        cabinet = values.BuiltAssembly(
            cabinet_spec,
            (),
            (),
            child_assemblies=(values.BuiltChildAssembly(drawer_child, drawer),),
        )
        cabinet_child = values.ChildAssemblySpec(
            "cabinet_01", "cabinet", cabinet_frame
        )
        wardrobe_spec = self.fixture_assembly_spec(
            "wardrobe_01", "wardrobe", (cabinet_child,), ()
        )
        wardrobe = values.BuiltAssembly(
            wardrobe_spec,
            (),
            (),
            child_assemblies=(values.BuiltChildAssembly(cabinet_child, cabinet),),
        )

        visits = tree.AssemblyTreeWalker().walk(wardrobe, identity)

        assert tuple(type(item).__name__ for item in visits) == (
            "AssemblyTreeAssembly",
            "AssemblyTreeAssembly",
            "AssemblyTreeAssembly",
            "AssemblyTreePart",
            "AssemblyTreeHardware",
        )
        assert visits[3].path == (
            "wardrobe_01",
            "cabinet_01",
            "drawer_01",
            "part:drawer_side",
        )
        assert visits[3].local_to_root.origin_in_parent == values.Point3D(
            110.0, 5.0, 0.0
        )
        assert visits[4].local_to_root.origin_in_parent == values.Point3D(
            108.0, 0.0, 0.0
        )

    def test_requires_placement_only_for_hardware_with_geometry(
        self, generated_values
    ) -> None:
        values, _ = generated_values
        tree = importlib.import_module("assemblies.assembly_tree")
        hardware_spec = values.PurchasedHardwareSpec(
            "runner_left", "Hettich", "9057405", "ka-5332-left", None
        )
        spec = self.fixture_assembly_spec(
            "cabinet_01", "cabinet", (), (hardware_spec,)
        )
        declared_only = values.BuiltAssembly(
            spec,
            (),
            (),
            purchased_hardware=(values.BuiltPurchasedHardware(hardware_spec, None),),
        )

        visits = tree.AssemblyTreeWalker().walk(declared_only)

        assert visits[1].local_to_root is None
        with pytest.raises(tree.AssemblyTreeError, match="runner_left"):
            tree.AssemblyTreeWalker().walk(
                values.BuiltAssembly(
                    spec,
                    (),
                    (),
                    purchased_hardware=(
                        values.BuiltPurchasedHardware(hardware_spec, object()),
                    ),
                )
            )
