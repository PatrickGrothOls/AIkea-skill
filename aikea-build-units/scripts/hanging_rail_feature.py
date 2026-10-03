"""Scope: Add a cut-to-length rail, owned supports and real host-panel drilling."""
from dataclasses import dataclass, replace
import cadquery as cq
from hanging_rail_layout import HangingRailLayout
from hanging_rail_clearance import HangingRailClearance
from hanging_rail_profile import HangingRailProfile
from panel_machining_feature import PanelMachiningFeature
from purchased_hardware_spec import HardwarePurchaseSpec, PurchasedHardwareSpec


@dataclass(frozen=True)
class HangingRailFeature:
    layout: HangingRailLayout
    support_geometry: object = None
    support_asset_id: str = 'hettich-sl322-70664-drawing-preview'

    def apply(self, assembly):
        from assemblies.specification import BuiltPurchasedHardware, ConstructionRequirementSpec
        profile = HangingRailProfile()
        stations, length = self.layout.resolve(assembly, profile)
        name = self.layout.rail_id
        ids = (name, name+'_left_support', name+'_right_support')
        if set(ids).intersection(item.hardware_id for item in assembly.spec.purchased_hardware):
            raise ValueError('Hanging rail identities already exist in this assembly')
        if assembly.spec.requirements is None:
            raise ValueError('Declare construction requirements before adding a hanging rail')
        support = self.support_geometry if self.support_geometry is not None else profile.support_preview()
        purchases = []
        for identity, station in zip(ids[1:], stations):
            side_id, _, frame, _ = station
            spec = PurchasedHardwareSpec(identity, profile.manufacturer, profile.support_article,
                self.support_asset_id, frame,
                purchase=HardwarePurchaseSpec(identity, profile.support_article, 'piece', 'item',
                                               ('item',), mounting_fasteners_included=False),
                mounting_part_id=side_id)
            purchases.append(BuiltPurchasedHardware(spec, support))
        origin = stations[0][1]+cq.Vector(profile.end_allowance_mm, 0, 11.3)
        rail_frame = self.layout.frame(cq.Plane(origin=origin, xDir=(1, 0, 0), normal=(0, 0, 1)))
        rail = PurchasedHardwareSpec(name, profile.manufacturer, profile.rail_article,
            'hettich-30x15x0.6-cut-stock', rail_frame,
            purchase=HardwarePurchaseSpec(name, profile.rail_article, 'cut piece', 'rail', ('rail',)))
        purchases.append(BuiltPurchasedHardware(rail, profile.rail(length)))
        HangingRailClearance().validate(assembly, tuple(purchases))
        subjects = tuple('hardware:'+identity for identity in ids)
        requirements = (
            ConstructionRequirementSpec(name+'_fixings',
                'Install each SL 322 support with three 4 mm countersunk screws', subjects,
                tuple('machining:'+station[3].machining_id for station in stations), 'operations',
                profile.source_url),
            ConstructionRequirementSpec(name+'_cut_length',
                f'Cut one 30 x 15 x 0.6 mm oval rail to {length:g} mm; deburr both ends', subjects,
                basis='Inside width minus 7 mm; purchased stock length 5000 mm'),
            ConstructionRequirementSpec(name+'_screw_fit',
                'Confirm six purchased 4 mm countersunk screws, length, stock-specific pilot and load',
                subjects, basis=f'Pilots {self.layout.pilot_diameter_mm:g} x '
                f'{self.layout.pilot_depth_mm:g} mm; not a manufacturer pull-out/load rating'),
        )
        if self.support_geometry is None:
            requirements += (ConstructionRequirementSpec(name+'_source_cad',
                'Replace dimensioned support preview with exact imported SL 322 CAD', subjects,
                basis='Manufacturer drawing governs drilling; preview omits casting details'),)
        result = PanelMachiningFeature().apply(assembly, tuple(s[3] for s in stations), requirements)
        return replace(result, spec=replace(result.spec, purchased_hardware=result.spec.purchased_hardware+
                       tuple(p.spec for p in purchases)), purchased_hardware=result.purchased_hardware+tuple(purchases))

    def cut_list(self, assembly):
        profile = HangingRailProfile()
        _, length = self.layout.resolve(assembly, profile)
        return {'part_id': self.layout.rail_id, 'manufacturer': profile.manufacturer,
                'product_code': profile.rail_article, 'quantity': 1, 'cut_length_mm': length,
                'stock_length_mm': profile.stock_length_mm, 'section_mm': [30, 15, .6]}
