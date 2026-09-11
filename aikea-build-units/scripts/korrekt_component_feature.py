"""Scope: Own explicit Korrekt station purchases, deck operations and installation requirements."""

from dataclasses import dataclass, replace

from cabinet_feature_manifest import CabinetFeatureManifest
import cadquery as cq

from korrekt_mounting_profile import KorrektMountingProfile
from local_to_parent_location import LocalToParentLocation
from korrekt_mounting_machining import KorrektMountingMachining
from part_construction_error import PartConstructionError
from purchased_hardware_spec import HardwarePurchaseSpec


@dataclass(frozen=True)
class KorrektStation:
    """Keep caller-selected native CAD placements; do not invent adjustment or support spacing."""

    plate: object
    foot: object


@dataclass(frozen=True)
class KorrektComponentFeature:
    deck_part_ids: tuple[str, ...]
    stations: tuple[KorrektStation, ...]
    minimum_edge_margin_mm: float
    module: str = "korrekt.feature"

    def apply(self, assembly):
        from assemblies.specification import BuiltPurchasedHardware, ConstructionRequirementSpec

        purchases = tuple(self._purchase(item) for station in self.stations for item in (station.plate, station.foot))
        ids = tuple(item.hardware_id for item in purchases)
        existing = {item.hardware_id for item in assembly.spec.purchased_hardware}
        if not ids or len(set(ids)) != len(ids) or existing.intersection(ids):
            raise PartConstructionError("Korrekt stations need distinct, newly owned purchase IDs")
        for station in self.stations:
            for item, code in ((station.plate, "61854"), (station.foot, "70151")):
                if (item.manufacturer != "Hettich" or item.product_code != code or
                        item.hardware_asset_id != f"hettich_korrekt_{code}" or item.local_to_parent is None):
                    raise PartConstructionError("Korrekt station requires exact placed 61854 and 70151 purchases")
            self._validate_station(station)
        spec = replace(assembly.spec, purchased_hardware=assembly.spec.purchased_hardware+purchases)
        built = replace(assembly, spec=spec, purchased_hardware=assembly.purchased_hardware+tuple(
            BuiltPurchasedHardware(item, None) for item in purchases))
        result = KorrektMountingMachining().apply(built, self.deck_part_ids,
            tuple(station.plate.hardware_id for station in self.stations),
            minimum_edge_margin_mm=self.minimum_edge_margin_mm)
        new_joints = result.joints[len(assembly.joints):]
        affected = tuple(dict.fromkeys(joint.part_id for joint in new_joints))
        prefix = self.module.replace('.', '_')
        requirements = (
            ConstructionRequirementSpec(prefix+"_mounting", "Machine the sourced Korrekt mounting pattern",
                tuple(f"part:{name}" for name in affected),
                tuple(f"joint:{joint.joint_id}" for joint in new_joints), "operations"),
            ConstructionRequirementSpec(prefix+"_installation", "Install the owned foot and plate pairs",
                tuple(f"part:{name}" for name in affected)+tuple(f"hardware:{name}" for name in ids),
                (f"feature:{self.module}",), "operations"),
            ConstructionRequirementSpec(prefix+"_physical_fit",
                "Confirm plug/socket fit, screw engagement, top access, adjustment and deck support/load",
                tuple(f"part:{name}" for name in self.deck_part_ids)+tuple(f"hardware:{name}" for name in ids),
                basis="Sourced CAD and successful subtraction alone do not resolve these installation checks"),
        )
        declared = result.spec.requirements
        return replace(result, spec=replace(result.spec,
            requirements=declared+requirements if declared is not None else None))

    def register(self, project_root, result):
        """Scope future evidence to exactly these hardware and cut participants."""
        plate_ids = {station.plate.hardware_id for station in self.stations}
        joints = tuple(joint for joint in result.joints
                       if joint.joint_type == "korrekt_mounting" and joint.hardware_id in plate_ids)
        if {joint.hardware_id for joint in joints} != plate_ids:
            raise PartConstructionError("Build the current Korrekt feature before registering its participants")
        return CabinetFeatureManifest().register(project_root, result.spec.assembly_id, self.module, 30,
            affected_manufactured_part_paths=tuple(dict.fromkeys(joint.part_id for joint in joints)),
            affected_purchased_hardware_paths=tuple(item.hardware_id for station in self.stations
                                                    for item in (station.plate, station.foot)),
            qualified_joint_ids=tuple(joint.joint_id for joint in joints))

    def _validate_station(self, station):
        plate = LocalToParentLocation().build(station.plate.local_to_parent)
        axis = cq.Vector(*KorrektMountingProfile().socket_axis_xy_mm, 0).transform(
            cq.Matrix(plate.wrapped.Transformation()))
        foot = station.foot.local_to_parent
        origin = foot.origin_in_parent
        if (abs(axis.x-origin.x_mm) > 1e-6 or abs(axis.y-origin.y_mm) > 1e-6 or
                foot.axis_basis.local_z_in_parent.z < 0.999999 or origin.z_mm >= axis.z):
            raise PartConstructionError("Korrekt foot must be upright below its matching plate socket axis")

    def _purchase(self, item):
        purchase = item.purchase or HardwarePurchaseSpec(item.hardware_id, item.product_code, "piece", "item", ("item",))
        if (purchase.purchase_id != item.hardware_id or purchase.product_code != item.product_code or
                purchase.unit != "piece" or purchase.required_members != (purchase.member,) or
                not purchase.member or purchase.owner_levels_up != 0 or purchase.connection is not None):
            raise PartConstructionError("Each Korrekt article needs its own one-piece purchase identity")
        return replace(item, purchase=purchase)
