"""Scope: Export any recursively composed assembly through registered reviews."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_feature_review import AssemblyFeatureReviewContext
from assembly_review_feature_loader import AssemblyReviewFeatureLoader
from assembly_review_plan_composer import AssemblyReviewPlanComposer
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from assembly_tree_review_plan_validator import AssemblyTreeReviewPlanValidator
from cadquery_glb_exporter import CadQueryGlbExporter
from complete_assembly_review_report import CompleteAssemblyReviewReport
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from unit_mockup import MockupPart, UnitMockupInputError


@dataclass(frozen=True, slots=True)
class CompleteAssemblyReviewResult:
    """Report the exported tree and every available feature-state selector."""

    assembly_id: str
    glb_path: Path
    part_count: int
    feature_selectors: tuple[str, ...]
    report_path: Path
    rendered_parts: tuple[MockupPart, ...]


class CompleteAssemblyReviewGenerator:
    """Traverse, pose, hydrate, and export one arbitrary generated tree."""

    def __init__(
        self,
        loader=None,
        feature_loader=None,
        hydrator=None,
        geometry=None,
        exporter=None,
        composer=None,
        reporter=None,
        plan_validator=None,
    ) -> None:
        self.loader = loader or GeneratedAssemblyBuilderLoader()
        self.features = feature_loader or AssemblyReviewFeatureLoader()
        self.hydrator = hydrator or PurchasedHardwareHydrator(
            ProjectHardwareGeometryResolver()
        )
        self.geometry = geometry or AssemblyTreeReviewGeometry()
        self.exporter = exporter or CadQueryGlbExporter()
        self.composer = composer or AssemblyReviewPlanComposer()
        self.reporter = reporter or CompleteAssemblyReviewReport()
        self.plan_validator = plan_validator or AssemblyTreeReviewPlanValidator()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        output: Path,
        states: dict[str, str] | None = None,
    ) -> CompleteAssemblyReviewResult:
        requested = states or {}
        built = self.loader.load_assembly(project_root, assembly_id)
        visits = self.loader.walk(project_root, built)
        plans = []
        selectors = []
        resolved_states = {}
        for item in visits:
            if type(item).__name__ != "AssemblyTreeAssembly":
                continue
            for registration in self.features.load(project_root, item.path):
                selector = "/".join((*item.path, registration.feature_id))
                selectors.append(selector)
                resolved_states[selector] = requested.get(selector, "closed")
                context = AssemblyFeatureReviewContext(
                    project_root,
                    item.path,
                    item.assembly,
                )
                plans.append(
                    registration.feature.plan(
                        context,
                        resolved_states[selector],
                    )
                )
        unknown = sorted(set(requested) - set(selectors))
        if unknown:
            raise UnitMockupInputError(
                ["unknown assembly feature state: " + ", ".join(unknown)]
            )
        plan = self.composer.compose(tuple(plans))
        self.plan_validator.validate(visits, plan)
        hydrated = self.hydrator.hydrate(project_root, built, plan.hides)
        rendered = self.geometry.build(
            self.loader.walk(project_root, hydrated),
            {},
            plan,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        self.exporter.export(assembly_id, rendered, output)
        report_path = self.reporter.write(
            assembly_id,
            output,
            rendered,
            resolved_states,
        )
        return CompleteAssemblyReviewResult(
            assembly_id,
            output,
            len(rendered),
            tuple(selectors),
            report_path,
            rendered,
        )


__all__ = ["CompleteAssemblyReviewGenerator", "CompleteAssemblyReviewResult"]
