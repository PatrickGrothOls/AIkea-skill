"""Scope: Display paired Cabineo purchases using explicitly illustrative seated envelopes."""
from dataclasses import replace
import cadquery as cq
from cabineo_connector_layout import CabineoConnectorLayout
from cabineo_cutter_placement import CabineoCutterPlacement
from cabineo_profile import NON_BOTTOM_CABINEO
from assemblies.specification import HardwarePurchaseSpec, ConnectionPurchaseSpec
from assemblies.design_primitives import P


class ConnectorHardware:
    def apply(self,built):
        items=list(built.purchased_hardware)
        layout=CabineoConnectorLayout();placer=CabineoCutterPlacement()
        p=NON_BOTTOM_CABINEO
        bores=[cq.Solid.makeCylinder(7.25,10,cq.Vector(0,c,0.25)) for c in p.pocket_centers_mm]
        body=bores[0].fuse(*bores[1:]).intersect(cq.Solid.makeBox(15,33,10.5,cq.Vector(-7.5,0,0)))
        sleeve=cq.Solid.makeCylinder(4.4,12,cq.Vector(0,0,5),cq.Vector(0,-1,0)).cut(
            cq.Solid.makeCylinder(3,12,cq.Vector(0,0,5),cq.Vector(0,-1,0)))
        for joint in built.joints:
            if joint.joint_type!='cabineo':
                continue
            source=built.spec.part(joint.source_part_id)
            for index,position in enumerate(layout.positions(joint,source),1):
                for kind,shape,manufacturer,article,parent in (
                        ('connector',body,'Lamello','Cabineo 8 M6 - SKU qualification open',joint.source_part_id),
                        ('insert',sleeve,'Häfele','267.91.314',joint.target_part_id)):
                    name=f'{joint.joint_id}_{index}_{kind}'
                    shape_local=placer.translate(placer.orient(shape,joint.source_face,joint.source_edge),
                        joint.source_face,joint.source_edge,position,source.local_size_mm[2],layout.edge_position(joint.source_edge,source))
                    purchase=HardwarePurchaseSpec(name,article,'piece','item',('item',),
                        connection=ConnectionPurchaseSpec(joint.joint_id,index,kind))
                    items.append(P.hardware(name,manufacturer,article,shape_local,source.local_to_parent,parent,purchase))
        return replace(built,spec=replace(built.spec,purchased_hardware=tuple(h.spec for h in items)),purchased_hardware=tuple(items))
