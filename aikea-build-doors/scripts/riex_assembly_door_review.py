"""Scope: Move the complete front child with exact open hinge CAD in generic tree review."""
import cadquery as cq

from assembly_door_host import AssemblyDoorHost
from assembly_tree_review_plan import AssemblyReviewMotion, AssemblyReviewOverlay, AssemblyTreeReviewPlan
from local_to_parent_location import LocalToParentLocation
from riex_nc70_hardware_loader import RiexNc70HardwareLoader
from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
from riex_nc70_hardware_specs import RiexNc70HardwareSpecs
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as PROFILE
from unit_mockup import UnitMockupInputError


class RiexAssemblyDoorReview:
    def __init__(self, plan):
        self.saved_plan = plan
        self.hardware = RiexNc70HardwareLoader()

    def plan(self, context, state):
        if state not in {"closed", "open", "removed"}:
            raise UnitMockupInputError([f"unsupported door review state: {state}"])
        plan = self.saved_plan
        host = AssemblyDoorHost(context.assembly, plan.host_spec, plan.hinge_side)
        expected = RiexNc70HardwareSpecs().build(host, plan, PROFILE)
        current = {item.spec.hardware_id: item.spec for item in context.assembly.purchased_hardware}
        if any(current.get(item.hardware_id) != item for item in expected):
            raise UnitMockupInputError(["the front review requires the current exact hinge purchases"])
        if state == "closed":
            return AssemblyTreeReviewPlan()
        hidden = tuple(context.owner_path+(f"hardware:{item.hardware_id}",) for item in expected)
        child_path = context.owner_path+(host.front.spec.assembly_id,)
        if state == "removed":
            return AssemblyTreeReviewPlan(hidden_paths=hidden, hidden_subtrees=(child_path,))
        placement = RiexNc70HardwarePlacement()
        pivot = placement.pivot(host, PROFILE, plan.hinge_side)
        translation = cq.Location(cq.Vector(*pivot, 0))
        rotation = cq.Location(cq.Vector(), cq.Vector(0,0,1),
                               plan.hinge_side.opening_angle_degrees(PROFILE.open_angle_degrees))
        front_frame = LocalToParentLocation().build(host.front.spec.local_to_parent)
        motion = front_frame.inverse * translation * rotation * translation.inverse * front_frame
        hardware = self.hardware.load(context.project_root/'hardware/riex/nc70')
        parts = placement.parts(host, hardware, plan, PROFILE, True)
        return AssemblyTreeReviewPlan(motions=(AssemblyReviewMotion(child_path, motion),),
            hidden_paths=hidden, overlays=(AssemblyReviewOverlay(context.owner_path, parts),))
