"""Scope: Validate explicit, operator-owned CNC AWS target configuration."""

from dataclasses import dataclass
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class CncDeploymentConfig:
    account_id: str
    region: str
    accepted_bucket: str

    def __post_init__(self):
        self.validate_identity(self.account_id, self.region)
        if (not isinstance(self.accepted_bucket, str)
                or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}[a-z0-9]", self.accepted_bucket)
                or self.accepted_bucket.startswith(("xn--", "sthree-", "amzn-s3-demo-"))
                or self.accepted_bucket.endswith(("-s3alias", "--ol-s3", "--x-s3", "--table-s3"))):
            raise ValueError("AcceptedBucket must be a valid DNS-safe S3 bucket name without dots.")

    @staticmethod
    def validate_identity(account_id, region):
        if not isinstance(account_id, str) or not re.fullmatch(r"[0-9]{12}", account_id):
            raise ValueError("AccountId must be an explicit 12-digit string.")
        # Only the commercial AWS partition is supported by these ARN/endpoint builders.
        if not isinstance(region, str) or not re.fullmatch(r"(?:af|ap|ca|eu|il|me|mx|sa|us)-(?:central|east|west|north|south|northeast|southeast)-[1-9]", region):
            raise ValueError("Region must be a commercial AWS region identifier.")

    @staticmethod
    def validate_email(email):
        if not isinstance(email, str) or not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", email):
            raise ValueError("An explicit notification email address is required.")
        return email

    @classmethod
    def from_file(cls, filename):
        data = json.loads(Path(filename).read_text())
        if not isinstance(data, dict) or set(data) != {"AccountId", "Region", "AcceptedBucket"}:
            raise ValueError("Configuration requires only AccountId, Region and AcceptedBucket.")
        return cls(data["AccountId"], data["Region"], data["AcceptedBucket"])

    def require_live_target(self):
        if (self.account_id in {"123456789012", "000000000000", "111111111111"}
                or self.accepted_bucket.startswith("example-")):
            raise ValueError("Example configuration cannot be used for AWS writes.")
