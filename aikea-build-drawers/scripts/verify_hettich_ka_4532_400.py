"""Scope: Expose exact 400 mm runner source/opening verification as a reusable local command."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path

from hettich_ka_4532_400_profile import HETTICH_KA_4532_400
from hettich_ka_4532_400_step_set import HettichKa4532FourHundredStepLoader
from hettich_ka_4532_400_opening_check import HettichKa4532FourHundredOpeningCheck


class VerifyKa4532FourHundredCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("source_directory", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args()
        step_set = HettichKa4532FourHundredStepLoader().load(args.source_directory)
        report = HettichKa4532FourHundredOpeningCheck().verify(step_set)
        report.update({"source": str(step_set.source.asset.path),
            "source_sha256": step_set.source.asset.sha256, "profile": asdict(HETTICH_KA_4532_400),
            "native_bounds_mm": asdict(step_set.source.bounds_mm),
            "native_member_roles": list(step_set.members), "source_geometry_modified": False,
            "native_fixed_to_moving_outer_face_spacing_mm": 12.5,
            "native_vs_nominal_contact_allowance_qualified": False})
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+"\n")
        print(json.dumps({"status": report["status"], "article": report["article"],
            "opening_count": report["opening_count"], "report": str(args.output),
            "manufacturing_authority": False}))


if __name__ == "__main__":
    VerifyKa4532FourHundredCommand().run()
