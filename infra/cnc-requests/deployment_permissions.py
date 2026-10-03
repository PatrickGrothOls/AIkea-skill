"""Scope: Render the notification IAM policy without widening its restrictions."""

import argparse
import json
from pathlib import Path
from string import Template

from infrastructure import CncDeploymentConfig


class NotificationPermissions:
    def __init__(self, config, email):
        self.config = config
        self.email = CncDeploymentConfig.validate_email(email)

    def policy(self):
        source = Path(__file__).with_name("deployment-policy.template.json").read_text()
        return json.loads(Template(source).substitute(
            ACCOUNT_ID=self.config.account_id, REGION=self.config.region,
            ACCEPTED_BUCKET=self.config.accepted_bucket, NOTIFICATION_EMAIL=self.email))

    def write(self, output):
        policy = self.policy()
        if len(json.dumps(policy, separators=(",", ":"))) > 6144:
            raise ValueError("Policy exceeds managed-policy limit.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(policy, indent=2) + "\n")


class NotificationPermissionsCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--config", type=Path, required=True)
        parser.add_argument("--email", required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args()
        NotificationPermissions(CncDeploymentConfig.from_file(args.config), args.email).write(args.output)


if __name__ == "__main__":
    NotificationPermissionsCommand().run()
