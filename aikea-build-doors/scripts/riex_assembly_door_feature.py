"""Scope: Attach an owned multi-part front using existing hinge tooling and shared layer drilling."""
from dataclasses import dataclass, replace

from assembly_door_host import AssemblyDoorHost
from layered_surface_drilling import LayeredSurfaceDrilling
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from riex_nc70_hardware_specs import RiexNc70HardwareSpecs
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from riex_nc70_machining_recipe import RiexNc70MachiningRecipe


@dataclass(frozen=True)
class RiexAssemblyDoorFeature:
    plan: object

    def recipe(self, assembly):
        host = AssemblyDoorHost(assembly, self.plan.host_spec, self.plan.hinge_side)
        original = RiexNc70MachiningRecipe().build(host, self.plan, RIEX_NC70_FULL_OVERLAY)
        parent, front = [], []
        for request in original:
            if request.part_id == self.plan.door_part_id:
                front.extend(LayeredSurfaceDrilling().build(request.machining_id,
                    host.front.assembly.spec.parts, request.surface_to_part, request.holes))
            else:
                parent.append(request)
        return host, tuple(parent), tuple(front)

    def apply(self, assembly):
        from assemblies.specification import BuiltPurchasedHardware, ConstructionRequirementSpec

        host, parent_requests, front_requests = self.recipe(assembly)
        feature = PanelMachiningFeature()
        front = feature.apply(host.front.assembly, front_requests,
                              self._requirements(front_requests, ConstructionRequirementSpec))
        children = tuple(replace(child, assembly=front) if child is host.front else child
                         for child in assembly.child_assemblies)
        machined = feature.apply(replace(assembly, child_assemblies=children), parent_requests,
                                 self._requirements(parent_requests, ConstructionRequirementSpec))
        hardware = RiexNc70HardwareSpecs().build(host, self.plan, RIEX_NC70_FULL_OVERLAY)
        existing = {item.spec.hardware_id for item in assembly.purchased_hardware}
        identifiers = tuple(item.hardware_id for item in hardware)
        if len(set(identifiers)) != len(identifiers) or existing.intersection(identifiers):
            raise PartConstructionError("hinge purchases require distinct newly owned IDs")
        subjects = host.front_subjects+(f"part:{self.plan.support_part_id}",)+tuple(
            f"hardware:{name}" for name in identifiers)
        requirements = (ConstructionRequirementSpec("door_layered_installation",
            "Confirm whole-front attachment, selected screws, engagement and opening clearance", subjects,
            basis="Machining and source-CAD poses do not establish adhesive, material, load or motion suitability"),)
        declared = machined.spec.requirements
        spec = replace(machined.spec, purchased_hardware=machined.spec.purchased_hardware+hardware,
                       requirements=declared+requirements if declared is not None else None)
        return replace(machined, spec=spec, purchased_hardware=machined.purchased_hardware+tuple(
            BuiltPurchasedHardware(item, None) for item in hardware))

    def _requirements(self, requests, contract):
        return tuple(contract(request.machining_id, "Machine the selected hinge pattern",
            (f"part:{request.part_id}",), (f"machining:{request.machining_id}",), "operations")
            for request in requests)
