"""Scope: Export part files and conservatively check full-width front pullout using shared tools."""
import json
from pathlib import Path
import cadquery as cq
from blank_sheet_builder import BlankSheetBuilder
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from furniture_geometry_check import FurnitureGeometryCheck
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart


class AdditionalEvidence:
    def export_parts(self,root,visits):
        directory=root/'manufacturing/parts';directory.mkdir(parents=True,exist_ok=True)
        records=[]
        for item in FabricationTreeEvidenceBuilder().build(visits).parts:
            base=directory/item.path.replace('/','__')
            cq.exporters.export(item.part.solid,str(base.with_suffix('.step')))
            spec=item.part.spec
            outline=tuple((p.x_mm,p.height_mm) for p in spec.outline_mm)
            blank=BlankSheetBuilder(outline,1) if outline else BlankSheetBuilder.rectangle(*spec.local_size_mm[:2],1)
            cq.exporters.export(blank.build().faces('<Z'),str(base.with_suffix('.dxf')))
            records.append({'path':item.path,'stock':spec.material_id,'size_mm':spec.local_size_mm,
                            'drawing':'Blank perimeter only; machining remains in assembly operations/STEP.'})
        (root/'manufacturing/part-manifest.json').write_text(json.dumps(records,indent=2))

    def front_travel(self,root,visits,open_parts):
        checker=FurnitureGeometryCheck();records=[]
        envelope=cq.Workplane('XY').box(6000,2500,3000,centered=False).translate((-1500,-1000,0))
        candidates=tuple(p for p in open_parts if any(t in p.name for t in ('door_panel','hinge','side','shelf','support')))
        for visit in visits:
            if not hasattr(visit,'part') or visit.part.spec.part_id!='front_wall':continue
            w,h,t=visit.part.spec.local_size_mm
            sweep=MockupPart('/'.join(visit.path)+'__400mm_pullout_envelope',
                BlankSheetBuilder.rectangle(w,h,t+400).build(),
                LocalToParentLocation().build(visit.local_to_root),(1,0,0,1))
            problems=[]
            for obstacle in candidates:
                if not checker._boxes_overlap(sweep.placed_shape().BoundingBox(),obstacle.placed_shape().BoundingBox()):continue
                result=checker.check((sweep,obstacle),envelope)
                problems.extend(result['overlaps']+result['uncertain_intersections'])
            records.append({'drawer':list(visit.path[:-1]),'status':'PASS' if not problems else 'FAIL',
                            'problems':problems})
        (root/'reviews/front-pullout-check.json').write_text(json.dumps({'drawers':records,
            'scope':'Conservative full400mm structural-front swept envelope against exact fully open doors/hinges and static sides/shelves. Door-opening arc and runner-stage kinematics remain separate.'},indent=2))
