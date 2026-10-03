"""Scope: Describe the dedicated CNC queue, worker and email subscription stack."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "aikea-review-unit/scripts"))
from cnc_deployment_config import CncDeploymentConfig


class CncInfrastructure:
    NAME = "aikea-cnc-requests"

    def __init__(self, config: CncDeploymentConfig):
        self.config = config

    def template(self, email):
        CncDeploymentConfig.validate_email(email)
        bucket_arn = f"arn:aws:s3:::{self.config.accepted_bucket}"
        role_policies = [
            {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": bucket_arn + "/aikea/cnc-requests/*"},
            {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": bucket_arn,
             "Condition": {"StringLike": {"s3:prefix": ["aikea/cnc-requests/*"]}}},
            {"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": bucket_arn + "/aikea/cnc-requests/*/notified.json"},
            {"Effect": "Allow", "Action": ["sns:Publish"], "Resource": {"Ref": "Topic"}},
            {"Effect": "Allow", "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
             "Resource": {"Fn::GetAtt": ["Queue", "Arn"]}},
            {"Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
             "Resource": f"arn:aws:logs:{self.config.region}:{self.config.account_id}:log-group:/aws/lambda/{self.NAME}:*"},
        ]
        resources = {
            "Topic": self._resource("SNS::Topic", {"TopicName": self.NAME}),
            "AlarmTopicPolicy": self._resource("SNS::TopicPolicy", {
                "Topics": [{"Ref": "Topic"}], "PolicyDocument": {"Version": "2012-10-17", "Statement": [{
                    "Effect": "Allow", "Principal": {"Service": "cloudwatch.amazonaws.com"}, "Action": "sns:Publish",
                    "Resource": {"Ref": "Topic"}, "Condition": {
                        "ArnEquals": {"aws:SourceArn": f"arn:aws:cloudwatch:{self.config.region}:{self.config.account_id}:alarm:{self.NAME}-failed-delivery"},
                        "StringEquals": {"aws:SourceAccount": self.config.account_id}}}]}}),
            "Email": self._resource("SNS::Subscription", {
                "TopicArn": {"Ref": "Topic"}, "Protocol": "email", "Endpoint": email}),
            "DeadLetters": self._resource("SQS::Queue", {
                "QueueName": self.NAME + "-dead-letters", "MessageRetentionPeriod": 1209600,
                "SqsManagedSseEnabled": True}),
            "Queue": self._resource("SQS::Queue", {
                "QueueName": self.NAME, "VisibilityTimeout": 180, "MessageRetentionPeriod": 1209600,
                "SqsManagedSseEnabled": True,
                "RedrivePolicy": {"deadLetterTargetArn": {"Fn::GetAtt": ["DeadLetters", "Arn"]}, "maxReceiveCount": 5}}),
            "QueuePolicy": self._resource("SQS::QueuePolicy", {
                "Queues": [{"Ref": "Queue"}], "PolicyDocument": {"Version": "2012-10-17", "Statement": [{
                    "Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"}, "Action": "sqs:SendMessage",
                    "Resource": {"Fn::GetAtt": ["Queue", "Arn"]}, "Condition": {
                        "ArnEquals": {"aws:SourceArn": bucket_arn}, "StringEquals": {"aws:SourceAccount": self.config.account_id}}}]}}),
            "Role": self._resource("IAM::Role", {
                "RoleName": self.NAME + "-worker", "AssumeRolePolicyDocument": {"Version": "2012-10-17", "Statement": [{
                    "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]},
                "Policies": [{"PolicyName": "cnc-request-notifications", "PolicyDocument": {
                    "Version": "2012-10-17", "Statement": role_policies}}]}),
            "Logs": self._resource("Logs::LogGroup", {
                "LogGroupName": "/aws/lambda/" + self.NAME, "RetentionInDays": 14}),
            "Worker": self._resource("Lambda::Function", {
                "FunctionName": self.NAME, "Runtime": "python3.12", "Handler": "index.handler", "Timeout": 30,
                "MemorySize": 128, "Role": {"Fn::GetAtt": ["Role", "Arn"]},
                "Code": {"ZipFile": (Path(__file__).parent / "notification_worker.py").read_text()},
                "Environment": {"Variables": {"BUCKET": self.config.accepted_bucket, "TOPIC": {"Ref": "Topic"}}}}),
            "Events": self._resource("Lambda::EventSourceMapping", {
                "EventSourceArn": {"Fn::GetAtt": ["Queue", "Arn"]}, "FunctionName": {"Ref": "Worker"},
                "BatchSize": 1, "ScalingConfig": {"MaximumConcurrency": 2}, "Enabled": True}),
            "FailedDeliveryAlarm": self._resource("CloudWatch::Alarm", {
                "AlarmName": self.NAME + "-failed-delivery", "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesVisible", "Statistic": "Maximum",
                "Period": 60, "EvaluationPeriods": 1, "Threshold": 0,
                "ComparisonOperator": "GreaterThanThreshold", "TreatMissingData": "notBreaching",
                "Dimensions": [{"Name": "QueueName", "Value": {"Fn::GetAtt": ["DeadLetters", "QueueName"]}}],
                "AlarmActions": [{"Ref": "Topic"}]}),
        }
        resources["Worker"]["DependsOn"] = "Logs"
        return {"AWSTemplateFormatVersion": "2010-09-09", "Description": "AIkea private CNC quote notifications",
                "Resources": resources, "Outputs": {
                    "QueueArn": {"Value": {"Fn::GetAtt": ["Queue", "Arn"]}},
                    "TopicArn": {"Value": {"Ref": "Topic"}}}}

    def notification(self, existing, queue_arn):
        configured = dict(existing)
        queues = [item for item in configured.get("QueueConfigurations", []) if item.get("Id") != self.NAME]
        queues.append({"Id": self.NAME, "QueueArn": queue_arn, "Events": ["s3:ObjectCreated:*"],
                       "Filter": {"Key": {"FilterRules": [
                           {"Name": "prefix", "Value": "aikea/cnc-requests/"},
                           {"Name": "suffix", "Value": "/ready.json"}]}}})
        configured["QueueConfigurations"] = queues
        return configured

    def _resource(self, kind, properties):
        return {"Type": "AWS::" + kind, "Properties": properties}
