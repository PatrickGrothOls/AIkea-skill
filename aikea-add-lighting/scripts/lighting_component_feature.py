"""Scope: Own one light's common host machining, installed purchase and unresolved services."""

from dataclasses import dataclass, replace

from cabinet_lighting_placement import CabinetLightingPlacementBuilder
from lighting_machining_recipe import LightingMachiningRecipe
from panel_machining_feature import PanelMachiningFeature
from part_lighting_builder import PartLightingBuilder
from part_lighting_plan import PartLightingPlan
from purchased_hardware_spec import HardwarePurchaseSpec


@dataclass(frozen=True)
class LightingComponentFeature:
    plan: PartLightingPlan

    def apply(self, assembly):
        from assemblies.specification import BuiltPurchasedHardware, PurchasedHardwareSpec, ConstructionRequirementSpec

        plan, run = self.plan, self.plan.run
        self.validate_owner(assembly.spec)
        host = next(part for part in assembly.parts if part.spec.part_id == plan.part_id)
        request = LightingMachiningRecipe().build(host.spec, plan)
        geometry = PartLightingBuilder().prepare(host, plan)
        placement = CabinetLightingPlacementBuilder().build(assembly.spec, host.spec, plan)
        variant = f"{run.profile.product_name} / {run.length_mm:g} mm / {run.color_temperature_k} K"
        hardware_spec = PurchasedHardwareSpec(run.run_id, run.profile.manufacturer, variant,
            run.profile.profile_id, placement.luminaire_in_cabinet.as_project_placement(),
            geometry_selector=f"{run.length_mm:g}mm_{run.color_temperature_k}k",
            purchase=HardwarePurchaseSpec(run.run_id, variant, "piece", "luminaire", ("luminaire",)))
        requirements = (
            ConstructionRequirementSpec(run.run_id+"_mounting", "Machine the saved light groove",
                (f"part:{plan.part_id}",), (f"machining:{request.machining_id}",), "operations"),
            ConstructionRequirementSpec(run.run_id+"_installation", "Install the selected made-to-length luminaire",
                (f"part:{plan.part_id}", f"hardware:{run.run_id}"), ("feature:lighting.feature",), "operations"),
            ConstructionRequirementSpec(run.run_id+"_services",
                "Select compatible supply, controls and cable route; confirm product end and installation details",
                (f"part:{plan.part_id}", f"hardware:{run.run_id}"),
                basis="The groove and light envelope do not establish a complete electrical installation"),
        )
        machined = PanelMachiningFeature().apply(assembly, (request,), requirements)
        spec = replace(machined.spec, purchased_hardware=machined.spec.purchased_hardware+(hardware_spec,))
        hardware = BuiltPurchasedHardware(hardware_spec, geometry.luminaire_body)
        return replace(machined, spec=spec, purchased_hardware=machined.purchased_hardware+(hardware,))

    def validate_owner(self, spec):
        if spec.assembly_id != self.plan.assembly_id:
            raise ValueError("lighting plan and owning assembly differ")
        if any(item.hardware_id == self.plan.run.run_id for item in spec.purchased_hardware):
            raise ValueError("lighting needs a newly owned purchase ID")
