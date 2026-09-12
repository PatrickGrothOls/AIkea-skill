"""Scope: Read current saved geometry eligibility for a visual fabrication decision."""

import json


class ConstructionReviewEligibility:
    """Validate the saved position record without rerunning CAD or the final readiness gate."""

    REPORT = "assemblies/construction-position-check.json"

    def allows(self, root, construction_sha256):
        # The report is an external file boundary and can be absent or mid-regeneration.
        try:
            data = json.loads((root / self.REPORT).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return False
        return (isinstance(data, dict) and data.get("schema_version") == 2
                and data.get("status") == "valid"
                and isinstance(construction_sha256, str) and bool(construction_sha256)
                and data.get("construction_sha256") == construction_sha256)
