"""Scope: Render the shared builder and independent construction obligations of a drawer recipe."""


class DrawerConstructionModuleRenderer:
    def builder(self, drawer_id):
        return (
            f'"""Scope: Construct the editable {drawer_id} with shared panel tools."""\n\n'
            "from assemblies.panel_assembly import PanelAssemblyBuilder\n"
            "from assemblies.specification import BuiltPurchasedHardware\n"
            "from .spec import SPEC\n\n\n"
            "HARDWARE = tuple(BuiltPurchasedHardware(item, None) for item in SPEC.purchased_hardware)\n"
            "BUILDER = PanelAssemblyBuilder(SPEC, hardware=HARDWARE, allow_unresolved=True)\n"
        )

    def requirements(self, box, drilling=(), hardware_ids=()):
        subjects = tuple(f"part:{part.part_id}" for part in box.parts)
        operations = tuple(f"machining:{request.machining_id}" for request in drilling)
        disposition = "operations" if operations else "unresolved"
        installed = tuple(f"hardware:{identity}" for identity in hardware_ids)
        return (
            "    requirements=(\n"
            f"        ConstructionRequirementSpec('box_joinery', 'Resolve drawer-box joinery and bottom support', {subjects!r}),\n"
            "        ConstructionRequirementSpec('runner_fixings', 'Verify both drawer-side mounting interfaces', "
            f"('part:left_side', 'part:right_side'), {operations!r}, {disposition!r}),\n"
            "        ConstructionRequirementSpec('installed_motion', 'Verify installed hardware and drawer movement', "
            f"{subjects + installed!r}),\n"
            "    ),\n"
        )
