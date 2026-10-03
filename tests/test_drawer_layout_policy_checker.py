"""Scope: Enforce real drawer frontage/stack relationships and user-only exceptions."""
import json
from types import SimpleNamespace as N
import cadquery as cq
from drawer_layout_policy_checker import DrawerLayoutPolicyChecker
from construction_input_fingerprint import ConstructionInputFingerprinter


class LayoutFixture:
    def __init__(self):
        self.root='furniture_01/cabinet_01';self.drawer=self.root+'/drawer_01'
        self.frame=N(origin_in_parent=N(x_mm=0,y_mm=0,z_mm=0),axis_basis=N(
            local_x_in_parent=N(x=1,y=0,z=0),local_z_in_parent=N(x=0,y=0,z=1)))
        self.visits=[]
        for name,size,origin in (('floor',(566,416,16),(16,0,0)),('cap',(564,410,16),(17,2,166.5)),
                                ('left',(16,416,500),(0,0,0)),('right',(16,416,500),(582,0,0))):
            self.add(self.root,name,size,origin)
        front=self.add(self.drawer,'front',(562,16,144.5),(18,2,19),'drawer_front')
        self.add(self.drawer,'left_wall',(16,384,144.5),(53.7,18,19),'drawer_side')
        self.add(self.drawer,'right_wall',(16,384,144.5),(528.3,18,19),'drawer_side')
        self.owner=N(spec=N(assembly_id='drawer_01',purpose='drawer',parts=(front,)),
            joints=tuple(N(participant_ids=('front',side)) for side in ('left_wall','right_wall')),
            )
        self.owner.spec.machining=(N(part_id='front',operation_type='surface_groove'),)
        self.visits.extend((N(path=tuple(self.drawer.split('/')),assembly=self.owner,local_to_root=self.frame),
                            N(path=tuple(self.root.split('/')),local_to_root=self.frame,
                              assembly=N(spec=N(assembly_id='cabinet_01',purpose='cabinet'),joints=()))))
        self.clearance={'path':self.drawer,'status':'PASS','method':'full_travel_sweep','travel_mm':400,
            'constraint_paths':[self.root+'/part:left',self.root+'/part:right'],
            'obstruction_deductions_mm':[0,0],'fit_clearances_mm':[2,2],
            'support_offsets_mm':[25,25],'runner_installation_widths_mm':[12.7,12.7]}
        self.stack={'cabinet':self.root,'floor':self.root+'/part:floor','cap':self.root+'/part:cap',
            'opening_sides':[self.root+'/part:left',self.root+'/part:right'],'operating_gaps_mm':[3,3],
            'drawers':[{'path':self.drawer,'front':self.drawer+'/part:front',
                        'sides':[self.drawer+'/part:left_wall',self.drawer+'/part:right_wall'],'side_reveals_mm':[2,2]}]}

    def add(self,owner,name,size,origin,role='panel'):
        spec=N(part_id=name,role=role)
        solid=cq.Workplane('XY').box(*size,centered=False).translate(origin)
        self.visits.append(N(path=tuple((owner+'/part:'+name).split('/')),part=N(spec=spec,solid=solid),local_to_root=self.frame))
        return spec

    def write(self,root):
        path=root/'assemblies/drawer-layout-policy.json';path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({'schema_version':1,'stacks':[self.stack]}))
        (root/'assemblies/drawer-travel-clearance.json').write_text(json.dumps({'schema_version':1,
            'construction_sha256':ConstructionInputFingerprinter().build(root,self.visits),
            'drawers':[self.clearance]}))


class TestDrawerLayoutPolicy:
    def test_accepts_actual_single_front_and_compact_floor_cap(self,tmp_path):
        f=LayoutFixture();f.write(tmp_path)
        assert DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_missing_policy_blocks_installed_drawer(self,tmp_path):
        assert not DrawerLayoutPolicyChecker().check(tmp_path,LayoutFixture().visits).passed

    def test_compact_check_runs_without_travel_proof(self,tmp_path):
        f=LayoutFixture();f.write(tmp_path)
        (tmp_path/'assemblies/drawer-travel-clearance.json').unlink()
        checker=DrawerLayoutPolicyChecker()
        assert checker.check(tmp_path,f.visits,compact_only=True).passed
        assert not checker.check(tmp_path,f.visits).passed
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:front':
                v.part.solid=v.part.solid.translate((0,0,40))
        assert any('compact_stack' in p for p in checker.check(tmp_path,f.visits).problems)
        assert not checker.check(tmp_path,f.visits,compact_only=True).passed

    def test_tall_empty_floor_gap_fails_even_if_declared_as_intent(self,tmp_path):
        f=LayoutFixture()
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:front':v.part.solid=v.part.solid.translate((0,0,80))
        f.stack['operating_gaps_mm']=[83,-77];f.write(tmp_path)
        check=DrawerLayoutPolicyChecker().check(tmp_path,f.visits)
        assert not check.passed and any('compact_stack' in p for p in check.problems)

    def test_narrow_box_front_does_not_satisfy_visible_frontage(self,tmp_path):
        f=LayoutFixture()
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:front':
                v.part.solid=cq.Workplane('XY').box(458.6,16,144.5,centered=False).translate((69.7,2,19))
        f.write(tmp_path)
        assert any('frontage' in p for p in DrawerLayoutPolicyChecker().check(tmp_path,f.visits).problems)

    def test_added_fascia_needs_user_provenance(self,tmp_path):
        f=LayoutFixture();f.owner.spec.parts+=(N(part_id='fascia',role='drawer_front'),)
        f.stack['user_requested_exceptions']=[{'rule':'single_front','requested_by':'agent',
            'request_quote':'I chose a fascia','request_reference':'design note'}];f.write(tmp_path)
        assert not DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed
        f.stack['user_requested_exceptions'][0].update(requested_by='user',
            request_quote='Please use an applied front.',request_reference='client message 2026-09-15')
        f.write(tmp_path)
        assert DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_missing_cap_reference_fails_closed(self,tmp_path):
        f=LayoutFixture();f.stack['cap']=f.root+'/part:missing';f.write(tmp_path)
        assert not DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_independent_dimensions_are_not_wardrobe_constants(self,tmp_path):
        f=LayoutFixture()
        for v in f.visits:
            if not hasattr(v,'part'):continue
            v.part.solid=cq.Workplane(obj=v.part.solid.val().scale(.8))
        f.stack['operating_gaps_mm']=[2.4,2.4]
        f.stack['drawers'][0]['side_reveals_mm']=[1.6,1.6];f.write(tmp_path)
        for key in ('obstruction_deductions_mm','fit_clearances_mm','support_offsets_mm','runner_installation_widths_mm'):
            f.clearance[key]=[v*.8 for v in f.clearance[key]]
        f.write(tmp_path)
        assert DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_asymmetric_hinge_deduction_produces_centered_symmetric_front(self,tmp_path):
        f=LayoutFixture()
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:front':
                v.part.solid=cq.Workplane('XY').box(542,16,144.5,centered=False).translate((28,2,19))
        f.clearance['obstruction_deductions_mm']=[10,0];f.write(tmp_path)
        assert DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_offcenter_front_fails_even_when_both_sides_clear_hardware(self,tmp_path):
        f=LayoutFixture()
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:front':
                v.part.solid=cq.Workplane('XY').box(552,16,144.5,centered=False).translate((28,2,19))
        f.clearance['obstruction_deductions_mm']=[10,0];f.write(tmp_path)
        assert any('symmetric' in p for p in DrawerLayoutPolicyChecker().check(tmp_path,f.visits).problems)

    def test_hidden_supports_may_differ_while_front_stays_centered(self,tmp_path):
        f=LayoutFixture();f.clearance['support_offsets_mm']=[25,0]
        for v in f.visits:
            if hasattr(v,'part') and v.path[-1]=='part:right_wall':
                v.part.solid=v.part.solid.translate((25,0,0))
        f.write(tmp_path)
        assert DrawerLayoutPolicyChecker().check(tmp_path,f.visits).passed

    def test_missing_or_stale_travel_evidence_fails(self,tmp_path):
        f=LayoutFixture();f.write(tmp_path)
        (tmp_path/'aikea.yaml').write_text('changed_hinge_layout: true')
        assert any('stale' in p for p in DrawerLayoutPolicyChecker().check(tmp_path,f.visits).problems)
        (tmp_path/'assemblies/drawer-travel-clearance.json').unlink()
        assert any('missing verified' in p for p in DrawerLayoutPolicyChecker().check(tmp_path,f.visits).problems)

    def test_unnecessary_symmetric_supports_fail_current_clearance(self,tmp_path):
        f=LayoutFixture();f.clearance['support_offsets_mm']=[25,0];f.write(tmp_path)
        assert any('box width' in p for p in DrawerLayoutPolicyChecker().check(tmp_path,f.visits).problems)
