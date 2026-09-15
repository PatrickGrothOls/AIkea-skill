"""Scope: Measure referenced drawer installation parts in their common world frame."""
from local_to_parent_location import LocalToParentLocation


class DrawerLayoutGeometry:
    def __init__(self,visits):
        self.visits={"/".join(v.path):v for v in visits}

    def box(self,path):
        visit=self.visits[path]
        return visit.part.solid.val().located(LocalToParentLocation().build(visit.local_to_root)).BoundingBox()

    def check(self,stack):
        floor=self.box(stack['floor']);cap=self.box(stack['cap'])
        left,right=(self.box(p) for p in stack['opening_sides'])
        tolerance=stack.get('tolerance_mm',.25)
        problems=[];fronts=[]
        for drawer in stack['drawers']:
            owner=self.visits[drawer['path']].assembly
            fronts.append(self.box(drawer['front']))
            front_id=drawer['front'].split('part:')[-1]
            declared=[p for p in owner.spec.parts if p.role=='drawer_front']
            if len(declared)!=1 or declared[0].part_id!=front_id:
                problems.append('single_front: require exactly one declared structural drawer_front')
            sides=[p.split('part:')[-1] for p in drawer['sides']]
            for side in sides:
                if not any({front_id,side} <= set(j.participant_ids) for j in owner.joints):
                    problems.append('single_front: structural front must join directly to both box sides')
            if not any(r.part_id==front_id and r.operation_type=='surface_groove' for r in owner.spec.machining):
                problems.append('single_front: structural front must capture the bottom')
            front=fronts[-1]
            for panel in owner.spec.parts:
                if panel.part_id==front_id or panel.role=='drawer_front':continue
                other=self.box(drawer['path']+'/part:'+panel.part_id)
                if (other.ymax<=front.ymin+tolerance and other.zlen>front.zlen/2 and
                    min(other.xmax,front.xmax)-max(other.xmin,front.xmin)>front.xlen/2):
                    problems.append('single_front: an additional panel doubles the visible structural front')
            reveals=drawer['side_reveals_mm']
            actual=(front.xmin-left.xmax,right.xmin-front.xmax)
            if any(abs(a-b)>tolerance for a,b in zip(actual,reveals)):
                problems.append('frontage: front does not span the opening minus declared operating reveals')
            if any(g<0 for g in actual):problems.append('frontage: front crosses the cabinet opening')
        if fronts:
            gaps=(fronts[0].zmin-floor.zmax,
                  *(b.zmin-a.zmax for a,b in zip(fronts,fronts[1:])),cap.zmin-fronts[-1].zmax)
            requested=stack['operating_gaps_mm']
            if len(gaps)!=len(requested) or any(abs(a-b)>tolerance for a,b in zip(gaps,requested)):
                problems.append('compact_stack: actual floor/inter-drawer/cap gaps differ from intended operating clearances')
            # Five millimetres is a conservative default policy ceiling, not a
            # hardware-fit claim. Larger design gaps require a user exception.
            if any(g<=0 or g>5+tolerance for g in gaps):
                problems.append('compact_stack: default gaps must be positive and no greater than 5 mm')
            if any(f.xmin<max(floor.xmin,cap.xmin)-tolerance or
                   f.xmax>min(floor.xmax,cap.xmax)+tolerance or
                   f.ymin<floor.ymin-tolerance or f.ymax>cap.ymax+tolerance for f in fronts):
                problems.append('compact_stack: referenced floor/cap does not cover the drawer frontage depth')
        return tuple(problems)
