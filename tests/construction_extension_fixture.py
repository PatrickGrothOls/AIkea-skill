"""Scope: Build and evidence a small custom paired pocket operation for protocol tests."""

from dataclasses import replace
from hashlib import sha256
import importlib
import json

import cadquery as cq

from construction_input_fingerprint import ConstructionInputFingerprinter
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from part_cut import AssemblyCuts, PartCut
from cabinet_feature_manifest import CabinetFeatureManifest


class PairedPocketBuilder:
    """Register one shared cutter into two adjacent panel frames."""

    def build(self, spec, joints):
        cutter = cq.Workplane("XY").center(20, 15).circle(3).extrude(8).translate((0, 0, 12)).val()
        return AssemblyCuts((
            PartCut("pair", "lower", 1, cutter, cq.Location()),
            PartCut("pair", "upper", 1, cutter, cq.Location(cq.Vector(0, 0, -16))),
        ))


class ConstructionExtensionFixture:
    """Keep geometry, exported participants and independently measured checks together."""

    def build(self, root, contracts):
        values, panels = contracts
        lower = values.PartSpec("lower", "custom", (), values.IDENTITY_LOCAL_TO_PARENT,
                                local_size_mm=(100, 30, 16), material_id="MDF")
        upper = replace(lower, part_id="upper", local_to_parent=values.LocalToParentPlacement(
            values.Point3D(0, 0, 16), values.IDENTITY_AXIS_BASIS))
        joint = values.JointSpec("pair", ("lower", "upper"), "test paired registration", "paired_pocket")
        requirement = values.ConstructionRequirementSpec(
            "registration", "Apply matching local pockets", ("part:lower", "part:upper"),
            ("joint:pair",), "operations")
        spec = panels.PanelAssemblySpec("unit_01", "custom", (lower, upper), (joint,),
                                       requirements=(requirement,))
        self.built = panels.PanelAssemblyBuilder(spec, joint_builder=PairedPocketBuilder()).build()
        walker = GeneratedProjectModuleRuntime().execute(root, self._walker)
        self.visits = walker.walk(self.built)
        self.root = root
        return self

    def write_evidence(self, participants=("lower", "upper"), hardware=()):
        owner = self.root / "assemblies/unit_01"
        owner.mkdir(exist_ok=True)
        (owner / "spec.py").write_text('"""Test fixture owner; values are held in the built spec."""\n')
        CabinetFeatureManifest().register(self.root, "unit_01", "paired_pocket.feature", 10,
                                          affected_manufactured_part_paths=participants,
                                          affected_purchased_hardware_paths=hardware,
                                          qualified_joint_ids=("pair",))
        artifacts = []
        for part in self.built.parts:
            path = f"unit_01/{part.spec.part_id}"
            step = self.root / "manufacturing/parts" / (path.replace("/", "__") + ".step")
            step.parent.mkdir(parents=True, exist_ok=True)
            cq.exporters.export(part.solid, str(step))
            if part.spec.part_id in participants:
                artifacts.append({"path": path, "step_sha256": sha256(step.read_bytes()).hexdigest()})
        lower, upper = self.built.cuts
        a = lower.cutter.located(lower.location)
        b = upper.cutter.located(cq.Location(cq.Vector(0, 0, 16)) * upper.location)
        self.evidence_path = owner / "fabrication-evidence/paired_pocket-feature.json"
        self.data = {
            "schema_version": 1, "feature": "paired_pocket.feature", "status": "valid",
            "manufacturing_authority": True, "qualified_joint_ids": ["pair"],
            "construction_sha256": ConstructionInputFingerprinter().build(self.root, self.visits),
            "checks": [{"name": "paired registration", "passed": a.cut(b).Volume() + b.cut(a).Volume() < 1e-6}],
            "part_artifacts": artifacts,
            "purchased_hardware_paths": [f"unit_01/{item}" for item in hardware],
        }
        self.save()

    def save(self):
        self._json(self.evidence_path, self.data)

    def _json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    def _walker(self):
        return importlib.import_module("assemblies.assembly_tree").AssemblyTreeWalker()
