"""Scope: Describe exact hinge and plate purchases using the shared hardware frames."""
from dataclasses import replace

from door_host import DoorHost
from purchased_hardware_spec import PurchasedHardwareSpec, HardwarePurchaseSpec
from riex_nc70_hardware_frame import RiexNc70HardwareFrameResolver


class RiexNc70HardwareSpecs:
    def build(self, assembly, plan, profile):
        host = DoorHost.resolve(assembly, plan.hinge_side, plan.host_spec)
        host.require_current_plan(plan, profile)
        frames, items = RiexNc70HardwareFrameResolver(), []
        # A layered front ID names an assembly datum, not an owned physical panel.
        door_owner = host.spec.door_part_id if host.spec.door_assembly_id is None else None
        for position in plan.placements:
            rows = (
                ("hinge", "F000001", "riex-nc70-f000001-closed", door_owner, frames.hinge(
                    host, profile, host.door_bottom_mm+position.door_height_mm, plan.hinge_side)),
                ("plate", "F000049", "riex-nc70-f000049-h0-euroscrew-plate", host.spec.support_part_id, frames.plate(
                    host, profile, host.support_bottom_mm+position.cabinet_height_mm, plan.hinge_side)),
            )
            for kind, code, asset, mounting_part_id, frame in rows:
                name = f"{position.hinge_id}_{kind}"
                template = host.door.local_to_parent
                basis = template.axis_basis
                axes = tuple(replace(axis, x=value[0], y=value[1], z=value[2]) for axis, value in zip(
                    (basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent),
                    (frame.local_x_in_cabinet, frame.local_y_in_cabinet, frame.local_z_in_cabinet)))
                placement = replace(template, origin_in_parent=replace(template.origin_in_parent,
                    x_mm=frame.origin_mm[0], y_mm=frame.origin_mm[1], z_mm=frame.origin_mm[2]),
                    axis_basis=replace(basis, local_x_in_parent=axes[0], local_y_in_parent=axes[1], local_z_in_parent=axes[2]))
                items.append(PurchasedHardwareSpec(name, "Riex", code, asset, placement,
                    purchase=HardwarePurchaseSpec(name, code, "piece", "item", ("item",)),
                    mounting_part_id=mounting_part_id))
        return tuple(items)
