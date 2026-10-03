"""Scope: Reconstruct the declared envelope from the current authoritative project input."""

import yaml
from functools import partial

from construction_position_inputs import ConstructionPositionInputs
from generated_project_module_runtime import GeneratedProjectModuleRuntime


class ConstructionEnvelopeAuthority:
    """Keep the exported STEP from becoming an independent or silently enlarged boundary."""

    def read(self, root, assembly_id, project=None):
        envelope, allowances, source = ConstructionPositionInputs().read(root, assembly_id)
        if source == "configured_measurements":
            envelope = GeneratedProjectModuleRuntime().execute(root, partial(self._configured, root, project))
        elif source != "root_builder":
            raise ValueError("unknown construction envelope authority")
        if envelope is None:
            raise ValueError("the selected root has no declared envelope")
        return envelope, allowances, source

    def _configured(self, root, project):
        from configured_review_envelope import ConfiguredReviewEnvelope

        # Preview callers may hold unsaved inputs; the fabrication gate always re-reads the saved file.
        if project is None:
            project = yaml.safe_load((root / "aikea.yaml").read_text())
        return ConfiguredReviewEnvelope().build(project)
