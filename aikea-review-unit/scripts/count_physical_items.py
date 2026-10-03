"""Scope: Export a draft item inventory from a generated project's closed tree."""

import argparse
import json
from pathlib import Path
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from cadquery_runtime import CadQueryRuntime


class CountPhysicalItemsCommand:
    """Write counting evidence without changing any fabrication BOM or design."""

    def run(self, project_root: Path, assembly_id: str = "wardrobe_01") -> int:
        from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
        from physical_item_counter import PhysicalItemCounter

        output = project_root / "manufacturing/item-counts.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        # Revoke an older result before executing builders, which can fail independently.
        output.write_text(json.dumps(dict(status="invalid", reason="Counting has not completed for this run.")), encoding="utf-8")
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(project_root, assembly_id)
        report = PhysicalItemCounter().count(loader.walk(project_root, built))
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(dict(report=str(output), status=report["status"],
                              totals=report["totals"], unresolved=len(report["unresolved"])), indent=2))
        return 2 if report["unresolved"] else 0


# This function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(description="Count physical items in a generated AIkea project.")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--assembly", default="wardrobe_01", help="Canonical closed assembly to inventory.")
    arguments = parser.parse_args()
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
    return CountPhysicalItemsCommand().run(arguments.project_root.resolve(), arguments.assembly)


if __name__ == "__main__":
    raise SystemExit(main())
