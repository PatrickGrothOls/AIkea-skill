"""Scope: Compose the intake stack and least-privilege runtime role."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aikea-review-unit/scripts"))
from cnc_deployment_config import CncDeploymentConfig
from api_resources import ApiResources
from identity_resources import IdentityResources
from storage_resources import StorageResources


class IntakeInfrastructure:
    NAME = "aikea-cnc-intake"

    def __init__(self, config: CncDeploymentConfig):
        self.config = config

    def template(self, artifact_key):
        resources = {**StorageResources().resources(), **IdentityResources().resources(), **ApiResources().resources()}
        resources.update({
            "Role": {"Type": "AWS::IAM::Role", "Properties": {
                "RoleName": self.NAME, "AssumeRolePolicyDocument": {"Version": "2012-10-17", "Statement": [{
                    "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]},
                "Policies": [{"PolicyName": "isolated-intake", "PolicyDocument": {
                    "Version": "2012-10-17", "Statement": self.permissions()}}]}},
            "Logs": {"Type": "AWS::Logs::LogGroup", "Properties": {
                "LogGroupName": "/aws/lambda/" + self.NAME, "RetentionInDays": 14}},
            "Gateway": {"Type": "AWS::Lambda::Function", "DependsOn": "Logs", "Properties": {
                "FunctionName": self.NAME, "Runtime": "python3.12", "Handler": "gateway.handler",
                "Role": {"Fn::GetAtt": ["Role", "Arn"]}, "MemorySize": 512, "Timeout": 28,
                "ReservedConcurrentExecutions": 2,
                "Code": {"S3Bucket": self.config.accepted_bucket, "S3Key": artifact_key},
                "Environment": {"Variables": {"QUARANTINE_BUCKET": {"Ref": "Quarantine"},
                                              "ACCEPTED_BUCKET": self.config.accepted_bucket, "USER_POOL": {"Ref": "UserPool"}}}}},
        })
        return {"AWSTemplateFormatVersion": "2010-09-09", "Description": "Private invitation-only AIkea CNC intake",
                "Resources": resources, "Outputs": {
                    "AccountId": {"Value": {"Ref": "AWS::AccountId"}},
                    "Region": {"Value": {"Ref": "AWS::Region"}},
                    "GatewayUrl": {"Value": {"Fn::GetAtt": ["Api", "ApiEndpoint"]}},
                    "ClientId": {"Value": {"Ref": "Client"}}, "UserPoolId": {"Value": {"Ref": "UserPool"}},
                    "LoginUrl": {"Value": {"Fn::Sub": "https://${Domain}.auth.${AWS::Region}.amazoncognito.com"}},
                    "QuarantineBucket": {"Value": {"Ref": "Quarantine"}}}}

    def permissions(self):
        accepted = "arn:aws:s3:::" + self.config.accepted_bucket
        return [
            {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"],
             "Resource": [{"Fn::Sub": "${Quarantine.Arn}/uploads/*"}, {"Fn::Sub": "${Quarantine.Arn}/reservations/*"},
                          {"Fn::Sub": "${Quarantine.Arn}/quotas/*"}]},
            {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": {"Fn::GetAtt": ["Quarantine", "Arn"]},
             "Condition": {"StringLike": {"s3:prefix": ["uploads/*", "reservations/*", "quotas/*"]}}},
            {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"], "Resource": [
                accepted + "/aikea/cnc-requests/*/" + name for name in ["source-repository.zip", "preview.png", "request.json", "ready.json"]]},
            {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": accepted,
             "Condition": {"StringLike": {"s3:prefix": ["aikea/cnc-requests/*"]}}},
            {"Effect": "Allow", "Action": ["cognito-idp:AdminGetUser"], "Resource": {"Fn::GetAtt": ["UserPool", "Arn"]}},
            {"Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
             "Resource": {"Fn::Sub": "arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/aikea-cnc-intake:*"}},
        ]
