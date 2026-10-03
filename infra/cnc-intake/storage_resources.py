"""Scope: Isolate private, temporary external uploads from accepted customer requests."""


class StorageResources:
    def resources(self):
        return {
            "Quarantine": {"Type": "AWS::S3::Bucket", "DeletionPolicy": "Retain", "UpdateReplacePolicy": "Retain",
                           "Properties": {
                "BucketName": {"Fn::Sub": "aikea-cnc-intake-${AWS::AccountId}-${AWS::Region}"},
                "PublicAccessBlockConfiguration": {"BlockPublicAcls": True, "IgnorePublicAcls": True,
                                                   "BlockPublicPolicy": True, "RestrictPublicBuckets": True},
                "OwnershipControls": {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]},
                "BucketEncryption": {"ServerSideEncryptionConfiguration": [{
                    "ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]},
                "LifecycleConfiguration": {"Rules": [
                    {"Id": "temporary-uploads", "Status": "Enabled", "Prefix": "uploads/", "ExpirationInDays": 1},
                    {"Id": "reservations", "Status": "Enabled", "Prefix": "reservations/", "ExpirationInDays": 7},
                    {"Id": "quotas", "Status": "Enabled", "Prefix": "quotas/", "ExpirationInDays": 7}]}}},
            "QuarantinePolicy": {"Type": "AWS::S3::BucketPolicy", "Properties": {
                "Bucket": {"Ref": "Quarantine"}, "PolicyDocument": {"Version": "2012-10-17", "Statement": [{
                    "Effect": "Deny", "Principal": "*", "Action": "s3:*",
                    "Resource": [{"Fn::GetAtt": ["Quarantine", "Arn"]}, {"Fn::Sub": "${Quarantine.Arn}/*"}],
                    "Condition": {"Bool": {"aws:SecureTransport": "false"}}}]}}},
        }
