"""Scope: Parse versioned fabrication records into unique exact-path indexes."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path


class FabricationRecordValidator:
    """Reject malformed records, missing paths, duplicates, and unexpected rows."""

    def json_index(
        self,
        path: Path,
        key: str,
        expected_paths: tuple[str, ...],
    ) -> tuple[dict[str, dict], tuple[str, ...]]:
        data = self.read_json(path)
        records = data.get(key) if data and data.get("schema_version") == 1 else None
        if not isinstance(records, list):
            return {}, (str(path),)
        return self._index(path, tuple(records), expected_paths)

    def csv_index(
        self,
        path: Path,
        expected_paths: tuple[str, ...],
    ) -> tuple[dict[str, dict], tuple[str, ...]]:
        try:
            with path.open(newline="", encoding="utf-8") as source:
                records = tuple(csv.DictReader(source))
        except OSError:
            return {}, (str(path),)
        return self._index(path, records, expected_paths)

    def read_json(self, path: Path) -> dict | None:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _index(
        self,
        path: Path,
        records: tuple,
        expected_paths: tuple[str, ...],
    ) -> tuple[dict[str, dict], tuple[str, ...]]:
        valid_records = tuple(item for item in records if isinstance(item, dict))
        record_paths = tuple(item.get("path") for item in valid_records)
        counts = Counter(item for item in record_paths if isinstance(item, str))
        expected_counts = Counter(expected_paths)
        expected = set(expected_counts)
        actual = set(counts)
        problems = tuple(
            sorted(
                ({str(path)} if len(valid_records) != len(records) else set())
                | {f"{item}: missing" for item in expected - actual}
                | {f"{item}: unexpected" for item in actual - expected}
                | {f"{item}: duplicate" for item, count in counts.items() if count != 1}
                | {
                    f"{item}: duplicate tree path"
                    for item, count in expected_counts.items()
                    if count != 1
                }
            )
        )
        return {
            item["path"]: item
            for item in valid_records
            if isinstance(item.get("path"), str) and counts[item["path"]] == 1
        }, problems


__all__ = ["FabricationRecordValidator"]
