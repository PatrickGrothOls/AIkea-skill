"""Scope: Resolve broad-face access from supported joint cutters and participant frames."""
import cadquery as cq
from local_to_parent_location import LocalToParentLocation
from part_outside_face_plane import PartOutsideFacePlaneResolver
from miter_edge_mate import MiterEdgeMate


class PanelJointSetupFaces:
    def resolve(self,spec,joint):
        parts={p.part_id:p for p in spec.parts}
        if joint.joint_type=='cabineo':
            source=parts[joint.source_part_id];target=parts[joint.target_part_id]
            locations=LocalToParentLocation()
            transform=locations.build(target.local_to_parent).inverse*locations.build(source.local_to_parent)
            sign=1 if joint.source_edge.startswith('>') else -1
            axis=tuple(sign if name==joint.source_edge[-1] else 0 for name in 'XYZ')
            start=cq.Vertex.makeVertex(0,0,0).located(transform).Center()
            end=cq.Vertex.makeVertex(*axis).located(transform).Center()
            vector=end-start
            faces=set() if abs(vector.x)>1e-7 or abs(vector.y)>1e-7 or abs(abs(vector.z)-1)>1e-7 else {'<Z' if vector.z>0 else '>Z'}
            return {source.part_id:{joint.source_face}&{'<Z','>Z'},target.part_id:faces}
        if joint.joint_type=='korrekt_mounting':
            part=parts[joint.part_id]
            plate=next(p for p in spec.purchased_hardware if p.hardware_id==joint.hardware_id)
            a=part.local_to_parent.axis_basis.local_z_in_parent
            b=plate.local_to_parent.axis_basis.local_z_in_parent
            parallel=abs(abs(a.x*b.x+a.y*b.y+a.z*b.z)-1)<1e-7
            # The registered Korrekt cutter contains only complete through bores.
            return {part.part_id:{'<Z','>Z'} if parallel else set()}
        if joint.joint_type=='equal_thickness_miter':
            return self._miter(tuple(parts[p] for p in joint.participant_ids))
        return {p:set() for p in joint.participant_ids}

    def _miter(self,parts):
        locations=LocalToParentLocation();planes=PartOutsideFacePlaneResolver()
        a,b=(planes.resolve(p,locations.build(p.local_to_parent)) for p in parts)
        mate=MiterEdgeMate.from_planes(a.center,a.normal,b.center,b.normal)
        result={}
        for part,sign in zip(parts,(1,-1)):
            axis=part.local_to_parent.axis_basis.local_z_in_parent
            z=sign*sum(n*v for n,v in zip(mate.plane_normal,(axis.x,axis.y,axis.z)))
            # Along this outward broad-face ray, the removed half-space stays
            # removed: no undercut. This does not qualify cutter reach or CAM.
            result[part.part_id]={'<Z','>Z'} if abs(z)<1e-7 else {'>Z' if z>0 else '<Z'}
        return result
