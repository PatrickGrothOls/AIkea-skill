"""Scope: Rebuild saved KA 5332 drawers as one compact floor-to-shelf stack."""

import argparse
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[2]
for sibling in ('aikea-build-units', 'aikea-review-unit'):
    sys.path.insert(0, str(PACKAGE / sibling / 'scripts'))

from cadquery_runtime import CadQueryRuntime
from drawer_host_loader import DrawerHostLoader
from hettich_ka_5332_compact_stack import HettichKa5332CompactStackPlanner
from hettich_ka_5332_cabinet_drawers_generator import HettichKa5332CabinetDrawersGenerator
from hettich_ka_5332_drawer_layout_collection_loader import HettichKa5332DrawerLayoutCollectionLoader


class CompactHettichDrawersCommand:
    """Keep identities and stock while fitting proposed height proportions to a cap."""

    def run(self, arguments):
        root = arguments.aikea_yaml.parent
        existing = HettichKa5332DrawerLayoutCollectionLoader().load(root, arguments.assembly)
        ordered = tuple(sorted(existing, key=lambda drawer: drawer.bottom_height_mm))
        host = DrawerHostLoader().load(root, arguments.assembly)
        layouts = HettichKa5332CompactStackPlanner().plan(
            host, ordered, cap_underside_mm=arguments.cap_underside_mm)
        result = HettichKa5332CabinetDrawersGenerator().generate(
            root, arguments.assembly, layouts, hardware_directory=arguments.hardware_directory)
        print(json.dumps({
            'status': 'generated',
            'scope': 'vertical placement; complete installation checks still required',
            'cap_underside_above_floor_mm': arguments.cap_underside_mm,
            'drawers': [{
                'id': drawer.layout.drawer_id,
                'bottom_above_floor_mm': drawer.hardware_mounting.resolved_drawer_bottom_height_mm,
                'height_mm': drawer.layout.box_height_mm,
            } for drawer in result.plan.drawers],
        }, indent=2))
        return 0

    @classmethod
    def main(cls):
        runtime = CadQueryRuntime.from_environment()
        if not runtime.current_is_ready():
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('aikea_yaml', type=Path)
        parser.add_argument('--assembly', required=True)
        parser.add_argument('--cap-underside-mm', required=True, type=float,
                            help='Actual cap underside above cabinet floor top, after shelf placement.')
        parser.add_argument('--hardware-directory', required=True, type=Path)
        return cls().run(parser.parse_args())


if __name__ == '__main__':
    raise SystemExit(CompactHettichDrawersCommand.main())
