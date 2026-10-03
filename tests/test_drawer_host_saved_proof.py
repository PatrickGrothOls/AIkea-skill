"""Scope: Run the saved custom drawer through generation, exact test CAD and both review states."""

from dataclasses import replace
from pathlib import Path
import os

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_plan import DrawerLayout
from hettich_ka_4532_spacer_cabinet_drawer_generator import HettichKa4532SpacerCabinetDrawerGenerator
from hettich_ka_4532_spacer_mounting_test_support import HettichKa4532StepSetLoaderProbe
from hettich_ka_4532_spacer_proof_generator import HettichKa4532SpacerProofGenerator
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSetLoader


class TestDrawerHostSavedProof:
    def test_saved_custom_input_drives_proof_and_changed_host_invalidates_it(self, tmp_path, monkeypatch):
        spec_path = self._project(tmp_path)
        loader = HettichKa4532StepSetLoaderProbe()
        monkeypatch.setattr(HettichKa4532SpacerStepSetLoader, "load", loader.load)
        HettichKa4532SpacerCabinetDrawerGenerator(loader).generate(
            tmp_path, "niche_01", DrawerLayout("drawer_01", 100, box_height_mm=150, box_depth_mm=500),
            hardware_directory=tmp_path/"hardware", cabinet_front_mm=50, drawer_front_mm=50)
        generator = HettichKa4532SpacerProofGenerator(step_loader=loader)
        result = generator.generate(tmp_path, "niche_01", tmp_path/"review")
        assert result.report.is_valid, result.report.failed_check_names()
        assert result.report.collisions["swept_envelope_pairs"] == []
        assert result.closed_glb_path.stat().st_size > 0 and result.open_glb_path.stat().st_size > 0
        assert result.report.as_dict()["manufacturing_authority"] is False
        before = spec_path.stat()
        source = spec_path.read_text()
        spec_path.write_text(source.replace('front_mm=50', 'front_mm=49'))
        # Python timestamp caches have only whole-second precision for source changes.
        os.utime(spec_path, ns=(before.st_atime_ns, before.st_mtime_ns))
        changed = generator.generate(tmp_path, "niche_01", tmp_path/"review")
        assert not changed.report.is_valid

    def _project(self, root):
        project = yaml.safe_load((Path(__file__).parent/'fixtures/four-unit-review-aikea.yaml').read_text())
        (root/'aikea.yaml').write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, root)
        original = CabinetAssemblySpecLoader().load(root, "tall_storage_01")
        parts = []
        for old, new in (("left_side", "support_a"), ("right_side", "support_b")):
            part = original.part(old)
            frame = part.local_to_parent
            point = frame.origin_in_parent
            shifted = replace(point, x_mm=point.x_mm+100, y_mm=point.y_mm+25, z_mm=point.z_mm+32)
            parts.append(replace(part, part_id=new, role="support", local_to_parent=replace(frame, origin_in_parent=shifted), material_id="mdf"))
        parent = root/'assemblies/niche_01'
        parent.mkdir()
        (parent/'__init__.py').write_text('"""Scope: Own the test custom bay."""\n')
        source = ('"""Scope: Declare custom panels and an inset drawer bay."""\n'
                  'from assemblies.specification import *\nfrom assemblies.panel_assembly import PanelAssemblySpec\n'
                  'from drawer_host import DrawerHostSpec\n'
                  f'SPEC = PanelAssemblySpec("niche_01", "custom", {tuple(parts)!r}, requirements=())\n'
                  'DRAWER_HOST = DrawerHostSpec("support_a", "support_b", front_mm=50, inside_depth_mm=539, bottom_mm=132, top_mm=932)\n')
        spec_path = parent/'spec.py'
        spec_path.write_text(source)
        (parent/'builder.py').write_text('"""Scope: Build the custom panels through shared construction."""\n'
            'from assemblies.panel_assembly import PanelAssemblyBuilder\nfrom .spec import SPEC\nBUILDER = PanelAssemblyBuilder(SPEC)\n')
        return spec_path
