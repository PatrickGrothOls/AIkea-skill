"""Scope: Load authored envelope and contact declarations inside the generated project runtime."""

import importlib
from functools import partial

from generated_project_module_runtime import GeneratedProjectModuleRuntime


class ConstructionPositionInputs:
    def read(self, root, assembly_id):
        return GeneratedProjectModuleRuntime().execute(root, partial(self._read, assembly_id))

    def _read(self, assembly_id):
        module = importlib.import_module(f"assemblies.{assembly_id}.builder")
        envelope = getattr(module, "ENVELOPE", None)
        source = "root_builder" if envelope is not None else getattr(module, "ENVELOPE_SOURCE", None)
        return envelope, getattr(module, "CONTACT_ALLOWANCES", ()), source
