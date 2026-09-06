"""Scope: Register one cabinet feature in deterministic composition order."""

from __future__ import annotations

import json
from pathlib import Path
import re


class CabinetFeatureManifest:
    """Merge one feature module into a cabinet-local ordered manifest."""

    _ASSEMBLY_ID = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")
    _MODULE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*$")
    _PART_PATH = re.compile(r"^[a-z][a-z0-9_]*(?:/[a-z][a-z0-9_]*)*$")

    def register(
        self,
        project_root: Path,
        assembly_id: str,
        module: str,
        order: int,
        review_module: str | None = None,
        affected_manufactured_part_paths: tuple[str, ...] = (),
    ) -> Path | None:
        self._validate(assembly_id, module, order)
        if review_module is not None and not self._MODULE.fullmatch(review_module):
            raise ValueError("review module must be a stable dotted name")
        if len(set(affected_manufactured_part_paths)) != len(
            affected_manufactured_part_paths
        ) or any(
            not self._PART_PATH.fullmatch(path)
            for path in affected_manufactured_part_paths
        ):
            raise ValueError("affected manufactured part paths must be unique and stable")
        path = project_root / "assemblies" / assembly_id / "features.json"
        features = self._load(path)
        by_module = {item["module"]: item for item in features}
        registration = {
            "module": module,
            "order": order,
            "affected_manufactured_part_paths": list(
                affected_manufactured_part_paths
            ),
        }
        if review_module is not None:
            registration["review_module"] = review_module
        by_module[module] = registration
        ordered = sorted(by_module.values(), key=lambda item: (item["order"], item["module"]))
        data = {"schema_version": 1, "features": ordered}
        content = json.dumps(data, indent=2) + "\n"
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            return None
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _load(self, path: Path) -> tuple[dict[str, object], ...]:
        if not path.is_file():
            return ()
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValueError(f"unsupported cabinet feature manifest: {path}")
        features = data.get("features")
        if not isinstance(features, list):
            raise ValueError(f"invalid cabinet feature manifest: {path}")
        return tuple(features)

    def _validate(self, assembly_id: str, module: str, order: int) -> None:
        if not self._ASSEMBLY_ID.fullmatch(assembly_id):
            raise ValueError("feature assembly id must be stable")
        if not self._MODULE.fullmatch(module):
            raise ValueError("feature module must be a stable dotted name")
        if order < 0:
            raise ValueError("feature order cannot be negative")


__all__ = ["CabinetFeatureManifest"]
