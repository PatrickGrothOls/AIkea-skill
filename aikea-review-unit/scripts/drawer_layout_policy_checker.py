"""Scope: Gate installed drawer defaults using actual part references and user-only exceptions."""
import json
import re
from math import isfinite
from drawer_layout_geometry import DrawerLayoutGeometry
from drawer_travel_clearance import DrawerTravelClearance
from fabrication_readiness_report import FabricationReadinessCheck


class DrawerLayoutPolicyChecker:
    RECORD='assemblies/drawer-layout-policy.json'

    def check(self,root,visits):
        drawers={"/".join(v.path) for v in visits if hasattr(v,'assembly') and
                 (re.fullmatch(r'drawer_[0-9]+',v.assembly.spec.assembly_id) or
                  'drawer' in v.assembly.spec.purpose.lower())}
        if not drawers:return FabricationReadinessCheck('design.drawer_layout',True)
        path=root/self.RECORD
        if not path.is_file():return self._result(('missing drawer layout policy evidence for installed drawers',))
        # Parse only the external JSON boundary; geometry failures are not swallowed.
        try:
            record=json.loads(path.read_text())
        except (OSError,ValueError) as error:
            return self._result((f'invalid drawer layout evidence: {error}',))
        invalid=self._record_problems(record,visits)
        if invalid:return self._result(invalid)
        clearances,invalid=DrawerTravelClearance().read(root,visits,drawers)
        if invalid:return self._result(invalid)
        visible_reveals={}
        for stack in record['stacks']:
            group=stack.get('front_alignment_group',stack['cabinet'])
            required=max(a+b for drawer in stack['drawers']
                         for a,b in zip(clearances[drawer['path']]['obstruction_deductions_mm'],
                                        clearances[drawer['path']]['fit_clearances_mm']))
            visible_reveals[group]=max(visible_reveals.get(group,0),required)
        geometry=DrawerLayoutGeometry(visits);problems=[];covered=[]
        for stack in record['stacks']:
            covered.extend(d['path'] for d in stack['drawers'])
            group=stack.get('front_alignment_group',stack['cabinet'])
            failures=geometry.check(stack,clearances,visible_reveals[group])
            exceptions=stack.get('user_requested_exceptions',[])
            allowed={e['rule'] for e in exceptions if e.get('requested_by')=='user' and
                     e.get('request_quote','').strip() and e.get('request_reference','').strip()}
            problems.extend(f'{stack["cabinet"]}: {failure}' for failure in failures
                            if failure.split(':')[0] not in allowed)
            if len(allowed)!=len(exceptions):problems.append('exception lacks an explicit user request quote/reference')
        if set(covered)!=drawers or len(covered)!=len(set(covered)):
            problems.append('every installed drawer must appear exactly once in the layout evidence')
        return self._result(tuple(problems))

    def _record_problems(self,record,visits):
        identities={"/".join(v.path) for v in visits}
        # The required field structure is checked before any CAD access.
        try:
            valid=record['schema_version']==1 and isinstance(record['stacks'],list)
            for stack in record['stacks']:
                references=[stack['cabinet'],stack['floor'],stack['cap'],*stack['opening_sides']]
                valid &= 0<float(stack.get('tolerance_mm',.25))<=.5
                valid &= len(stack['opening_sides'])==2 and bool(stack['drawers'])
                valid &= isinstance(stack.get('front_alignment_group',stack['cabinet']),str)
                valid &= all(isinstance(g,(int,float)) and isfinite(g) for g in stack['operating_gaps_mm'])
                for drawer in stack['drawers']:
                    references.extend((drawer['path'],drawer['front'],*drawer['sides']))
                    valid &= len(drawer['sides'])==2
                    valid &= all(p.startswith(drawer['path']+'/part:') for p in (drawer['front'],*drawer['sides']))
                valid &= set(references)<=identities
                valid &= all(e['rule'] in {'compact_stack','single_front','frontage'} and
                             all(isinstance(e.get(k,''),str) for k in ('requested_by','request_quote','request_reference'))
                             for e in stack.get('user_requested_exceptions',[]))
        except (KeyError,TypeError,ValueError):
            return ('malformed drawer layout policy record',)
        return () if valid else ('invalid drawer references, dimensions or policy tolerances',)

    def require(self,root,visits):
        check=self.check(root,visits)
        if not check.passed:raise ValueError('; '.join(check.problems))

    def _result(self,problems):
        return FabricationReadinessCheck('design.drawer_layout',not problems,problems)
