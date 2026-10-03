"""Scope: Provide a test-only overlapping reference pair and exact contact evidence."""

from hashlib import sha256
import importlib
import json

import cadquery as cq

from cabinet_feature_manifest import CabinetFeatureManifest
from construction_input_fingerprint import ConstructionInputFingerprinter
from generated_project_module_runtime import GeneratedProjectModuleRuntime


class ConstructionContactFixture:
    """Exercise geometric allowance enforcement without claiming this is a furniture design."""

    def build(self, root, contracts, minimum_x=9, maximum_volume=100):
        values, panels = contracts
        left = values.PartSpec("left", "test reference", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(10, 10, 10), material_id="test material")
        right = values.PartSpec("right", "test reference", (), values.LocalToParentPlacement(
            values.Point3D(9, 0, 0), values.IDENTITY_AXIS_BASIS),
            local_size_mm=(10, 10, 10), material_id="test material")
        self.built = panels.PanelAssemblyBuilder(panels.PanelAssemblySpec("unit_01", "contact fixture", (left, right))).build()
        walker, allowance_type = GeneratedProjectModuleRuntime().execute(root, self._contracts)
        self.visits = walker.walk(self.built)
        self.allowance = allowance_type("reference_fit", ("unit_01/part:left", "unit_01/part:right"),
                                        (minimum_x, 0, 0), (10, 10, 10), maximum_volume,
                                        "unit_01/feature:reference_fit.feature", "Test-only bounded reference overlap")
        self.record = {"allowance_id": self.allowance.allowance_id,
                       "subject_paths": list(self.allowance.subject_paths),
                       "minimum_mm": list(self.allowance.minimum_mm), "maximum_mm": list(self.allowance.maximum_mm),
                       "maximum_volume_mm3": maximum_volume, "evidence_feature": self.allowance.evidence_feature,
                       "basis": self.allowance.basis}
        self.root = root
        self.envelope = cq.Workplane("XY").box(20, 20, 20, centered=False)
        owner = root / "assemblies/unit_01"
        owner.mkdir()
        (owner / "spec.py").write_text('"""Scope: Identify this test feature owner."""\n')
        (owner / "builder.py").write_text(
            '"""Scope: Declare this test reference boundary and contact."""\nimport cadquery as cq\n'
            'from assemblies.contact_allowance import ContactAllowanceSpec\n'
            'ENVELOPE = cq.Workplane("XY").box(20, 20, 20, centered=False)\n'
            f'CONTACT_ALLOWANCES = (ContactAllowanceSpec(**{self.record!r}),)\n')
        CabinetFeatureManifest().register(root, "unit_01", "reference_fit.feature", 10,
                                          affected_manufactured_part_paths=("left", "right"))
        return self

    def write_evidence(self):
        artifacts = []
        for part in self.built.parts:
            path = f"unit_01/{part.spec.part_id}"
            step = self.root / "manufacturing/parts" / (path.replace("/", "__") + ".step")
            step.parent.mkdir(parents=True, exist_ok=True)
            cq.exporters.export(part.solid, str(step))
            artifacts.append({"path": path, "step_sha256": sha256(step.read_bytes()).hexdigest()})
        self.evidence_path = self.root / "assemblies/unit_01/fabrication-evidence/reference_fit-feature.json"
        self.data = {"schema_version": 1, "feature": "reference_fit.feature", "status": "valid",
                     "manufacturing_authority": True, "part_artifacts": artifacts,
                     "checks": [{"name": "test-only reference contact declaration", "passed": True}],
                     "construction_sha256": ConstructionInputFingerprinter().build(self.root, self.visits),
                     "contact_allowances": [self.record]}
        self.save()

    def save(self):
        self.evidence_path.parent.mkdir(exist_ok=True)
        self.evidence_path.write_text(json.dumps(self.data))

    def _contracts(self):
        return (importlib.import_module("assemblies.assembly_tree").AssemblyTreeWalker(),
                importlib.import_module("assemblies.contact_allowance").ContactAllowanceSpec)
