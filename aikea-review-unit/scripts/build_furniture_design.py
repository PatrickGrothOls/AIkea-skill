"""Scope: Execute one authored furniture tree, check its solids and export its review."""

import argparse
import json
from pathlib import Path
from functools import partial
import re
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units/scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from assembly_tree_review_geometry import AssemblyTreeReviewGeometry  # noqa: E402
from cadquery_glb_exporter import CadQueryGlbExporter  # noqa: E402
from construction_tree_checker import ConstructionTreeChecker  # noqa: E402
from construction_requirement_checker import ConstructionRequirementChecker  # noqa: E402
from construction_input_fingerprint import ConstructionInputFingerprinter  # noqa: E402
from construction_feature_qualification import ConstructionFeatureQualification  # noqa: E402
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder  # noqa: E402
from construction_position_evidence import ConstructionPositionEvidence  # noqa: E402
from construction_position_inputs import ConstructionPositionInputs  # noqa: E402
from fabrication_closed_assembly_model import FabricationClosedAssemblyModel  # noqa: E402
from fabrication_assembly_review_record import FabricationAssemblyReviewRecord  # noqa: E402
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader  # noqa: E402
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver  # noqa: E402
from purchased_hardware_hydrator import PurchasedHardwareHydrator  # noqa: E402


class FurnitureDesignBuild:
    """Consume the same assembly contract for any project-authored furniture."""

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()

    def build(self, project_root: Path, assembly_id: str, output: Path, fabrication_review=False) -> dict:
        canonical = project_root / "assemblies/full_wardrobe_review.glb"
        if fabrication_review and output.resolve() != canonical.resolve():
            raise ValueError("fabrication review must use assemblies/full_wardrobe_review.glb")
        output.parent.mkdir(parents=True, exist_ok=True)
        report_path = output.with_suffix(".geometry-check.json")
        report_path.write_text(json.dumps({"status": "invalid", "fabrication_ready": False,
                                          "scope": "Build has not completed."}) + "\n")
        if not re.fullmatch(r"[a-z][a-z0-9_]*_[0-9]{2}", assembly_id):
            raise ValueError("use a stable assembly ID such as furniture_01")
        fingerprint = ConstructionInputFingerprinter()
        sources = fingerprint.source_inputs(project_root)
        built = self.loader.load_assembly(project_root, assembly_id)
        built = self.loader.runtime.execute(project_root, partial(self._hydrate, project_root, built))
        envelope, allowances, _ = ConstructionPositionInputs().read(project_root, assembly_id)
        if envelope is None:
            raise ValueError("the authored root builder must declare its measured ENVELOPE")
        visits = self.loader.walk(project_root, built)
        paths = tuple(item.path for item in visits)
        if len(paths) != len(set(paths)):
            raise ValueError("assembly tree paths must be unique")
        parts = AssemblyTreeReviewGeometry().build(visits, {})
        position = ConstructionPositionEvidence().write(project_root, visits, envelope, allowances)
        report = dict(position["geometry"])
        report["status"] = position["status"]
        report["contact_evidence_problems"] = position["contact_evidence_problems"]
        evidence = FabricationTreeEvidenceBuilder().build(visits)
        qualified, features = ConstructionFeatureQualification().resolve(project_root, evidence, visits)
        checks = ConstructionTreeChecker().check(visits, qualified) + ConstructionRequirementChecker().check(visits, features)
        report["construction_sha256"] = fingerprint.build(project_root, visits)
        report["construction_checks"] = [check.as_dict() for check in checks]
        report["construction_status"] = "verified_operations" if all(check.passed for check in checks) else "incomplete"
        report["assembly_id"] = assembly_id
        report["assembly_count"] = sum(
            type(item).__name__ == "AssemblyTreeAssembly" for item in visits
        )
        if not report["invalid_solids"]:
            if fabrication_review:
                FabricationClosedAssemblyModel().write(visits, output)
            else:
                CadQueryGlbExporter().export(assembly_id, parts, output)
            report["glb"] = str(output)
        report["geometry_check"] = str(report_path)
        fingerprint.require_unchanged_sources(project_root, sources)
        if fabrication_review and report["status"] == "valid":
            record = FabricationAssemblyReviewRecord().write_proposal(project_root, output, report["construction_sha256"])
            report["review_record"] = str(record)
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        return report

    def _hydrate(self, project_root, built):
        return PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate(project_root, built)


class FurnitureDesignBuildCommand:
    """Expose project execution and evidence paths without imposing a design type."""

    def run(self) -> int:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        parser.add_argument("--assembly", default="furniture_01")
        parser.add_argument("--output", type=Path)
        parser.add_argument("--fabrication-review", action="store_true")
        args = parser.parse_args()
        project = args.project.resolve()
        default_output = project / ("assemblies/full_wardrobe_review.glb" if args.fabrication_review else f"reviews/{args.assembly}.glb")
        output = args.output or default_output
        report = FurnitureDesignBuild().build(project, args.assembly, output.resolve(), args.fabrication_review)
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "valid" else 2


if __name__ == "__main__":
    raise SystemExit(FurnitureDesignBuildCommand().run())
