"""Scope: Validate structured fabrication records and their tree-path coverage."""

from __future__ import annotations

import csv
import json
from pathlib import Path


class FabricationRecordValidator:
    """Require versioned records with one complete row per expected physical item."""

    def json_coverage(
        self,
        path: Path,
        key: str,
        expected: tuple[str, ...],
        required_fields: tuple[str, ...],
    ) -> tuple[str, ...]:
        data = self.read_json(path)
        if not data or data.get("schema_version") != 1:
            return (str(path),)
        records = data.get(key)
        if not isinstance(records, list):
            return (str(path),)
        by_path = {
            item.get("path"): item for item in records if isinstance(item, dict)
        }
        missing = set(expected) - set(by_path)
        incomplete = {
            item_path
            for item_path in expected
            if item_path in by_path
            and any(by_path[item_path].get(field) in (None, "") for field in required_fields)
        }
        return tuple(sorted(missing | incomplete))

    def csv_coverage(
        self,
        path: Path,
        expected: tuple[str, ...],
        required_fields: tuple[str, ...],
    ) -> tuple[str, ...]:
        try:
            with path.open(newline="", encoding="utf-8") as source:
                rows = tuple(csv.DictReader(source))
        except OSError:
            return (str(path),)
        by_path = {row.get("path"): row for row in rows}
        missing = set(expected) - set(by_path)
        incomplete = {
            item_path
            for item_path in expected
            if item_path in by_path
            and any(by_path[item_path].get(field) in (None, "") for field in required_fields)
        }
        return tuple(sorted(missing | incomplete)) or (() if rows else (str(path),))

    def read_json(self, path: Path) -> dict | None:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None


__all__ = ["FabricationRecordValidator"]
