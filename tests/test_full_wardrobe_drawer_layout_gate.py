"""Scope: Prevent the legacy wardrobe export from bypassing drawer layout evidence."""

from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from full_wardrobe_review_generator import FullWardrobeReviewGenerator
from hettich_ka_5332_cabinet_drawers_generator import HettichKa5332CabinetDrawersGenerator
from hettich_ka_5332_test_support import HettichKa5332StepAssemblyLoaderTestDouble, TEST_HETTICH_HARDWARE_DIRECTORY
from panel_review_hydration_fixture import PanelReviewHydrationFixture
from unit_mockup import UnitMockupInputError


class TestFullWardrobeDrawerLayoutGate:
    def test_installed_drawer_without_layout_evidence_cannot_export(self, tmp_path):
        project = yaml.safe_load((Path(__file__).parent / 'fixtures/four-unit-review-aikea.yaml').read_text())
        (tmp_path / 'aikea.yaml').write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        HettichKa5332CabinetDrawersGenerator(HettichKa5332StepAssemblyLoaderTestDouble()).generate(
            tmp_path, 'tall_storage_01', (DrawerLayout('drawer_01', 100),),
            hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY)
        generator = FullWardrobeReviewGenerator()
        generator._hydrate = PanelReviewHydrationFixture().hydrate
        with pytest.raises(UnitMockupInputError, match='missing drawer layout policy'):
            generator.generate(tmp_path, project)
        assert not (tmp_path / 'assemblies/full_wardrobe_review.glb').exists()
