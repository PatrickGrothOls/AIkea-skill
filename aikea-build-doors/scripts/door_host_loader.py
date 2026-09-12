"""Scope: Load an authored door host while retaining the caller's current feature-free assembly."""

from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from door_host import DoorHost


class DoorHostLoader:
    def load(self, project_root, assembly, hinge_side):
        spec = getattr(assembly, "spec", assembly)
        module = CabinetAssemblySpecLoader().load_module(project_root, spec.assembly_id)
        return DoorHost.resolve(assembly, hinge_side, getattr(module, "DOOR_HOST", None))
