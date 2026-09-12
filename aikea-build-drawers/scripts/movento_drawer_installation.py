"""Scope: Add a MOVENTO drawer, both runners, both clips and all host cuts together."""
from dataclasses import dataclass, replace
from typing import Any
from movento_panel_drawer import MoventoPanelDrawer
from movento_panel_machining import MoventoPanelMachining
from panel_machining_feature import PanelMachiningFeature


@dataclass(frozen=True)
class MoventoInstallationRequest:
    drawer_id: str
    dimensions: Any
    pilots: Any
    placement: Any
    left_part_id: str
    right_part_id: str


class MoventoDrawerInstallation:
    """Compose the complete candidate; qualification requirements stay unresolved.

    Caller supplies real supporting part IDs and the drawer's closed frame.
    Hardware hydration uses the existing checksum-gated project CAD provider.
    This does not waive source-fit, material, motion or fabrication checks.
    """

    def apply(self, parent, drawer_id, dimensions, pilots, placement, left_part_id, right_part_id):
        return self.apply_many(parent,(MoventoInstallationRequest(drawer_id,dimensions,pilots,placement,
                                                                   left_part_id,right_part_id),))

    def apply_many(self, parent, requests):
        requests = tuple(requests)
        names = tuple(r.drawer_id for r in requests)
        existing = {c.spec.assembly_id for c in parent.child_assemblies}
        if len(names) != len(set(names)) or existing.intersection(names):
            raise ValueError("drawer ID already exists; revise its saved installation explicitly")
        prepared = tuple(self._prepare(parent,r) for r in requests)
        cuts = tuple(cut for _,_,cuts,_ in prepared for cut in cuts)
        requirements = tuple(req for _,_,_,reqs in prepared for req in reqs)
        # Batch the host cuts so repeated drawers do not revalidate the growing
        # complete parent after each individual installation.
        result = PanelMachiningFeature().apply(parent,cuts,requirements)
        children = result.child_assemblies + tuple(child for child,_,_,_ in prepared)
        hardware = result.purchased_hardware + tuple(h for _,items,_,_ in prepared for h in items)
        return replace(result,spec=replace(result.spec,child_assemblies=tuple(c.spec for c in children),
                                          purchased_hardware=tuple(h.spec for h in hardware)),
                       child_assemblies=children,purchased_hardware=hardware)

    def _prepare(self, parent, request):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        from assemblies.specification import (ChildAssemblySpec, BuiltChildAssembly,
            BuiltPurchasedHardware, ConstructionRequirementSpec)
        drawer_id, dimensions, pilots, placement = request.drawer_id, request.dimensions, request.pilots, request.placement
        recipe = MoventoPanelDrawer()
        drawer_spec = recipe.specification(drawer_id, dimensions, pilots)
        clips, runners, host_cuts = [], [], []
        for hand, x, part_id in (("left",0,request.left_part_id),("right",dimensions.clear_width_mm,request.right_part_id)):
            clips.append(self.clip(hand,x))
            runners.append(self.runner(drawer_id,hand,x,placement))
            host_cuts.append(MoventoPanelMachining().host(drawer_id+"_"+hand,
                parent.spec.part(part_id),placement,x,pilots,recipe.frame))
        drawer_spec = replace(drawer_spec,purchased_hardware=tuple(clips),requirements=drawer_spec.requirements+(
            ConstructionRequirementSpec("locking_device_installation", "Qualify locking-device fixing and engagement",
                                        tuple("hardware:"+h.hardware_id for h in clips)),))
        drawer = PanelAssemblyBuilder(drawer_spec,hardware=tuple(BuiltPurchasedHardware(h,None) for h in clips)).build()
        child_spec = ChildAssemblySpec(drawer_id,drawer_spec.purpose,placement)
        requirements = (
            ConstructionRequirementSpec(drawer_id+"_host_preparation", "Prepare both physical runner hosts",
                ("part:"+request.left_part_id,"part:"+request.right_part_id),
                tuple("machining:"+cut.machining_id for cut in host_cuts),"operations",pilots.basis),
            ConstructionRequirementSpec(drawer_id+"_runner_installation", "Qualify exact runner fixing and installed motion",
                                        tuple("hardware:"+h.hardware_id for h in runners)),
        )
        return (BuiltChildAssembly(child_spec,drawer),tuple(BuiltPurchasedHardware(h,None) for h in runners),
                tuple(host_cuts),requirements)

    def clip(self, hand, x):
        from assemblies.specification import PurchasedHardwareSpec, HardwarePurchaseSpec
        product = "T51.7601 " + ("L" if hand=="left" else "R")
        purchase = HardwarePurchaseSpec("locking_"+hand,product,"piece",hand,(hand,),mounting_fasteners_included=False)
        return PurchasedHardwareSpec("locking_"+hand,"Blum",product,"t51-7601-"+hand+"-locking-device",
                                     self.native(x),purchase=purchase)

    def runner(self, drawer_id, hand, x, placement):
        from assemblies.specification import PurchasedHardwareSpec, HardwarePurchaseSpec
        purchase = HardwarePurchaseSpec(drawer_id+"_runners","760H5000S","pair",hand,("left","right"),
                                        mounting_fasteners_included=False)
        return PurchasedHardwareSpec(drawer_id+"_runner_"+hand,"Blum","760H5000S",
            "movento-760h5000s-runner-"+hand,placement.compose_child(self.native(x)),purchase=purchase)

    def native(self, x):
        return MoventoPanelDrawer.frame((x,37,9.575),((1,0,0),(0,0,1),(0,-1,0)))


__all__ = ["MoventoDrawerInstallation", "MoventoInstallationRequest"]
