"""Scope: Save a small authored door and support with no standard cabinet metadata."""

import importlib

from door_hinge_side import DoorHingeSide
from door_host import DoorHostSpec
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from door_host_loader import DoorHostLoader


class DoorHostTestSupport:
    def create(self, root, hand=DoorHingeSide.LEFT, face=">Z", inset=20):
        FurnitureDesignProject().initialize(root)
        values = GeneratedProjectModuleRuntime().execute(root, lambda: importlib.import_module("assemblies.specification"))
        left = hand is DoorHingeSide.LEFT
        origin = (100, 50, 32) if left else (602, 632, 32)
        axes = ((0, 1, 0), (0, 0, 1), (1, 0, 0)) if left else ((0, -1, 0), (0, 0, 1), (-1, 0, 0))
        if face == "<Z":
            origin = (118, 632, 32) if left else (584, 50, 32)
            axes = tuple(tuple(-value for value in axis) if index != 1 else axis for index, axis in enumerate(axes))
        support = values.PartSpec("post", "support", (), self._frame(values, origin, axes),
                                  local_size_mm=(582, 1000, 18), inside_face=face, material_id="mdf")
        door = values.PartSpec("slab", "front", (), self._frame(values, (101, 50+inset, 32),
                               ((1, 0, 0), (0, 0, 1), (0, -1, 0))),
                               local_size_mm=(500, 1000, 18), inside_face="<Z", material_id="mdf")
        declaration = DoorHostSpec("slab", "post")
        folder = root/'assemblies/niche_01'
        folder.mkdir()
        (folder/'__init__.py').write_text('"""Scope: Own the test front and support."""\n')
        (folder/'spec.py').write_text('"""Scope: Declare one authored front with its hinge support."""\n'
            'from assemblies.specification import *\nfrom assemblies.panel_assembly import PanelAssemblySpec\n'
            'from door_host import DoorHostSpec\n'
            f'SPEC = PanelAssemblySpec("niche_01", "custom front", {(support, door)!r}, requirements=())\n'
            f'DOOR_HOST = {declaration!r}\n')
        (folder/'builder.py').write_text('"""Scope: Build the authored panels through the common engine."""\n'
            'from assemblies.panel_assembly import PanelAssemblyBuilder\nfrom .spec import SPEC\nBUILDER = PanelAssemblyBuilder(SPEC)\n')
        assembly = CabinetAssemblySpecLoader().load(root, 'niche_01')
        return DoorHostLoader().load(root, assembly, hand)

    def _frame(self, values, origin, axes):
        return values.LocalToParentPlacement(values.Point3D(*origin), values.AxisBasis(*(values.AxisDirection(*axis) for axis in axes)))
