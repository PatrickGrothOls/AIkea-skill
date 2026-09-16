"""Scope: Export the unchanged v2 manufactured parts and current declared-face audit separately from old evidence."""
from pathlib import Path
from functools import partial
import json,sys
package=Path.cwd();root=package/'local-evidence/fresh-project'
sys.path[:0]=[str(package/(name+'/scripts')) for name in
    ('aikea-review-unit','aikea-build-units','aikea-build-drawers','aikea-build-doors','aikea-add-lighting','aikea')]
from OCP.OSD import OSD_Parallel,OSD_ThreadPool
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from purchased_hardware_hydrator import PurchasedHardwareHydrator
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from construction_input_fingerprint import ConstructionInputFingerprinter
from panel_setup_checker import PanelSetupChecker
from physical_item_counter import PhysicalItemCounter
from drawer_layout_policy_checker import DrawerLayoutPolicyChecker
from construction_requirement_checker import ConstructionRequirementChecker
from review_evidence import AdditionalEvidence


class CurrentPartExport:
    def run(self):
        OSD_Parallel.SetUseOcctThreads_s(True)
        pool=OSD_ThreadPool.DefaultPool_s(1);pool.Init(1);pool.SetNbDefaultThreadsToLaunch(1)
        loader=GeneratedAssemblyBuilderLoader();fingerprint=ConstructionInputFingerprinter()
        initial=fingerprint.source_inputs(root)
        built=loader.load_assembly(root,'furniture_01')
        built=loader.runtime.execute(root,partial(PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate,root,built))
        visits=loader.walk(root,built);current=fingerprint.build(root,visits)
        expected=json.loads((root/'reviews/grass-closed-diagnostic-v2.json').read_text())['construction_sha256']
        if current!=expected:raise ValueError('Current part export differs from corrected v2 construction')
        output=root/'deliverables/grass-v2'
        (output/'reviews').mkdir(parents=True,exist_ok=True)
        setups=[{'path':list(v.path),**PanelSetupChecker().check(v.assembly)} for v in visits if hasattr(v,'assembly')]
        report=dict(construction_sha256=current,fabrication_ready=False,assemblies=setups,
            drawer_layout_gate=DrawerLayoutPolicyChecker().check(root,visits).as_dict())
        (output/'reviews/panel-setup-audit.json').write_text(json.dumps(report,indent=2)+'\n')
        print('Current setup statuses',[(s['path'],s['status']) for s in setups],flush=True)
        AdditionalEvidence().export_parts(output,visits)
        counts=PhysicalItemCounter().count(visits)
        (output/'manufacturing/item-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
        requirements=ConstructionRequirementChecker().check(visits,{})
        (output/'reviews/unresolved-requirements.json').write_text(json.dumps([r.as_dict() for r in requirements],indent=2)+'\n')
        fingerprint.require_unchanged_sources(root,initial)
        print('Manufactured exports complete',counts['totals'],output,flush=True)


if __name__=='__main__':
    CurrentPartExport().run()
