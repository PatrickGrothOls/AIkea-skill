"""Scope: Verify compact planning survives real drawer generation and host drilling."""

from dataclasses import replace
from pathlib import Path

import cadquery as cq
import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from compact_drawer_stack_planner import CompactDrawerStackPlanner
from drawer_host_loader import DrawerHostLoader
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_5332_cabinet_drawers_generator import HettichKa5332CabinetDrawersGenerator
from hettich_ka_5332_compact_stack import HettichKa5332CompactStackPlanner
from hettich_ka_5332_drawer_layout_collection_loader import HettichKa5332DrawerLayoutCollectionLoader
from hettich_ka_5332_test_support import HettichKa5332StepAssemblyLoaderTestDouble, TEST_HETTICH_HARDWARE_DIRECTORY
from panel_hardware_reservation import PanelHardwareConflictError


class TestCompactDrawerStack:
    def layouts(self):
        return tuple(DrawerLayout(f'drawer_{index:02}', bottom, box_height_mm=height, box_depth_mm=500)
                     for index, (bottom, height) in enumerate(((100, 140), (270, 200), (490, 150)), 1))

    def test_fills_existing_cap_with_varied_heights_and_three_mm_gaps(self):
        layouts = CompactDrawerStackPlanner().plan(self.layouts(), cap_underside_mm=596)
        assert layouts[0].bottom_height_mm == 3
        for lower, upper in zip(layouts, layouts[1:]):
            assert upper.bottom_height_mm - lower.bottom_height_mm - lower.box_height_mm == pytest.approx(3)
        assert 596 - layouts[-1].bottom_height_mm - layouts[-1].box_height_mm == pytest.approx(3)
        assert layouts[1].box_height_mm / layouts[0].box_height_mm == pytest.approx(200 / 140)
        assert all(not drawer.snap_to_system_32 for drawer in layouts)

    @pytest.mark.parametrize('cap,gap', [(10, 3), (float('nan'), 3), (600, 0), (600, 6)])
    def test_rejects_invalid_envelope_or_operating_gap(self, cap, gap):
        with pytest.raises(ValueError):
            CompactDrawerStackPlanner().plan(self.layouts(), cap_underside_mm=cap, gap_mm=gap)

    def test_generated_parts_and_fixings_preserve_compact_stack(self, tmp_path):
        project = yaml.safe_load((Path(__file__).parent / 'fixtures/four-unit-review-aikea.yaml').read_text())
        (tmp_path / 'aikea.yaml').write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        host = DrawerHostLoader().load(tmp_path, 'tall_storage_01')
        layouts = HettichKa5332CompactStackPlanner().plan(host, self.layouts(), cap_underside_mm=596)
        generator = HettichKa5332CabinetDrawersGenerator(HettichKa5332StepAssemblyLoaderTestDouble())
        result = generator.generate(tmp_path, 'tall_storage_01', layouts,
                                    hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY)
        reloaded = HettichKa5332DrawerLayoutCollectionLoader().load(tmp_path, 'tall_storage_01')
        assert reloaded == layouts
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, 'tall_storage_01')
        visits = loader.walk(tmp_path, built)
        from drawer_layout_geometry import DrawerLayoutGeometry
        geometry = DrawerLayoutGeometry(visits)
        fronts = [geometry.box(f'tall_storage_01/{layout.drawer_id}/part:front') for layout in layouts]
        assert fronts[0].zmin - host.spec.bottom_mm == pytest.approx(3)
        assert [b.zmin-a.zmax for a, b in zip(fronts, fronts[1:])] == pytest.approx([3, 3])
        assert host.spec.bottom_mm + 596 - fronts[-1].zmax == pytest.approx(3)
        for drawer in result.plan.drawers:
            assert drawer.hardware_mounting.resolved_drawer_bottom_height_mm == pytest.approx(drawer.layout.bottom_height_mm)
            assert all(bool(r.system_32_node_rows_mm) == (drawer.layout.drawer_id != 'drawer_01')
                       for r in drawer.hardware_reservations)
            # Test all real fixing axes in the rebuilt side, not only saved records.
            for side in ('left', 'right'):
                part = next(p for p in built.parts if p.spec.part_id == host.part(side).part_id)
                for x in drawer.runner.cabinet_fixing_positions_from_front_mm:
                    point = host.frame(side).to_local((host.inside_x(side), host.spec.front_mm+x,
                            drawer.origin_in_parent_mm[2]+drawer.runner.runner_center_from_drawer_bottom_mm))
                    probe = cq.Vector(point[0], point[1], part.spec.local_size_mm[2]-1)
                    assert not part.solid.val().isInside(probe)
        # Exact placement must reject a conflict, never silently shift upward.
        blocking = replace(result.plan.drawers[0].hardware_reservations[0], owner_id='hinge_obstruction', hardware_kind='hinge')
        with pytest.raises(PanelHardwareConflictError):
            generator.planner.plan(host, layouts, result.plan.drawers[0].hardware_step, (blocking,))

    def test_reserves_rows_for_remaining_drawers(self):
        layouts = tuple(replace(item, box_height_mm=weight)
                        for item, weight in zip(self.layouts(), (1000, 1, 1)))
        planned = CompactDrawerStackPlanner().plan(layouts, cap_underside_mm=400,
                                                   available_bottoms_mm=(100, 200, 300))
        assert [item.bottom_height_mm for item in planned] == [3, 200, 300]

    def test_old_saved_layout_retains_grid_snapping(self, tmp_path):
        folder = tmp_path / 'assemblies/cabinet_01'
        folder.mkdir(parents=True)
        record = {'id': 'drawer_01', 'bottom_height_mm': 100, 'box': {
            'height_mm': 140, 'side_thickness_mm': 15, 'front_back_thickness_mm': 15,
            'bottom_thickness_mm': 9, 'bottom_underside_recess_mm': 13, 'side_length_mm': 500}}
        (folder / 'drawer-layout.yaml').write_text(yaml.safe_dump({'drawers': [record]}))
        loaded = HettichKa5332DrawerLayoutCollectionLoader().load(tmp_path, 'cabinet_01')
        assert loaded[0].snap_to_system_32
        assert loaded[0].bottom_height_mm == 100
