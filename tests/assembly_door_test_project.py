"""Scope: Save a real multi-part front with one explicitly owned hinge support."""
from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
from door_hinge_plan import DoorHingePlanner
from door_hinge_side import DoorHingeSide
from door_host import DoorHost, DoorHostSpec
from door_host_test_support import DoorHostTestSupport
from init_framed_door_design import FramedDoorDesignProject
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as PROFILE


class AssemblyDoorTestProject:
    def create(self, root, hand=DoorHingeSide.LEFT, border=60, generate=True):
        FramedDoorDesignProject().initialize(root)
        host = DoorHostTestSupport().create(root, hand)
        folder = root/'assemblies/niche_01'
        declaration = DoorHostSpec('front_01', 'post', 'front_01')
        (folder/'spec.py').write_text('"""Scope: Declare a support and an optional framed child."""\n'
            'from assemblies.specification import *\nfrom assemblies.panel_assembly import PanelAssemblySpec\n'
            'from assemblies.framed_front_spec import FrameBorders, FramedFrontSpec\n'
            'from door_host import DoorHostSpec\n'
            f'FRONT_PLACEMENT = {host.door.local_to_parent!r}\n'
            f'FRONT = FramedFrontSpec("front_01",500,1000,9,9,FrameBorders({border},60,60,60),4, '
            'backing_material_id="mdf-back",frame_material_id="mdf-frame")\n'
            f'SPEC = PanelAssemblySpec("niche_01", "custom front", ({host.support!r},), '
            'child_assemblies=(ChildAssemblySpec("front_01", "framed front", FRONT_PLACEMENT),), requirements=())\n'
            f'DOOR_HOST = {declaration!r}\n')
        (folder/'builder.py').write_text('"""Scope: Build the physical support and front through common tools."""\n'
            'from assemblies.panel_assembly import PanelAssemblyBuilder\n'
            'from assemblies.applied_frame_front import FramedFrontBuilder\n'
            'from .spec import SPEC, FRONT, FRONT_PLACEMENT\n'
            'class Builder:\n    def build(self):\n'
            '        front = FramedFrontBuilder(FRONT).child(FRONT_PLACEMENT)\n'
            '        return PanelAssemblyBuilder(SPEC, children=(front,)).build()\n'
            'BUILDER = Builder()\n')
        built = GeneratedAssemblyBuilderLoader().load_assembly(root, 'niche_01')
        resolved = DoorHost.resolve(built, hand, declaration)
        plan = DoorHingePlanner().plan(resolved, PROFILE, hand)
        if generate:
            CabinetDoorFeatureGenerator().generate(root, resolved, plan, PROFILE)
        return built, plan
