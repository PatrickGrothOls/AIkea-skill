"""Scope: Verify explicit mounting paths and lossless GLB inspection annotation."""

from dataclasses import replace
import json
import struct
from types import SimpleNamespace

import cadquery as cq
import pytest

from cadquery_glb_exporter import CadQueryGlbExporter
from glb_inspection_metadata import GlbInspectionMetadata
from purchased_hardware_spec import PurchasedHardwareSpec
from review_inspection_identity import ReviewInspectionIdentity
from unit_mockup import MockupPart, UnitMockupInputError


class AssemblyTreeHardware(SimpleNamespace):
    """Minimal tree visit for testing ownership independently of solid generation."""


class TestReviewInspectionMetadata:
    def hardware_visit(self, owner, part_id):
        spec = PurchasedHardwareSpec("component", "Vendor", "SKU", "source", None,
                                     mounting_part_id=part_id)
        return AssemblyTreeHardware(path=owner+("hardware:component",), hardware=SimpleNamespace(spec=spec))

    def test_fixed_and_drawer_mounted_members_keep_separate_owners(self):
        panel = SimpleNamespace(spec=SimpleNamespace(part_id="support"))
        root = ("dresser_01",)
        drawer = root+("drawer_01",)
        assemblies = {owner:SimpleNamespace(assembly=SimpleNamespace(parts=(panel,)))
                      for owner in (root, drawer)}
        identity = ReviewInspectionIdentity()
        assert identity.path(self.hardware_visit(root,"support"),assemblies)==("support","component")
        assert identity.path(self.hardware_visit(drawer,"support"),assemblies)==("drawer_01","support","component")
        assert identity.path(self.hardware_visit(drawer,None),assemblies)==("drawer_01","component")
        with pytest.raises(UnitMockupInputError,match="mounting part is missing"):
            identity.path(self.hardware_visit(root,"missing"),assemblies)

    def test_older_saved_hardware_contract_keeps_its_existing_assembly_path(self):
        item=AssemblyTreeHardware(path=("dresser_01","drawer_01","hardware:runner"),
                                  hardware=SimpleNamespace(spec=SimpleNamespace(hardware_id="runner")))
        assert ReviewInspectionIdentity().path(item,{})==("drawer_01","runner")

    def test_metadata_does_not_change_names_placements_or_binary_geometry(self,tmp_path):
        path = tmp_path/"assembly.glb"
        panel = MockupPart("unaltered_part_id",cq.Workplane("XY").box(20,30,40),
                          cq.Location(cq.Vector(10,20,30)),(.5,.5,.5,1))
        CadQueryGlbExporter().export("assembly_01",(panel,),path)
        before, binary = self.document_and_binary(path)
        annotated = replace(panel,inspection_path=("drawer","panel","fitting"),review_kind="hardware")
        GlbInspectionMetadata().write(path,(annotated,))
        after, changed_binary = self.document_and_binary(path)
        assert binary == changed_binary
        for old,new in zip(before["nodes"],after["nodes"],strict=True):
            if old.get("name")==panel.name and "mesh" in old:
                assert new["extras"]["aikea"]=={
                    "inspection_path":["drawer","panel","fitting"],"kind":"hardware"}
                new.pop("extras")
        assert before==after

    def test_exporter_writes_metadata_on_real_cadquery_part_nodes(self,tmp_path):
        path = tmp_path/"assembly.glb"
        part = MockupPart("part",cq.Workplane("XY").box(20,30,40),cq.Location(),(.5,.5,.5,1),
                          inspection_path=("drawer","part"),review_kind="panel")
        CadQueryGlbExporter().export("assembly_01",(part,),path)
        document,_ = self.document_and_binary(path)
        actual = [n["extras"]["aikea"] for n in document["nodes"] if n.get("name")=="part" and "mesh" in n]
        assert actual==[{"inspection_path":["drawer","part"],"kind":"panel"}]

    def test_incorrect_exported_identity_does_not_partially_rewrite_artifact(self,tmp_path):
        path=tmp_path/"assembly.glb"
        part=MockupPart("part",cq.Workplane("XY").box(20,30,40),cq.Location(),(.5,.5,.5,1))
        CadQueryGlbExporter().export("assembly_01",(part,),path)
        original=path.read_bytes()
        with pytest.raises(UnitMockupInputError,match="inspection parts are missing"):
            GlbInspectionMetadata().write(path,(replace(part,name="wrong",inspection_path=("wrong",)),))
        assert path.read_bytes()==original

    def document_and_binary(self,path):
        content=path.read_bytes()
        size=struct.unpack_from("<I",content,12)[0]
        return json.loads(content[20:20+size]),content[20+size:]
