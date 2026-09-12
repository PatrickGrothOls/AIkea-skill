"""Scope: Retain the lighting-review command as an adapter to generic complete-assembly review."""

from hashlib import sha256
import json

from assembly_review_feature_loader import AssemblyReviewFeatureLoader
from cabinet_lighting_review import CabinetLightingReviewResult
from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
from door_review_state import DoorReviewState
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from part_lighting_plan_loader import PartLightingPlanLoader


class CabinetLightingReviewGenerator:
    def generate(self, project_root, assembly_id, part_id, *, base_builder_module="complete_builder",
                 hardware_directory=None, door_state=DoorReviewState.REMOVED):
        # The old hardware-directory argument is retained for callers; registered providers own CAD loading.
        if base_builder_module not in {"builder", "complete_builder"}:
            raise ValueError("Move existing features into complete_builder before lighting review")
        plan = PartLightingPlanLoader().load(project_root/'assemblies'/assembly_id/'parts'/part_id/'lighting.yaml')
        if (plan.assembly_id, plan.part_id) != (assembly_id, part_id):
            raise ValueError("lighting review must use the requested owner and host")
        loader, features = GeneratedAssemblyBuilderLoader(), AssemblyReviewFeatureLoader()
        built = loader.load_assembly(project_root, assembly_id)
        registrations = tuple((visit.path, feature)
            for visit in loader.walk(project_root, built) if hasattr(visit, "assembly")
            for feature in features.load(project_root, visit.path))
        active = next((feature.feature for owner, feature in registrations
                       if owner == (assembly_id,) and feature.feature_id == 'lighting'), None)
        if active is None:
            raise ValueError("No registered lighting review; add or regenerate the saved lighting feature")
        if active.lighting_plan != plan:
            raise ValueError("Requested lighting plan is inactive; review the current registered host and run")
        states = {"/".join((*owner, feature.feature_id)): door_state.value
                  for owner, feature in registrations if feature.feature_id == 'door_hinges'}
        output = project_root/'assemblies'/assembly_id/(assembly_id+'_lighting_review.glb')
        result = CompleteAssemblyReviewGenerator().generate(project_root, assembly_id, output, states)
        report = output.with_name('lighting-fit-check.json')
        report.write_text(json.dumps(dict(schema_version=1, status='geometry_preview', manufacturing_authority=False,
            glb_sha256=sha256(output.read_bytes()).hexdigest(), review_report=str(result.report_path.relative_to(project_root)),
            checks=['common groove construction', 'light body clearance against manufactured parts in its owner subtree'],
            unresolved=['manufactured-part clearance outside the lighting owner subtree', 'illumination placement approval', 'other hardware and movement clearance',
                        'supply, controls, cable route and final product installation']), indent=2)+'\n')
        return CabinetLightingReviewResult(assembly_id, output, report)
