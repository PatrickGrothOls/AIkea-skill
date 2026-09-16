"""Scope: Export explicitly incomplete closed-fit diagnostics, retaining the failed completion gate."""
from pathlib import Path
from functools import partial
import json,sys,faulthandler

package=Path.cwd();root=package/'local-evidence/fresh-project'
sys.path[:0]=[str(package/(name+'/scripts')) for name in
    ('aikea-review-unit','aikea-build-units','aikea-build-drawers','aikea-build-doors','aikea-add-lighting','aikea')]
from OCP.OSD import OSD_Parallel,OSD_ThreadPool
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from assembly_tree_review_plan import AssemblyTreeReviewPlan
from assembly_feature_review import AssemblyFeatureReviewContext
from lighting_component_review import LightingComponentReview
from cadquery_glb_exporter import CadQueryGlbExporter
from drawer_layout_policy_checker import DrawerLayoutPolicyChecker
from physical_item_counter import PhysicalItemCounter
from panel_setup_checker import PanelSetupChecker
from check_grass_closed_contacts import ClosedContactsCheck
from construction_input_fingerprint import ConstructionInputFingerprinter
from construction_position_evidence import ConstructionPositionEvidence
from construction_envelope_authority import ConstructionEnvelopeAuthority
from construction_tree_checker import ConstructionTreeChecker
from export_current_parts import CurrentPartExport


class ClosedDiagnosticExport:
    def run(self):
        OSD_Parallel.SetUseOcctThreads_s(True)
        pool=OSD_ThreadPool.DefaultPool_s(1);pool.Init(1);pool.SetNbDefaultThreadsToLaunch(1)
        faulthandler.dump_traceback_later(90,repeat=True)
        loader=GeneratedAssemblyBuilderLoader();fingerprint=ConstructionInputFingerprinter()
        source_state=fingerprint.source_inputs(root)
        built=loader.load_assembly(root,'furniture_01')
        built=loader.runtime.execute(root,partial(PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate,root,built))
        visits=loader.walk(root,built)
        gate=DrawerLayoutPolicyChecker().check(root,visits)
        lights=loader.runtime.execute(root,partial(self.lights,visits))
        plan=AssemblyTreeReviewPlan(overlays=tuple(o for f in lights for o in f.overlays))
        parts=AssemblyTreeReviewGeometry().build(visits,{},plan)
        output=root/'reviews/furniture_01-grass-closed-diagnostic-v3.glb'
        CadQueryGlbExporter().export('furniture_01',parts,output)
        fingerprint.require_unchanged_sources(root,source_state)
        counts=PhysicalItemCounter().count(visits)
        setups=[{'path':list(v.path),**PanelSetupChecker().check(v.assembly)} for v in visits if hasattr(v,'assembly')]
        record=dict(status='CLOSED_DIAGNOSTIC_ONLY',fabrication_ready=False,complete_review=False,
            construction_sha256=fingerprint.build(root,visits),drawer_layout_gate=gate.as_dict(),
            source_pair_registration='Native source datums matched; overlapping clip bodies remain unqualified',
            motion='No open-position or moving-arm proof. Widths fit closed source only, not certified maximum travel width.',
            supports='Calibrated birch stock/lamination and screw holding are unqualified.',
            load='User retains616.75mm leaves provisionally;600mm reference chart qualification remains open.',
            counts=counts,panel_setups=setups,render_items=len(parts),
            emitters=sum('light_source__' in p.name for p in parts),artifact=str(output))
        (root/'reviews/grass-closed-diagnostic-v3.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k not in ('counts','panel_setups')},indent=2),flush=True)
        closed=ClosedContactsCheck()
        result=closed.evaluate(visits)
        closed.export_step(visits)
        fingerprint.require_unchanged_sources(root,source_state)
        print('Closed source-versus-wood check',result['status'],flush=True)
        envelope,allowances,source=ConstructionEnvelopeAuthority().read(root,'furniture_01')
        position=ConstructionPositionEvidence().write(root,visits,envelope,allowances,source)
        (root/'reviews/grass-v3-whole-tree-position.json').write_text(json.dumps(position,indent=2)+'\n')
        checks=ConstructionTreeChecker().check(visits)
        (root/'reviews/grass-v3-applied-operations.json').write_text(json.dumps([c.as_dict() for c in checks],indent=2)+'\n')
        print('Whole-tree closed status',position['status'],flush=True)
        CurrentPartExport().export(visits,record['construction_sha256'])
        fingerprint.require_unchanged_sources(root,source_state)
        faulthandler.cancel_dump_traceback_later()

    def lights(self,visits):
        from assemblies.cabinet_builder import CabinetBuilder
        contributions=[]
        for visit in visits:
            if not hasattr(visit,'assembly') or not visit.assembly.spec.assembly_id.startswith('cabinet_'):
                continue
            recipe=CabinetBuilder(int(visit.assembly.spec.assembly_id[-2:])-1)
            context=AssemblyFeatureReviewContext(root,visit.path,visit.assembly)
            contributions.extend(LightingComponentReview(p).plan(context,'on')
                for p in recipe.lighting_plans(visit.assembly.spec))
        return contributions


if __name__=='__main__':
    ClosedDiagnosticExport().run()
