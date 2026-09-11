"""Scope: Bind construction evidence to current declared values and project source inputs."""

from dataclasses import fields, is_dataclass
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace


class ConstructionInputFingerprinter:
    """Catch metadata-only changes even when the rendered geometry remains identical."""

    def build(self, root, visits):
        records = []
        for visit in visits:
            item = getattr(visit, "assembly", getattr(visit, "part", getattr(visit, "hardware", None)))
            record = {"path": visit.path, "spec": item.spec, "placement": visit.local_to_root}
            if hasattr(visit, "assembly"):
                record["joints"] = visit.assembly.joints
            records.append(self._value(record))
        content = {"schema_version": 1, "tree": sorted(records, key=lambda item: item["path"]),
                   "source": self.source_inputs(root)}
        return sha256(json.dumps(content, sort_keys=True, separators=(",", ":"),
                                 allow_nan=False).encode()).hexdigest()

    def source_inputs(self, root):
        inputs = [root / "aikea.yaml", *(root / "assemblies").rglob("*.py"),
                  *(root / "assemblies").rglob("features.json")]
        return {str(path.relative_to(root)): sha256(path.read_bytes()).hexdigest()
                for path in sorted(set(inputs)) if path.is_file()}

    def require_unchanged_sources(self, root, snapshot):
        if self.source_inputs(root) != snapshot:
            raise ValueError("construction inputs changed during the build; rebuild before reviewing")

    def _value(self, value):
        if is_dataclass(value):
            return {"type": type(value).__name__, **{
                field.name: self._value(getattr(value, field.name)) for field in fields(value)
            }}
        if isinstance(value, SimpleNamespace):
            return self._value(vars(value))
        if isinstance(value, dict):
            return {key: self._value(item) for key, item in value.items()}
        if isinstance(value, (tuple, list)):
            return [self._value(item) for item in value]
        if isinstance(value, Path):
            return str(value)
        if value is None or isinstance(value, (str, bool, int, float)):
            return value
        raise ValueError(f"unsupported construction input value: {type(value).__name__}")
