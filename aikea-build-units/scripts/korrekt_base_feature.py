"""Scope: Attach default floor-standing Korrekt stations to declared deck/kickboard modules."""
from dataclasses import dataclass
from korrekt_base_layout import KorrektBaseLayout
from korrekt_component_feature import KorrektComponentFeature, KorrektStation
from korrekt_mounting_cutter import KorrektMountingCutter
from part_construction_error import PartConstructionError
from purchased_hardware_spec import HardwarePurchaseSpec, PurchasedHardwareSpec


@dataclass(frozen=True)
class KorrektBaseFeature:
    layout: KorrektBaseLayout
    station_spans_mm: tuple[tuple[float, float], ...] = ()
    # Read from the exact 70151 source. This frozen CAD pose is never scaled or articulated.
    native_foot_height_mm: float = 80.0

    def feature(self, spec):
        self.layout.check_adjustment_range()
        if self.layout.support_height_mm < self.native_foot_height_mm-1e-6:
            raise PartConstructionError(
                f"The untouched 70151 CAD pose is 80 mm high and intrudes into the deck at "
                f"{self.layout.support_height_mm:g} mm. Keep the room envelope and resolve deck "
                "stock or obtain a verified adjusted foot pose; do not scale or replace it with braces.")
        stations = []
        spans = self.station_spans_mm or tuple((m.start_x_mm,m.end_x_mm) for m in spec.modules)
        for start,end in spans:
            axes = self.layout.station_axes(start,end,spec.depth_mm,
                spec.plinth_recess_mm+self.layout.deck_thickness_mm)
            for x,y in axes:
                index = len(stations)+1
                origin = KorrektMountingCutter().placement((x,y),self.layout.support_height_mm,0).toTuple()[0]
                plate = self._purchase(f"plate_{index:02d}","61854",origin,False)
                foot = self._purchase(f"foot_{index:02d}","70151",(x,y,-self.layout.source_foot_floor_z_mm),True)
                stations.append(KorrektStation(plate,foot))
        return KorrektComponentFeature(tuple(p.part_id for p in spec.parts if p.role == "base_deck"),
            tuple(stations),self.layout.minimum_plate_edge_margin_mm)

    def _purchase(self, identity, article, origin, included):
        from assemblies.specification import LocalToParentPlacement, Point3D, IDENTITY_AXIS_BASIS
        return PurchasedHardwareSpec(identity,"Hettich",article,"hettich_korrekt_"+article,
            LocalToParentPlacement(Point3D(*origin),IDENTITY_AXIS_BASIS),
            purchase=HardwarePurchaseSpec(identity,article,"piece","item",("item",),
                mounting_fasteners_included=included))
