"""Scope: Verify hinge purchases follow declared panel owners without altering source poses."""
from dataclasses import replace
from types import SimpleNamespace

import pytest

from door_hinge_plan import DoorHingePlanner
from door_hinge_side import DoorHingeSide
from door_host_test_support import DoorHostTestSupport
from review_inspection_identity import ReviewInspectionIdentity
from riex_nc70_hardware_frame import RiexNc70HardwareFrameResolver
from riex_nc70_hardware_specs import RiexNc70HardwareSpecs
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as PROFILE


class AssemblyTreeHardware(SimpleNamespace):
    """Supply only the tree visit needed by the inspection identity contract."""


class TestRiexHingeAttachment:
    @pytest.mark.parametrize("hand", (DoorHingeSide.LEFT, DoorHingeSide.RIGHT))
    @pytest.mark.parametrize("face", ("<Z", ">Z"))
    def test_custom_panel_owners_purchase_identity_and_native_poses(self, tmp_path, hand, face):
        host = DoorHostTestSupport().create(tmp_path, hand, face)
        plan = DoorHingePlanner().plan(host, PROFILE, hand)
        hardware = RiexNc70HardwareSpecs().build(host, plan, PROFILE)
        assert len(hardware) == len(plan.placements)*2
        owners = {"F000001": "slab", "F000049": "post"}
        root = ("furniture", "niche_01")
        assemblies = {root: SimpleNamespace(assembly=SimpleNamespace(parts=tuple(
            SimpleNamespace(spec=part) for part in host.assembly.parts)))}
        frames = RiexNc70HardwareFrameResolver()
        for position, hinge, plate in zip(plan.placements, hardware[::2], hardware[1::2], strict=True):
            expected = (
                frames.hinge(host, PROFILE, host.door_bottom_mm+position.door_height_mm, hand),
                frames.plate(host, PROFILE, host.support_bottom_mm+position.cabinet_height_mm, hand),
            )
            for item, frame in zip((hinge, plate), expected, strict=True):
                owner = owners[item.product_code]
                assert item.mounting_part_id == owner
                assert item.purchase.purchase_id == item.hardware_id
                assert item.purchase.product_code == item.product_code
                assert item.purchase.required_members == ("item",)
                placement = item.local_to_parent
                point, basis = placement.origin_in_parent, placement.axis_basis
                assert (point.x_mm, point.y_mm, point.z_mm) == frame.origin_mm
                assert tuple((axis.x, axis.y, axis.z) for axis in (
                    basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent)) == (
                    frame.local_x_in_cabinet, frame.local_y_in_cabinet, frame.local_z_in_cabinet)
                visit = AssemblyTreeHardware(path=root+("hardware:"+item.hardware_id,),
                                             hardware=SimpleNamespace(spec=item))
                assert ReviewInspectionIdentity().path(visit, assemblies) == (
                    "niche_01", owner, item.hardware_id)

    def test_assembly_datum_is_not_claimed_as_a_physical_mounting_panel(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        # This contract-only host marks the datum as layered; no layer CAD is built.
        host.spec = replace(host.spec, door_assembly_id=host.spec.door_part_id)
        plan = DoorHingePlanner().plan(host, PROFILE)
        hardware = RiexNc70HardwareSpecs().build(host, plan, PROFILE)
        assert {item.mounting_part_id for item in hardware[::2]} == {None}
        assert {item.mounting_part_id for item in hardware[1::2]} == {"post"}
