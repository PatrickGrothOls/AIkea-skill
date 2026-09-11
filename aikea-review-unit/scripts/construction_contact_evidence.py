"""Scope: Authorize bounded contact declarations only from their current feature evidence."""

from dataclasses import asdict
import json

from construction_feature_qualification import ConstructionFeatureQualification


class ConstructionContactEvidence:
    """Match the exact region and pair, not only a passing feature or hardware family."""

    KEYS = {"allowance_id", "subject_paths", "minimum_mm", "maximum_mm",
            "maximum_volume_mm3", "evidence_feature", "basis"}

    def records(self, allowances):
        return json.loads(json.dumps([asdict(allowance) for allowance in allowances], allow_nan=False))

    def check(self, root, tree, visits, allowances):
        if not isinstance(allowances, list):
            return ("contact allowances must be a list",)
        records = {f"{scope.owner_path}/feature:{scope.module}": (data, subjects)
                   for scope, data, subjects in ConstructionFeatureQualification().current_scopes(root, tree, visits)}
        problems = []
        for allowance in allowances:
            if not self._valid_record(allowance):
                problems.append("contact allowance has invalid fields")
                continue
            data, subjects = records.get(allowance["evidence_feature"], ({}, set()))
            declared = data.get("contact_allowances", [])
            if (not set(allowance["subject_paths"]) <= subjects
                    or not isinstance(declared, list) or allowance not in declared):
                problems.append(f"{allowance['allowance_id']}: missing exact current contact evidence")
        return tuple(problems)

    def _valid_record(self, record):
        return (isinstance(record, dict) and set(record) == self.KEYS
                and all(isinstance(record[field], str) and record[field].strip()
                        for field in ("allowance_id", "evidence_feature", "basis"))
                and isinstance(record["subject_paths"], list)
                and all(isinstance(path, str) for path in record["subject_paths"])
                and all(isinstance(record[field], list) for field in ("minimum_mm", "maximum_mm")))
