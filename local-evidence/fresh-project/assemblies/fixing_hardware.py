"""Scope: Retain installation screws as physical items with explicit simplified geometry."""
from dataclasses import replace
import cadquery as cq
from assemblies.design_primitives import P
from local_to_parent_location import LocalToParentLocation


class FixingHardware:
    def apply(self,built):
        items=list(built.purchased_hardware)
        for request in built.spec.machining:
            selection=self._selection(request)
            if selection is None:
                continue
            article,length,web=selection
            part=built.spec.part(request.part_id)
            # A 2.8mm illustrative core deliberately omits unverified thread/root
            # geometry. The purchase diameter remains4mm; this is not fit proof.
            screw=cq.Solid.makeCylinder(1.4,length,cq.Vector(0,0,-web)).fuse(
                cq.Solid.makeCylinder(3.75,2.8,cq.Vector(0,0,-web-2.8)))
            frame=LocalToParentLocation().build(request.surface_to_part)
            for n,hole in enumerate(request.holes):
                shape=screw.translate((hole.x_mm,hole.y_mm,0)).located(frame)
                items.append(P.hardware(f'{request.machining_id}_screw_{n:02d}','Newfix' if length==14 else 'SPAX',article,
                    shape,part.local_to_parent,part.part_id))
        return replace(built,spec=replace(built.spec,purchased_hardware=tuple(h.spec for h in items)),purchased_hardware=tuple(items))

    def _selection(self,request):
        if request.operation_type!='surface_holes':
            return None
        if request.machining_id.endswith('_rail_pilots'):
            return '2145501 / Ø4×14',14,1
        if request.machining_id.endswith('_runner_pilots'):
            # Drawer is machined from its inner face; screw enters the opposite
            # face. Its placement is resolved separately below, not guessed here.
            return None
        if request.machining_id.endswith('_mounting_clearance'):
            return ('0201010400605 / Ø4×60',60,0) if '_left_' in request.machining_id else ('0201010400503 / Ø4×50',50,0)
        return None

    def moving_screws(self,built):
        items=list(built.purchased_hardware)
        screw=cq.Solid.makeCylinder(1.4,14,cq.Vector(0,0,-1)).fuse(
            cq.Solid.makeCylinder(3.75,2.8,cq.Vector(0,0,-3.8)))
        for hand in ('left','right'):
            part=built.spec.part(hand+'_wall')
            xs=(21,149,275) if hand=='left' else (400-37,400-165,400-291)
            for n,x in enumerate(xs):
                items.append(P.hardware(f'{hand}_moving_screw_{n:02d}','Newfix','2145501 / Ø4×14',
                    screw.translate((x,35,0)),part.local_to_parent,part.part_id))
        return replace(built,spec=replace(built.spec,purchased_hardware=tuple(h.spec for h in items)),purchased_hardware=tuple(items))
