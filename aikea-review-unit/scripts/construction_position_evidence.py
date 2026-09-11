"""Scope: Save and independently re-evaluate closed geometry for any physical root."""

from hashlib import sha256
import json

import cadquery as cq

from construction_contact_evidence import ConstructionContactEvidence
from construction_input_fingerprint import ConstructionInputFingerprinter
from construction_physical_geometry import ConstructionPhysicalGeometry
from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from furniture_geometry_check import FurnitureGeometryCheck
from construction_envelope_authority import ConstructionEnvelopeAuthority


class ConstructionPositionEvidence:
    """A valid saved report must reproduce against current solids, inputs and contact evidence."""

    REPORT = "assemblies/construction-position-check.json"
    ENVELOPE = "assemblies/construction-envelope.step"

    def write(self, root, visits, envelope, allowances=(), envelope_source="root_builder"):
        path = root / self.REPORT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"schema_version": 2, "status": "invalid"}) + "\n")
        contacts = ConstructionContactEvidence().records(allowances)
        tree = FabricationTreeEvidenceBuilder().build(visits)
        problems = ConstructionContactEvidence().check(root, tree, visits, contacts)
        physical = ConstructionPhysicalGeometry()
        parts = physical.build(visits)
        geometry = FurnitureGeometryCheck().check(parts, envelope, contacts if not problems else ())
        envelope_path = root / self.ENVELOPE
        cq.exporters.export(envelope, str(envelope_path))
        data = {
            "schema_version": 2, "root_assembly_id": visits[0].assembly.spec.assembly_id,
            "status": "valid" if geometry["status"] == "valid" and not problems else "invalid",
            "construction_sha256": ConstructionInputFingerprinter().build(root, visits),
            "envelope": self.ENVELOPE, "envelope_sha256": sha256(envelope_path.read_bytes()).hexdigest(),
            "envelope_source": envelope_source,
            "physical_items": physical.bounds(parts), "geometry": geometry,
            "contact_allowances": contacts, "contact_evidence_problems": list(problems),
        }
        path.write_text(json.dumps(data, indent=2) + "\n")
        return data

    def check(self, root, tree, visits):
        data = FabricationRecordValidator().read_json(root / self.REPORT)
        problems = self._record_problems(root, visits, data)
        if not problems:
            problems.extend(ConstructionContactEvidence().check(root, tree, visits, data.get("contact_allowances")))
        if not problems:
            # The saved STEP is an external parsing boundary; report a corrupt validation input.
            try:
                envelope = cq.importers.importStep(str(root / self.ENVELOPE))
            except ValueError:
                problems.append("declared envelope is not a readable STEP solid")
        if not problems:
            expected, allowances, source = ConstructionEnvelopeAuthority().read(
                root, visits[0].assembly.spec.assembly_id)
            if (source != data["envelope_source"]
                    or expected.val().cut(envelope.val()).Volume() + envelope.val().cut(expected.val()).Volume() > 1e-5
                    or ConstructionContactEvidence().records(allowances) != data["contact_allowances"]):
                problems.append("saved envelope or contacts differ from the current declared inputs")
        if not problems:
            physical = ConstructionPhysicalGeometry()
            parts = physical.build(visits)
            geometry = FurnitureGeometryCheck().check(parts, envelope, data["contact_allowances"])
            if geometry["status"] != "valid" or geometry != data.get("geometry"):
                problems.append("closed geometry does not reproduce the saved position checks")
            if physical.bounds(parts) != data.get("physical_items"):
                problems.append("current physical paths or bounds differ from the position record")
        return FabricationReadinessCheck("validation.construction_position", not problems, tuple(problems))

    def _record_problems(self, root, visits, data):
        if (not data or data.get("schema_version") != 2 or data.get("status") != "valid"
                or data.get("root_assembly_id") != visits[0].assembly.spec.assembly_id
                or data.get("construction_sha256") != ConstructionInputFingerprinter().build(root, visits)
                or data.get("envelope") != self.ENVELOPE
                or data.get("envelope_source") not in ("root_builder", "configured_measurements")
                or data.get("contact_evidence_problems") != []):
            return ["missing or stale construction position record"]
        envelope = root / self.ENVELOPE
        if not envelope.is_file() or sha256(envelope.read_bytes()).hexdigest() != data.get("envelope_sha256"):
            return ["missing or changed declared envelope"]
        return []
