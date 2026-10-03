"""Scope: Remove cabinet lighting from composition while retaining its saved plan."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aikea-build-units/scripts"))

from cabinet_feature_manifest import CabinetFeatureManifest


class RemoveCabinetLightingCommand:
    """Leave all other features and source geometry untouched."""

    def run(self) -> int:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly-id", required=True)
        arguments = parser.parse_args()
        try:
            changed = CabinetFeatureManifest().unregister(
                arguments.aikea_yaml.parent, arguments.assembly_id, "lighting.feature"
            )
        except (OSError, ValueError) as error:
            print(json.dumps({"status": "invalid", "problem": str(error)}))
            return 2
        print(json.dumps({
            "status": "removed" if changed else "not_registered",
            "assembly_id": arguments.assembly_id,
            "next": "Rebuild complete_builder in a fresh process and refresh exports and quote.",
        }))
        return 0


if __name__ == "__main__":
    raise SystemExit(RemoveCabinetLightingCommand().run())
