"""Scope: Run shared full-tree export and evidence tools in one serial CAD process."""
from pathlib import Path
import sys,json,faulthandler,time
from functools import partial
root=Path('local-evidence/fresh-project').resolve(); package=Path('.').resolve()
sys.path[:0]=[str(package/(name+'/scripts')) for name in ('aikea-review-unit','aikea-build-units','aikea-build-drawers','aikea-build-doors','aikea-add-lighting','aikea')]
faulthandler.dump_traceback_later(90,repeat=True)
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from physical_item_counter import PhysicalItemCounter
from panel_setup_checker import PanelSetupChecker
from construction_input_fingerprint import ConstructionInputFingerprinter
from construction_position_evidence import ConstructionPositionEvidence
from construction_envelope_authority import ConstructionEnvelopeAuthority
from construction_tree_checker import ConstructionTreeChecker
from construction_requirement_checker import ConstructionRequirementChecker
from review_evidence import AdditionalEvidence
from drawer_layout_policy_checker import DrawerLayoutPolicyChecker
from assembly_feature_review import AssemblyFeatureReviewContext
from assembly_tree_review_plan import AssemblyTreeReviewPlan, AssemblyReviewMotion
from lighting_component_review import LightingComponentReview
from riex_nc70_door_review_feature import RiexNc70DoorReviewFeature
from OCP.OSD import OSD_Parallel, OSD_ThreadPool
OSD_Parallel.SetUseOcctThreads_s(True)
pool=OSD_ThreadPool.DefaultPool_s(1);pool.Init(1);pool.SetNbDefaultThreadsToLaunch(1)
print('OCCT thread pool',pool.NbThreads(),pool.NbDefaultThreadsToLaunch(),flush=True)
import cadquery as cq
loader=GeneratedAssemblyBuilderLoader();fingerprint=ConstructionInputFingerprinter();sources=fingerprint.source_inputs(root)
print('Building complete fresh tree',flush=True)
built=loader.load_assembly(root,'furniture_01')
print('Hydrating exact base source hardware',flush=True)
built=loader.runtime.execute(root,partial(PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate,root,built))
visits=loader.walk(root,built)
DrawerLayoutPolicyChecker().require(root,visits)
parts=AssemblyTreeReviewGeometry().build(visits,{})
print('Exporting full inspection GLB with current geometry',flush=True)
CadQueryGlbExporter().export('furniture_01',parts,root/'reviews/furniture_01.glb')
print('GLB exported',len(parts),flush=True)
fingerprint.require_unchanged_sources(root,sources)
envelope,allowances,source=ConstructionEnvelopeAuthority().read(root,'furniture_01')
print('Preparing shared lighting and open-door review contributions',flush=True)
# A runtime callback keeps project-owned imports inside the shared module context.
def review_plans():
    from assemblies.cabinet_builder import CabinetBuilder
    from door_host import DoorHost, DoorHostSpec
    from door_hinge_side import DoorHingeSide
    from door_hinge_plan import DoorHingePlanner
    from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
    lights=[];doors=[]
    for visit in visits:
        if not hasattr(visit,'assembly') or not visit.assembly.spec.assembly_id.startswith('cabinet_'): continue
        recipe=CabinetBuilder(int(visit.assembly.spec.assembly_id[-2:])-1)
        context=AssemblyFeatureReviewContext(root,visit.path,visit.assembly)
        lights.extend(LightingComponentReview(p).plan(context,'on') for p in recipe.lighting_plans(visit.assembly.spec))
        host=DoorHost(visit.assembly.spec,DoorHostSpec('door_panel','left_side'),DoorHingeSide.LEFT)
        plan=DoorHingePlanner().plan(host,RIEX_NC70_FULL_OVERLAY,blocked_reservations=recipe._reservations(visit.assembly.spec))
        doors.append(RiexNc70DoorReviewFeature(plan).plan(context,'open'))
    return lights,doors
lights,doors=loader.runtime.execute(root,review_plans)
for state,features in (('lit',lights),('open',lights+doors)):
    plan=AssemblyTreeReviewPlan(hidden_paths=tuple(p for f in features for p in f.hidden_paths),overlays=tuple(o for f in features for o in f.overlays))
    review_parts=AssemblyTreeReviewGeometry().build(visits,{},plan)
    CadQueryGlbExporter().export('furniture_01',review_parts,root/('reviews/furniture_01-'+state+'.glb'))
    print('Shared review export',state,len(review_parts),flush=True)

assembly=cq.Assembly(name='furniture_01')
for part in parts: assembly.add(part.solid,name=part.name,loc=part.location)
assembly.save(str(root/'reviews/furniture_01.step'),exportType='STEP')
print('STEP exported',flush=True)
(root/'manufacturing').mkdir(exist_ok=True)
counts=PhysicalItemCounter().count(visits);(root/'manufacturing/item-counts.json').write_text(json.dumps(counts,indent=2))
setups=[{'path':list(v.path),**PanelSetupChecker().check(v.assembly)} for v in visits if hasattr(v,'assembly')]
(root/'reviews/panel-setup-audit.json').write_text(json.dumps({'assemblies':setups,'construction_sha256':fingerprint.build(root,visits),'fabrication_ready':False},indent=2))
print('Inventory and setup report exported',counts['totals'],flush=True)
AdditionalEvidence().export_parts(root,visits)
print('All manufactured part STEP/DXF files exported',flush=True)

AdditionalEvidence().front_travel(root,visits,review_parts)
print('Full front pullout envelope checked',flush=True)
print('Running complete closed-geometry check',flush=True)
position=ConstructionPositionEvidence().write(root,visits,envelope,allowances,source)
(root/'reviews/furniture_01.geometry-check.json').write_text(json.dumps(position,indent=2))
checks=ConstructionTreeChecker().check(visits,set())+ConstructionRequirementChecker().check(visits,{})
(root/'reviews/construction-checks.json').write_text(json.dumps([c.as_dict() for c in checks],indent=2))
print('Finished shared checks',position['status'],flush=True)
faulthandler.cancel_dump_traceback_later()
