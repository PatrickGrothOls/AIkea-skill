"""Scope: Verify fail-closed deployment configuration and unchanged IAM boundaries offline."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "aikea-review-unit/scripts"))
sys.path.insert(0, str(ROOT / "infra/cnc-intake"))
sys.path.insert(0, str(ROOT / "infra/cnc-requests"))
from cnc_deployment_config import CncDeploymentConfig
from deploy import CncDeployment
from deploy_intake import IntakeDeployment
from infrastructure import CncInfrastructure
from intake_infrastructure import IntakeInfrastructure
from hosted_quote_session import HostedQuoteSession
from test_cnc_package_validation import TestPackageValidation as PackageFixture


class TestDeploymentConfig:
    @pytest.fixture
    def target(self):
        return CncDeploymentConfig("222222222222", "eu-west-1", "test-private-cnc-bucket")

    @pytest.mark.parametrize("updates", [
        {"AccountId": ""}, {"AccountId": 123456789012}, {"AccountId": "123*"},
        {"Region": ""}, {"Region": "eu-west-1:malformed"}, {"Region": "cn-north-1"},
        {"AcceptedBucket": "*"}, {"AcceptedBucket": "bucket/key"}, {"AcceptedBucket": "UPPER"},
        {"Unexpected": "field"},
    ])
    def test_invalid_configuration_refused(self, tmp_path, updates):
        data = json.loads((ROOT / "infra/deployment.example.json").read_text()) | updates
        path = tmp_path / "config.json"
        path.write_text(json.dumps(data))
        with pytest.raises(ValueError):
            CncDeploymentConfig.from_file(path)

    @pytest.mark.parametrize("script", ["cnc-requests/deploy.py", "cnc-intake/deploy_intake.py"])
    def test_missing_cli_config_never_invokes_aws(self, tmp_path, script):
        # Empty PATH makes any accidental AWS invocation fail independently of local credentials.
        result = subprocess.run([sys.executable, str(ROOT / "infra" / script), "--apply", "--output", str(tmp_path)],
                                env={"PATH": ""}, capture_output=True)
        assert result.returncode != 0 and b"--config" in result.stderr
        assert not list(tmp_path.iterdir())

    def test_account_mismatch_stops_both_deployers_before_writes(self, tmp_path, target):
        notification = CncDeployment("test", tmp_path, target)
        notification.aws = Mock(return_value={"Account": "333333333333"})
        intake = IntakeDeployment(target)
        intake.aws = Mock(return_value=json.dumps({"Account": "333333333333"}))
        for deployment, invoke in [(notification, lambda: notification.deploy(tmp_path / "unused.json")),
                                   (intake, lambda: intake.apply(tmp_path))]:
            with pytest.raises(ValueError, match="Wrong AWS account"):
                invoke()
            deployment.aws.assert_called_once_with("sts", "get-caller-identity")

    def test_example_targets_refused_before_any_aws_call(self, tmp_path):
        config = CncDeploymentConfig.from_file(ROOT / "infra/deployment.example.json")
        for deployment in [CncDeployment("test", tmp_path, config), IntakeDeployment(config)]:
            deployment.aws = Mock()
            with pytest.raises(ValueError, match="Example configuration"):
                if isinstance(deployment, IntakeDeployment):
                    deployment.apply(tmp_path)
                else:
                    deployment.deploy(tmp_path / "unused.json")
            deployment.aws.assert_not_called()

    def test_notification_resources_remain_exactly_scoped(self, target):
        resources = CncInfrastructure(target).template("cnc-operator@example.com")["Resources"]
        conditions = resources["QueuePolicy"]["Properties"]["PolicyDocument"]["Statement"][0]["Condition"]
        assert conditions == {"ArnEquals": {"aws:SourceArn": "arn:aws:s3:::" + target.accepted_bucket},
                              "StringEquals": {"aws:SourceAccount": target.account_id}}
        role = resources["Role"]["Properties"]["Policies"][0]["PolicyDocument"]["Statement"]
        put = next(s for s in role if s["Action"] == ["s3:PutObject"])
        assert put["Resource"] == "arn:aws:s3:::" + target.accepted_bucket + "/aikea/cnc-requests/*/notified.json"

    @pytest.mark.parametrize("directory,class_name", [("cnc-intake", "DeploymentPermissions"),
                                                      ("cnc-requests", "NotificationPermissions")])
    def test_policy_generators_preserve_conditions(self, target, directory, class_name):
        spec = importlib.util.spec_from_file_location(directory, ROOT / "infra" / directory / "deployment_permissions.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if directory == "cnc-requests":
            statements = module.NotificationPermissions(target, "cnc-operator@example.com").policy()["Statement"]
            subscription = next(s for s in statements if s["Action"] == ["sns:Subscribe"])
            assert subscription["Condition"] == {"StringEquals": {"sns:Protocol": "email", "sns:Endpoint": "cnc-operator@example.com"}}
            triggers = [s for s in statements if "lambda:CreateEventSourceMapping" in s["Action"]]
            assert triggers[0]["Condition"]["ArnEquals"]["lambda:FunctionArn"].endswith(":function:aikea-cnc-requests")
        else:
            statements = module.DeploymentPermissions(target).policies()["deployment-policy.json"]["Statement"]
        passing = next(s for s in statements if "iam:PassRole" in s["Action"])
        assert passing["Condition"] == {"StringEquals": {"iam:PassedToService": "lambda.amazonaws.com"}}
        assert "*" not in passing["Resource"]
        assert not any("s3:DeleteObject" in s["Action"] for s in statements)

    def test_gateway_targets_require_configured_account_and_region(self):
        config = {"AccountId": "123456789012", "Region": "eu-west-1", "ClientId": "testclient",
                  "GatewayUrl": "https://test.execute-api.eu-west-1.amazonaws.com",
                  "LoginUrl": "https://aikea-cnc-123456789012.auth.eu-west-1.amazoncognito.com",
                  "QuarantineBucket": "aikea-cnc-intake-123456789012-eu-west-1"}
        for key in ["LoginUrl", "QuarantineBucket", "GatewayUrl"]:
            with pytest.raises(ValueError):
                HostedQuoteSession(PackageFixture().archive(), "b" * 64, config | {key: "https://attacker.invalid"})
        session = HostedQuoteSession(PackageFixture().archive(), "b" * 64, config, http=Mock(), login=Mock())
        with pytest.raises(ValueError, match="destination"):
            session._upload({"url": "https://wrong.s3.eu-west-1.amazonaws.com/"}, "source.zip", b"source")
        session.http.post.assert_not_called()

    def test_intake_outputs_supply_client_validation_fields(self, target):
        outputs = IntakeInfrastructure(target).template("test.zip")["Outputs"]
        assert outputs["AccountId"]["Value"] == {"Ref": "AWS::AccountId"}
        assert outputs["Region"]["Value"] == {"Ref": "AWS::Region"}
