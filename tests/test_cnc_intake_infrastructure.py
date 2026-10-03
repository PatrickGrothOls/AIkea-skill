"""Scope: Verify closed API routes, private storage and deployable runtime packaging."""

import json
from pathlib import Path
import sys
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "infra/cnc-intake"))
from intake_infrastructure import IntakeInfrastructure
from deploy_intake import IntakeDeployment
from deployment_permissions import DeploymentPermissions

from cnc_deployment_config import CncDeploymentConfig

EXAMPLE_CONFIG = CncDeploymentConfig("123456789012", "eu-north-1", "example-aikea-cnc-requests")


class TestIntakeInfrastructure:
    def test_every_route_requires_scoped_jwt(self):
        resources = IntakeInfrastructure(EXAMPLE_CONFIG).template("artifact.zip")["Resources"]
        routes = [r["Properties"] for r in resources.values() if r["Type"] == "AWS::ApiGatewayV2::Route"]
        assert len(routes) == 2
        assert all(r["AuthorizationType"] == "JWT" and r["AuthorizationScopes"] == ["aikea/submit"] for r in routes)
        assert resources["UserPool"]["Properties"]["AdminCreateUserConfig"]["AllowAdminCreateUserOnly"]
        assert not resources["Client"]["Properties"]["GenerateSecret"]
        assert resources["Client"]["Properties"]["AllowedOAuthFlows"] == ["code"]

    def test_quarantine_is_private_temporary_and_not_notification_source(self):
        resources = IntakeInfrastructure(EXAMPLE_CONFIG).template("artifact.zip")["Resources"]
        bucket = resources["Quarantine"]["Properties"]
        assert all(bucket["PublicAccessBlockConfiguration"].values())
        assert "NotificationConfiguration" not in bucket
        assert "CorsConfiguration" not in bucket
        assert bucket["LifecycleConfiguration"]["Rules"][0]["ExpirationInDays"] == 1
        permissions = json.dumps(IntakeInfrastructure(EXAMPLE_CONFIG).permissions())
        assert "sns:Publish" not in permissions and "s3:DeleteObject" not in permissions
        assert "notified.json" not in permissions

    def test_artifact_is_reproducible_and_has_all_shared_runtime_modules(self, tmp_path):
        deployment = IntakeDeployment(EXAMPLE_CONFIG)
        archive, key, template = deployment.prepare(tmp_path)
        first = archive.read_bytes()
        assert deployment.prepare(tmp_path)[1] == key
        assert archive.read_bytes() == first
        with ZipFile(archive) as package:
            assert {"gateway.py", "source_package_rules.py", "quote_preferences.py", "package_validation.py"} <= set(package.namelist())
            for name in package.namelist():
                compile(package.read(name), name, "exec")
        assert json.loads(template.read_text())["Resources"]["Gateway"]["Properties"]["Code"]["S3Key"] == key

    def test_managed_policies_fit_and_role_passing_is_service_bound(self):
        policies = DeploymentPermissions(EXAMPLE_CONFIG).policies()
        assert all(len(json.dumps(p, separators=(",", ":"))) <= 6144 for p in policies.values())
        core = policies["deployment-core-policy.json"]["Statement"]
        passing = next(s for s in core if "iam:PassRole" in s["Action"])
        assert passing["Resource"].endswith(":role/aikea-cnc-intake")
        assert passing["Condition"]["StringEquals"]["iam:PassedToService"] == "lambda.amazonaws.com"

    def test_combined_policy_allows_tagging_only_intake_service(self):
        policy = DeploymentPermissions(EXAMPLE_CONFIG).policies()["deployment-policy.json"]
        tags = next(s for s in policy["Statement"] if "/tags/" in str(s["Resource"]))
        assert tags["Action"] == ["apigateway:POST"]
        assert tags["Condition"] == {"StringEquals": {"aws:RequestTag/Service": "aikea-cnc-intake"}}
        assert all("%2Fapis%2F" in arn for arn in tags["Resource"])

    def test_checked_in_policies_are_exact_generated_safe_examples(self):
        for name, policy in DeploymentPermissions(EXAMPLE_CONFIG).policies().items():
            path = Path(__file__).resolve().parents[1] / "infra/cnc-intake" / name
            assert json.loads(path.read_text()) == policy
