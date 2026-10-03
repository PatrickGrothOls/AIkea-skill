"""Scope: Prepare reproducible intake artifacts; deploy only with explicit --apply."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from intake_infrastructure import IntakeInfrastructure, CncDeploymentConfig


class IntakeDeployment:
    RUNTIME = ("gateway.py", "intake_contract.py", "intake_storage.py", "intake_reservations.py",
               "intake_acceptance.py", "package_validation.py", "preview_validation.py")

    def __init__(self, config, profile="default"):
        self.config, self.profile = config, profile

    def prepare(self, output):
        output.mkdir(parents=True, exist_ok=True)
        here = Path(__file__).resolve().parent
        shared = here.parents[1] / "aikea-review-unit/scripts"
        sources = [here / name for name in self.RUNTIME] + [shared / name for name in ["source_package_rules.py", "quote_preferences.py"]]
        archive_path = output / "intake.zip"
        with ZipFile(archive_path, "w") as archive:
            for path in sorted(sources):
                entry = ZipInfo(path.name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                archive.writestr(entry, path.read_bytes())
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        key = f"aikea/deploy/cnc-intake/{digest}.zip"
        template = output / "template.json"
        template.write_text(json.dumps(IntakeInfrastructure(self.config).template(key), indent=2))
        return archive_path, key, template

    def apply(self, output):
        self.config.require_live_target()
        archive, key, template = self.prepare(output)
        identity = json.loads(self.aws("sts", "get-caller-identity"))
        if identity["Account"] != self.config.account_id:
            raise ValueError("Wrong AWS account; deployment refused.")
        self.aws("cloudformation", "validate-template", "--template-body", "file://" + str(template))
        self.aws("s3api", "put-object", "--bucket", self.config.accepted_bucket, "--key", key,
                 "--body", str(archive), "--content-type", "application/zip", "--checksum-algorithm", "SHA256")
        self.aws("cloudformation", "deploy", "--stack-name", IntakeInfrastructure.NAME,
                 "--template-file", str(template), "--capabilities", "CAPABILITY_NAMED_IAM", "--no-fail-on-empty-changeset")
        result = json.loads(self.aws("cloudformation", "describe-stacks", "--stack-name", IntakeInfrastructure.NAME))
        values = {item["OutputKey"]: item["OutputValue"] for item in result["Stacks"][0]["Outputs"]}
        (output / "outputs.json").write_text(json.dumps(values, indent=2))
        print(json.dumps(values, indent=2))

    def aws(self, *arguments):
        return subprocess.check_output(["aws", *arguments, "--profile", self.profile, "--region", self.config.region,
                                        "--output", "json", "--no-cli-pager"], text=True)


class IntakeDeploymentCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--config", type=Path, required=True)
        parser.add_argument("--profile", default="default")
        parser.add_argument("--output", type=Path, required=True)
        parser.add_argument("--apply", action="store_true")
        args = parser.parse_args()
        deployment = IntakeDeployment(CncDeploymentConfig.from_file(args.config), args.profile)
        if args.apply:
            deployment.apply(args.output.resolve())
        else:
            deployment.prepare(args.output.resolve())
            print("Prepared intake.zip and template.json; no AWS changes.")


if __name__ == "__main__":
    IntakeDeploymentCommand().run()
