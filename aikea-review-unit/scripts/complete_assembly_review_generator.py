"""Scope: Export any recursively composed assembly through registered reviews."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_feature_review import AssemblyFeatureReviewContext
from assembly_review_plan_composer import AssemblyReviewPlanComposer
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from unit_mockup import UnitMockupInputError


@dataclass(frozen=True, slots=True)
class CompleteAssemblyReviewResult:
    """Report the exported tree and every available feature-state selector."""

    assembly_id: str
    glb_path: Path
    part_count: int
    feature_selectors: tuple[str, ...]


class CompleteAssemblyReviewGenerator:
    """Traverse, pose, hydrate, and export one arbitrary generated tree."""

    def __init__(
        self,
        loader=None,
        hydrator=None,
        geometry=None,
        exporter=None,
        composer=None,
    ) -> None:
        self.loader = loader or GeneratedAssemblyBuilderLoader()
        self.hydrator = hydrator or PurchasedHardwareHydrator(
            ProjectHardwareGeometryResolver()
        )
        self.geometry = geometry or AssemblyTreeReviewGeometry()
        self.exporter = exporter or CadQueryGlbExporter()
        self.composer = composer or AssemblyReviewPlanComposer()

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
        for item in visits:
            if type(item).__name__ != "AssemblyTreeAssembly":
                continue
            owner_id = item.assembly.spec.assembly_id
            for registration in self.loader.load_review_features(
                project_root, item.path
            ):
                selector = "/".join((*item.path, registration.feature_id))
                selectors.append(selector)
                context = AssemblyFeatureReviewContext(
                    project_root,
                    item.path,
                    item.assembly,
                )
                plans.append(
                    registration.feature.plan(
                        context,
                        requested.get(selector, "closed"),
                    )
                )
        unknown = sorted(set(requested) - set(selectors))
        if unknown:
            raise UnitMockupInputError(
                ["unknown assembly feature state: " + ", ".join(unknown)]
            )
        plan = self.composer.compose(tuple(plans))
        hydrated = self.hydrator.hydrate(project_root, built, plan.hides)
        rendered = self.geometry.build(
            self.loader.walk(project_root, hydrated),
            {},
            plan,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        self.exporter.export(assembly_id, rendered, output)
        return CompleteAssemblyReviewResult(
            assembly_id,
            output,
            len(rendered),
            tuple(selectors),
        )


__all__ = ["CompleteAssemblyReviewGenerator", "CompleteAssemblyReviewResult"]
