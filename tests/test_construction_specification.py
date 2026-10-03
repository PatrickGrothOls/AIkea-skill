"""Scope: Check shared construction inputs in a real generated project package."""

from dataclasses import replace
import importlib

from assembly_composition_test_case import AssemblyCompositionTestCase


class TestConstructionSpecification(AssemblyCompositionTestCase):
    """Keep the input contract compatible with existing physical tree consumers."""

    def test_configured_parts_can_be_reused_and_adapted(self, generated_values):
        values, _ = generated_values
        construction = importlib.import_module("assemblies.construction_specification")
        configured = importlib.import_module("assemblies.tall_storage_01.spec").SPEC
        shared = construction.PanelAssemblySpec(
            configured.assembly_id, configured.purpose, configured.parts,
            configured.joints, configured.child_assemblies, configured.purchased_hardware,
        )
        original = shared.parts[0]
        changed = replace(original, material_id="mdf", role="custom_partition")
        adapted = replace(shared, purpose="custom arrangement",
                          parts=(changed, *shared.parts[1:]))
        assert shared.part(original.part_id) == original
        assert adapted.part(original.part_id).material_id == "mdf"
        assert adapted.part(original.part_id).local_to_parent == original.local_to_parent
        assert adapted.joints == configured.joints
        assert original.material_id == "Test white cabinet panel, 18 mm"
        built = values.BuiltAssembly(
            adapted, tuple(values.BuiltPart(part, object()) for part in adapted.parts),
            adapted.joints,
        )
        assert built.spec is adapted
        assert built.parts[0].spec.material_id == "mdf"

    def test_local_machining_is_explicit_without_role_dispatch(self, generated_values):
        values, root = generated_values
        construction = importlib.import_module("assemblies.construction_specification")
        part = values.PartSpec("partition", "custom", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(400, 700, 16), material_id="mdf")
        request = construction.PartMachiningSpec("adjustment_grid", "partition", "system_32")
        plain = construction.PanelAssemblySpec("custom_01", "unregistered", (part,))
        drilled = replace(plain, machining=(request,))
        assert plain.machining == ()
        assert drilled.machining == (request,)
        assert drilled.parts == plain.parts
        assert (root / "assemblies/construction_specification.py").is_file()
