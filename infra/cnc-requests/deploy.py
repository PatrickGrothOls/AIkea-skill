"""Scope: Prepare or deploy CNC notifications while preserving existing bucket hooks."""

import argparse
import json
from pathlib import Path
import subprocess

from infrastructure import CncInfrastructure, CncDeploymentConfig


class CncDeployment:
    def __init__(self, profile, output, config):
        self.profile, self.output = profile, output
        self.infrastructure = CncInfrastructure(config)

    def prepare(self, email):
        self.output.mkdir(parents=True, exist_ok=True)
        template = self.output / "cloudformation.json"
        template.write_text(json.dumps(self.infrastructure.template(email), indent=2) + "\n")
        return template

    def deploy(self, template):
        self.infrastructure.config.require_live_target()
        identity = self.aws("sts", "get-caller-identity")
        if identity["Account"] != self.infrastructure.config.account_id:
            raise ValueError("Wrong AWS account; deployment stopped.")
        self.aws("cloudformation", "deploy", "--stack-name", self.infrastructure.NAME,
                 "--template-file", str(template), "--capabilities", "CAPABILITY_NAMED_IAM",
                 "--no-fail-on-empty-changeset", structured=False)
        stack = self.aws("cloudformation", "describe-stacks", "--stack-name", self.infrastructure.NAME)
        outputs = {item["OutputKey"]: item["OutputValue"] for item in stack["Stacks"][0]["Outputs"]}
        existing = self.aws("s3api", "get-bucket-notification-configuration", "--bucket", self.infrastructure.config.accepted_bucket)
        (self.output / "previous-bucket-notifications.json").write_text(json.dumps(existing, indent=2) + "\n")
        updated = self.infrastructure.notification(existing, outputs["QueueArn"])
        notification_file = self.output / "bucket-notifications.json"
        notification_file.write_text(json.dumps(updated, indent=2) + "\n")
        # Re-read to avoid overwriting changes made during this deployment.
        if existing != self.aws("s3api", "get-bucket-notification-configuration", "--bucket", self.infrastructure.config.accepted_bucket):
            raise RuntimeError("Bucket notifications changed concurrently; rerun to merge the latest settings.")
        self.aws("s3api", "put-bucket-notification-configuration", "--bucket", self.infrastructure.config.accepted_bucket,
                 "--notification-configuration", "file://" + str(notification_file.resolve()))
        print(json.dumps({"status": "deployed_email_confirmation_required", **outputs}))

    def aws(self, *arguments, structured=True):
        command = ["aws", *arguments, "--profile", self.profile, "--region", self.infrastructure.config.region,
                   "--output", "json", "--no-cli-pager"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr.strip() or error.stdout.strip()) from error
        return json.loads(result.stdout or "{}") if structured else result.stdout


class CncDeploymentCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--config", type=Path, required=True)
        parser.add_argument("--email", required=True)
        parser.add_argument("--profile", default="default")
        parser.add_argument("--output", type=Path, required=True)
        parser.add_argument("--apply", action="store_true")
        args = parser.parse_args()
        deployment = CncDeployment(args.profile, args.output, CncDeploymentConfig.from_file(args.config))
        template = deployment.prepare(args.email)
        if args.apply:
            deployment.deploy(template)
        else:
            print(f"Prepared {template}; AWS unchanged.")


if __name__ == "__main__":
    CncDeploymentCommand().run()
