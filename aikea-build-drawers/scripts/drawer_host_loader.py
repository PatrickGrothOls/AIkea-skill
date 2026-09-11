"""Scope: Load an authored drawer host declaration or adapt a standard generated cabinet."""

from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from drawer_host import DrawerHost


class DrawerHostLoader:
    def load(self, project_root, assembly_id):
        module = CabinetAssemblySpecLoader().load_module(project_root, assembly_id)
        declaration = getattr(module, "DRAWER_HOST", None)
        return (DrawerHost(module.SPEC, declaration) if declaration is not None
                else DrawerHost.resolve(module.SPEC))
