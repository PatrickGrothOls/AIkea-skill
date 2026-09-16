"""Scope: Check exact closed GRASS bodies against the current wood and export matching native STEP."""
from pathlib import Path
from functools import partial
import json,sys
package=Path.cwd();root=package/'local-evidence/fresh-project'
sys.path[:0]=[str(package/(name+'/scripts')) for name in
    ('aikea-review-unit','aikea-build-units','aikea-build-drawers','aikea-build-doors','aikea-add-lighting','aikea')]
import cadquery as cq
from OCP.OSD import OSD_Parallel,OSD_ThreadPool
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from construction_input_fingerprint import ConstructionInputFingerprinter
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from local_to_parent_location import LocalToParentLocation


class ClosedContactsCheck:
    def run(self):
        OSD_Parallel.SetUseOcctThreads_s(True)
        pool=OSD_ThreadPool.DefaultPool_s(1);pool.Init(1);pool.SetNbDefaultThreadsToLaunch(1)
        loader=GeneratedAssemblyBuilderLoader();fingerprint=ConstructionInputFingerprinter()
        initial=fingerprint.source_inputs(root)
        built=loader.load_assembly(root,'furniture_01')
        built=loader.runtime.execute(root,partial(PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate,root,built))
        visits=loader.walk(root,built);current=fingerprint.build(root,visits)
        expected=json.loads((root/'reviews/grass-closed-diagnostic-v2.json').read_text())['construction_sha256']
        if current!=expected:raise ValueError('closed-contact construction differs from exported diagnostic')
        self.evaluate(visits)
        self.export_step(visits)
        fingerprint.require_unchanged_sources(root,initial)

    def evaluate(self,visits):
        current=ConstructionInputFingerprinter().build(root,visits)
        panels=[];hardware=[];locations=LocalToParentLocation()
        for visit in visits:
            item=getattr(visit,'part',None)
            if item is not None:
                panels.append(('/'.join(visit.path),item.solid.val().located(locations.build(visit.local_to_root))))
            item=getattr(visit,'hardware',None)
            if item is not None and item.spec.product_code in ('F028122660','F058139748'):
                hardware.append(('/'.join(visit.path),item.solid.val().located(locations.build(visit.local_to_root))))
        findings=[];tested=0
        for identity,body in hardware:
            bounds=body.BoundingBox()
            for panel,wood in panels:
                other=wood.BoundingBox()
                if not all(getattr(bounds,a+'max')>getattr(other,a+'min') and
                           getattr(other,a+'max')>getattr(bounds,a+'min') for a in 'xyz'):
                    continue
                volume=body.intersect(wood).Volume();tested+=1
                if volume>1e-3:findings.append(dict(hardware=identity,panel=panel,overlap_mm3=volume))
        result=dict(scope='Exact unchanged CLOSED manufacturer bodies versus all machined wood only',
            status='FAIL' if findings else 'PASS',construction_sha256=current,hardware_bodies=len(hardware),
            wood_parts=len(panels),exact_intersections=tested,findings=findings,
            excluded='Opening/moving-arm path, hardware-to-hardware engagement and machining/load qualification')
        (root/'reviews/grass-closed-wood-contact-v2.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2),flush=True)
        return result

    def export_step(self,visits):
        assembly=cq.Assembly(name='furniture_01_grass_closed_provisional')
        for part in AssemblyTreeReviewGeometry().build(visits,{}):
            assembly.add(part.solid,name=part.name,loc=part.location)
        output=root/'reviews/furniture_01-grass-closed-provisional-v2.step'
        assembly.save(str(output),exportType='STEP')
        print('Matching provisional STEP exported',output,flush=True)


if __name__=='__main__':
    ClosedContactsCheck().run()
