"""Scope: Prepare reviewable, resource-scoped deployment policy documents."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aikea-review-unit/scripts"))
from cnc_deployment_config import CncDeploymentConfig


class DeploymentPermissions:
    NAME = "aikea-cnc-intake"

    def __init__(self, config: CncDeploymentConfig):
        self.config = config

    def policies(self):
        account, region, name = self.config.account_id, self.config.region, self.NAME
        bucket = f"arn:aws:s3:::{name}-{account}-{region}"
        role = f"arn:aws:iam::{account}:role/{name}"
        core = [
            self.allow(["s3:CreateBucket", "s3:GetBucketLocation", "s3:GetBucketPolicy", "s3:PutBucketPolicy",
                        "s3:DeleteBucketPolicy", "s3:GetBucketPublicAccessBlock", "s3:PutBucketPublicAccessBlock",
                        "s3:GetBucketOwnershipControls", "s3:PutBucketOwnershipControls", "s3:GetEncryptionConfiguration",
                        "s3:PutEncryptionConfiguration", "s3:GetLifecycleConfiguration", "s3:PutLifecycleConfiguration",
                        "s3:GetBucketTagging", "s3:PutBucketTagging", "s3:GetBucketVersioning"], bucket),
            self.allow(["s3:PutObject", "s3:GetObject"],
                       f"arn:aws:s3:::{self.config.accepted_bucket}/aikea/deploy/cnc-intake/*"),
            self.allow(["iam:CreateRole", "iam:GetRole", "iam:DeleteRole", "iam:PutRolePolicy", "iam:GetRolePolicy",
                        "iam:DeleteRolePolicy", "iam:UpdateAssumeRolePolicy", "iam:ListRolePolicies", "iam:ListAttachedRolePolicies", "iam:TagRole", "iam:UntagRole"], role),
            self.allow(["iam:PassRole"], role, {"StringEquals": {"iam:PassedToService": "lambda.amazonaws.com"}}),
            self.allow(["lambda:CreateFunction", "lambda:GetFunction", "lambda:GetFunctionConfiguration", "lambda:UpdateFunctionCode",
                        "lambda:UpdateFunctionConfiguration", "lambda:DeleteFunction", "lambda:PutFunctionConcurrency",
                        "lambda:GetFunctionConcurrency", "lambda:DeleteFunctionConcurrency", "lambda:AddPermission",
                        "lambda:RemovePermission", "lambda:GetPolicy", "lambda:TagResource", "lambda:UntagResource", "lambda:ListTags"],
                       f"arn:aws:lambda:{region}:{account}:function:{name}"),
            self.allow(["logs:CreateLogGroup", "logs:DeleteLogGroup", "logs:PutRetentionPolicy", "logs:DeleteRetentionPolicy",
                        "logs:TagResource", "logs:UntagResource", "logs:ListTagsForResource"],
                       [f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/{name}",
                        f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/{name}:*"]),
            self.allow(["logs:DescribeLogGroups", "cloudformation:ValidateTemplate", "cloudformation:GetTemplateSummary"], "*"),
            self.allow(["cloudformation:CreateStack", "cloudformation:UpdateStack", "cloudformation:DeleteStack",
                        "cloudformation:DescribeStacks", "cloudformation:DescribeStackEvents", "cloudformation:GetTemplate",
                        "cloudformation:CreateChangeSet", "cloudformation:DescribeChangeSet", "cloudformation:ExecuteChangeSet",
                        "cloudformation:DeleteChangeSet"], [f"arn:aws:cloudformation:{region}:{account}:stack/{name}/*",
                                                           f"arn:aws:cloudformation:{region}:{account}:changeSet/awscli-cloudformation-package-deploy-*/*"]),
        ]
        tag = {"StringEquals": {"aws:ResourceTag/Service": name}}
        request_tag = {"StringEquals": {"aws:RequestTag/Service": name}}
        identity = [
            self.allow(["cognito-idp:CreateUserPool"], "*", request_tag),
            self.allow(["cognito-idp:TagResource"], f"arn:aws:cognito-idp:{region}:{account}:userpool/*", request_tag),
            self.allow(["cognito-idp:DescribeUserPool", "cognito-idp:UpdateUserPool", "cognito-idp:DeleteUserPool",
                        "cognito-idp:CreateUserPoolClient", "cognito-idp:DescribeUserPoolClient", "cognito-idp:UpdateUserPoolClient",
                        "cognito-idp:DeleteUserPoolClient", "cognito-idp:CreateResourceServer", "cognito-idp:DescribeResourceServer",
                        "cognito-idp:UpdateResourceServer", "cognito-idp:DeleteResourceServer", "cognito-idp:CreateUserPoolDomain",
                        "cognito-idp:UpdateUserPoolDomain", "cognito-idp:DeleteUserPoolDomain", "cognito-idp:ListTagsForResource"],
                       f"arn:aws:cognito-idp:{region}:{account}:userpool/*", tag),
            self.allow(["cognito-idp:DescribeUserPoolDomain"], "*"),
            self.allow(["apigateway:POST"], f"arn:aws:apigateway:{region}::/apis", request_tag),
            self.allow(["apigateway:POST"], [
                f"arn:aws:apigateway:{region}::/tags/arn%3Aaws%3Aapigateway%3A{region}%3A%3A%2Fv2%2Fapis%2F*",
                f"arn:aws:apigateway:{region}::/tags/arn%3Aaws%3Aapigateway%3A{region}%3A%3A%2Fapis%2F*"], request_tag),
            self.allow(["apigateway:GET", "apigateway:POST", "apigateway:PATCH", "apigateway:DELETE", "apigateway:PUT"],
                       f"arn:aws:apigateway:{region}::/apis/*", tag),
        ]
        return {"deployment-policy.json": {"Version": "2012-10-17", "Statement": core + identity},
                "deployment-core-policy.json": {"Version": "2012-10-17", "Statement": core},
                "deployment-identity-policy.json": {"Version": "2012-10-17", "Statement": identity}}

    def allow(self, actions, resources, condition=None):
        statement = {"Effect": "Allow", "Action": actions, "Resource": resources}
        if condition:
            statement["Condition"] = condition
        return statement

    def write(self, output):
        for name, policy in self.policies().items():
            compact = json.dumps(policy, separators=(",", ":"))
            if len(compact) > 6144:
                raise ValueError("Policy exceeds managed-policy limit.")
            (output / name).write_text(json.dumps(policy, indent=2) + "\n")


class DeploymentPermissionsCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--config", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args()
        config = CncDeploymentConfig.from_file(args.config)
        args.output.mkdir(parents=True, exist_ok=True)
        DeploymentPermissions(config).write(args.output)


if __name__ == "__main__":
    DeploymentPermissionsCommand().run()
