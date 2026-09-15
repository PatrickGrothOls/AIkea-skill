"""Scope: Present one owned light and check its body against the own manufactured subtree."""

from dataclasses import dataclass

from assembly_tree_review_plan import AssemblyReviewOverlay, AssemblyTreeReviewPlan
from cabinet_lighting_placement import CabinetLightingPlacementBuilder
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from lighting_purchase import LightingPurchase
from local_to_parent_location import LocalToParentLocation
from part_lighting_builder import PartLightingBuilder
from part_lighting_plan import PartLightingPlan
from unit_mockup import MockupPart


@dataclass(frozen=True)
class LightingComponentReview:
    lighting_plan: PartLightingPlan

    def plan(self, context, state):
        if state not in {"closed", "on", "off"}:
            raise ValueError("Lighting review supports on/off; remove the feature to remove its construction")
        plan = self.lighting_plan
        if context.assembly.spec.assembly_id != plan.assembly_id:
            raise ValueError("lighting review and owning assembly differ")
        host = next(part for part in context.assembly.parts if part.spec.part_id == plan.part_id)
        hardware = next(item for item in context.assembly.purchased_hardware if item.spec.hardware_id == plan.run.run_id)
        if hardware.spec != LightingPurchase().build(plan.run, hardware.spec.local_to_parent):
            raise ValueError("lighting review differs from its current purchased variant")
        geometry = PartLightingBuilder().prepare(host, plan)
        placement = CabinetLightingPlacementBuilder().build(context.assembly.spec, host.spec, plan)
        body = geometry.luminaire_body.val().located(placement.luminaire_location)
        current = hardware.solid.val().located(LocalToParentLocation().build(hardware.spec.local_to_parent))
        if body.cut(current).Volume()+current.cut(body).Volume() > 1e-5:
            raise ValueError("lighting review differs from its current owned hardware")
        for item in GeneratedAssemblyBuilderLoader().walk(context.project_root, context.assembly):
            if hasattr(item, "part"):
                solid = item.part.solid.val().located(LocalToParentLocation().build(item.local_to_root))
                if body.intersect(solid).Volume() > 0.01:
                    raise ValueError("light body interferes with manufactured part: "+"/".join(item.path))
        profile = plan.run.profile.profile_id
        parts = [MockupPart(f"purchased_light__{profile}__{plan.run.run_id}", geometry.luminaire_body,
                            placement.luminaire_location, (0.23, 0.24, 0.22, 1.0),
                            inspection_path=(plan.part_id, plan.run.run_id), review_kind="hardware")]
        if state != "off":
            color = {2900: (1.0, 0.68, 0.38, 1.0), 3200: (1.0, 0.76, 0.50, 1.0),
                     4300: (1.0, 0.90, 0.74, 1.0)}[plan.run.color_temperature_k]
            parts.append(MockupPart(f"light_source__{profile}__{plan.run.run_id}__{plan.run.color_temperature_k}k",
                                   geometry.emitter_face, placement.luminaire_location, color,
                                   inspection_path=(plan.part_id, plan.run.run_id), review_kind="hardware"))
        return AssemblyTreeReviewPlan(hidden_paths=(context.owner_path+(f"hardware:{plan.run.run_id}",),),
            overlays=(AssemblyReviewOverlay(context.owner_path, tuple(parts)),))
