"""Scope: Bind KA 4532 proof to current custom host geometry and support material."""

from dataclasses import replace
from types import SimpleNamespace

import cadquery as cq
import pytest

from drawer_host import DrawerHost, DrawerHostSpec
from hettich_ka_4532_installed_geometry_test_support import HettichKa4532InstalledGeometryTestSupport
from hettich_ka_4532_spacer_installed_fixing_checker import HettichKa4532SpacerInstalledFixingChecker
from hettich_ka_4532_spacer_mounting_test_support import HettichKa4532SpacerMountingTestSupport
from hettich_ka_4532_spacer_proof_checker import HettichKa4532SpacerProofChecker
from hettich_ka_4532_fixing_evidence_test_support import HettichKa4532FixingEvidenceTestSupport


class TestDrawerHostProof:
    @pytest.fixture
    def installed(self):
        fixture = HettichKa4532InstalledGeometryTestSupport()
        parts = fixture.shifted_parts(tuple(fixture.parts), x_mm=100, y_mm=50, z_mm=80)
        supports = {}
        for side, name, x, y, normal in (("left", "support_a", 98, 25, (1, 0, 0)),
                                       ("right", "support_b", 199, 650, (-1, 0, 0))):
            part = HettichKa4532SpacerMountingTestSupport()._side_part(x, y, normal)
            part.part_id, part.local_size_mm = name, (625, 500, 2)
            part.local_to_parent.origin_in_parent.z_mm = 30
            supports[name] = part
            old = parts.pop(f"{side}_side")
            shape = cq.Solid.makeBox(2, 625, 500, cq.Vector(98 if side == "left" else 197, 25, 30))
            parts[name] = replace(old, name=name, solid=cq.Workplane(obj=shape), location=cq.Location())
        assembly = SimpleNamespace(assembly_id="niche_01", parts=tuple(supports.values()), part=supports.__getitem__)
        host = DrawerHost(assembly, DrawerHostSpec("support_a", "support_b", 50, 550, 80, 400))
        return host, parts, fixture.source

    def test_shifted_renamed_supports_with_inset_front_verify(self, installed):
        host, parts, source = installed
        assert HettichKa4532SpacerInstalledFixingChecker().axis_height("drawer_01", parts, source, host) == 103

    @pytest.mark.parametrize("change", ("front", "ceiling", "shifted_support", "missing_support", "void_at_fixing"))
    def test_current_host_changes_or_missing_support_reject_stale_geometry(self, installed, change):
        host, parts, source = installed
        if change == "front":
            host = DrawerHost(host.assembly, replace(host.spec, front_mm=49))
        elif change == "ceiling":
            host = DrawerHost(host.assembly, replace(host.spec, top_mm=81))
        elif change == "missing_support":
            parts.pop("support_a")
        elif change == "shifted_support":
            parts["support_a"] = replace(parts["support_a"], location=cq.Location(cq.Vector(1, 0, 0)))
        else:
            part = parts["support_a"]
            void = cq.Solid.makeCylinder(5, 4, cq.Vector(97, 87, 103), cq.Vector(1, 0, 0))
            parts[part.name] = replace(part, solid=cq.Workplane(obj=part.placed_shape().cut(void)))
        assert HettichKa4532SpacerInstalledFixingChecker().axis_height("drawer_01", parts, source, host) is None

    def test_proof_uses_actual_reservation_participants(self, installed):
        host, parts, source = installed
        opened = tuple(replace(part, location=cq.Location(cq.Vector(0, -50, 0))*part.location)
                       if name.startswith("drawer_01__") else part for name, part in parts.items())
        evidence = HettichKa4532FixingEvidenceTestSupport().build()
        evidence["cabinet_id"] = "niche_01"
        for axis in evidence["resolved_authority"]["spacer_support_corridor"]["axes"]:
            axis["cabinet_height_mm"] = 103
        source_cad = {"runner": {"item_number": "9114276", "asset_id": "hettich-ka-4532-500-runner-pair", "sha256": "runner-sha256"},
                      "spacer": {"item_number": "13952", "asset_id": "hettich-13952-spacer-profile", "sha256": "spacer-sha256", "instances": 2}}
        checker = HettichKa4532SpacerProofChecker()
        correct = tuple({"side_part_id": name} for name in ("support_a", "support_b"))
        args = ("niche_01", "drawer_01", 50, tuple(parts.values()), opened, source_cad, source, {}, evidence)
        report = checker.check(*args, correct, host)
        assert report.is_valid, report.failed_check_names()
        assert report.as_dict()["manufacturing_authority"] is False
        stale = tuple({"side_part_id": name} for name in ("left_side", "right_side"))
        assert not checker.check(*args, stale, host).is_valid
