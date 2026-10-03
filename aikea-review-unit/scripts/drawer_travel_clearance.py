"""Scope: Validate current sweep evidence before using hardware-derived drawer widths."""
import json
from math import isfinite
from construction_input_fingerprint import ConstructionInputFingerprinter


class DrawerTravelClearance:
    RECORD = 'assemblies/drawer-travel-clearance.json'

    def read(self, root, visits, drawers):
        path = root / self.RECORD
        if not path.is_file():
            return {}, ('missing verified drawer travel-clearance evidence',)
        # This file is an external evidence boundary, not a replacement sweep solver.
        try:
            record = json.loads(path.read_text())
            entries = record['drawers']
            valid = record['schema_version'] == 1 and isinstance(entries, list)
            identities = {'/'.join(v.path) for v in visits}
            for item in entries:
                valid &= item['status'] == 'PASS' and item['method'] == 'full_travel_sweep'
                valid &= self._positive(item['travel_mm'])
                valid &= bool(item['constraint_paths']) and set(item['constraint_paths']) <= identities
                for name in ('obstruction_deductions_mm', 'fit_clearances_mm',
                             'support_offsets_mm', 'runner_installation_widths_mm'):
                    values = item[name]
                    valid &= len(values) == 2 and all(self._nonnegative(v) for v in values)
            paths = [item['path'] for item in entries]
            valid &= set(paths) == drawers and len(paths) == len(set(paths))
            fingerprint = record['construction_sha256']
        except (OSError, KeyError, TypeError, ValueError):
            return {}, ('malformed drawer travel-clearance evidence',)
        if not valid:
            return {}, ('unverified drawer travel, constraint paths or independent side deductions',)
        if fingerprint != ConstructionInputFingerprinter().build(root, visits):
            return {}, ('stale drawer travel-clearance evidence; recheck current hinges, doors and drawers',)
        return {item['path']: item for item in entries}, ()

    def _nonnegative(self, value):
        return isinstance(value, (int, float)) and isfinite(value) and value >= 0

    def _positive(self, value):
        return self._nonnegative(value) and value > 0
