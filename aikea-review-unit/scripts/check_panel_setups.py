"""Scope: Save a non-authorizing one-face setup audit for a complete built tree."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aikea-build-units/scripts"))

from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from construction_input_fingerprint import ConstructionInputFingerprinter
from panel_setup_checker import PanelSetupChecker


class PanelSetupAuditCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        parser.add_argument("--assembly", required=True)
        args = parser.parse_args()
        project = args.project.resolve()
        output = project / "reviews/panel-setup-audit.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"status": "not_completed", "machining_ready": False}) + "\n")
        fingerprint = ConstructionInputFingerprinter()
        sources = fingerprint.source_inputs(project)
        loader = GeneratedAssemblyBuilderLoader()
        root = loader.load_assembly(project, args.assembly)
        results = []
        visits = loader.walk(project, root)
        for visit in visits:
            if type(visit).__name__ == "AssemblyTreeAssembly":
                report = PanelSetupChecker().check(visit.assembly)
                results.append({"path": list(visit.path), **report})
        rows = [part for result in results for part in result["parts"]]
        summary = {
            "status": "compatible" if all(row["allowed_faces"] for row in rows) else "conflict_or_unsupported",
            "machining_ready": False,
            "construction_sha256": fingerprint.build(project, visits),
            "part_count": len(rows),
            "conflicts": ["/".join(result["path"] + [part["part_id"]]) for result in results
                          for part in result["parts"] if not part["allowed_faces"]],
            "scope": "Declared operation entry faces only; consult geometry, requirements and CAM evidence separately",
        }
        fingerprint.require_unchanged_sources(project, sources)
        output.write_text(json.dumps({**summary, "assemblies": results}, indent=2) + "\n")
        print(json.dumps({**summary, "report": str(output)}, indent=2))
        return 0 if summary["status"] == "compatible" else 2


if __name__ == "__main__":
    raise SystemExit(PanelSetupAuditCommand().run())
