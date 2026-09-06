"""Scope: Generate local unit folders from one completed aikea.yaml project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

AIKEA_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea" / "scripts"
sys.path.insert(0, str(AIKEA_SCRIPTS))

from assembly_taxonomy import AssemblyTaxonomyInputError  # noqa: E402
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator  # noqa: E402
from assembly_taxonomy_writer import AssemblyTaxonomyConflict  # noqa: E402
from generated_file_record import GeneratedFileRecordError  # noqa: E402
from overall_wardrobe_inputs import OverallWardrobeInputError  # noqa: E402


class UnitTaxonomyCommand:
    """Own project file input and JSON terminal output for taxonomy generation."""

    def run(self, path: Path) -> int:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise AssemblyTaxonomyInputError(["aikea.yaml must contain an object"])
            taxonomy = AssemblyTaxonomyGenerator().generate(data, path.parent)
        except (OSError, yaml.YAMLError) as error:
            return self._invalid([str(error)])
        except (AssemblyTaxonomyInputError, OverallWardrobeInputError) as error:
            return self._invalid(list(error.problems))
        except AssemblyTaxonomyConflict as error:
            return self._invalid([str(error)])
        except GeneratedFileRecordError as error:
            return self._invalid([str(error)])
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assemblies": [
                        {
                            "id": item.assembly_id,
                            "path": f"assemblies/{item.assembly_id}",
                        }
                        for item in taxonomy.assemblies
                    ],
                },
                indent=2,
            )
        )
        return 0

    def _invalid(self, problems: list[str]) -> int:
        print(json.dumps({"status": "invalid", "problems": problems}, indent=2))
        return 2


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate local AIkea unit folders from a completed project."
    )
    parser.add_argument("aikea_yaml", type=Path)
    return UnitTaxonomyCommand().run(parser.parse_args().aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
