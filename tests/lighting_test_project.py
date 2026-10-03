"""Scope: Save a rotated custom host and an independent earlier machining feature."""

from pathlib import Path

from cabinet_feature_manifest import CabinetFeatureManifest
from complete_assembly_builder_renderer import CompleteAssemblyBuilderRenderer
from furniture_design_project import FurnitureDesignProject


class LightingTestProject:
    def create(self, root):
        FurnitureDesignProject().initialize(root)
        owner = root/'assemblies/custom_01'
        (owner/'service').mkdir(parents=True)
        files = {
            '__init__.py': '"""Scope: Own a custom upright panel."""\n',
            'spec.py': '''"""Scope: Declare the arbitrary host using common construction values."""
from assemblies.specification import PartSpec, LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
from assemblies.panel_assembly import PanelAssemblySpec
PART = PartSpec('host', 'display panel', (), LocalToParentPlacement(Point3D(100, 200, 50),
    AxisBasis(AxisDirection(0,1,0), AxisDirection(0,0,1), AxisDirection(1,0,0))),
    local_size_mm=(800, 400, 16), inside_face='>Z', material_id='mdf')
SPEC = PanelAssemblySpec('custom_01', 'display panel', (PART,), (), requirements=())
''',
            'builder.py': '"""Scope: Build explicit panels through common construction."""\nfrom assemblies.panel_assembly import PanelAssemblyBuilder\nfrom .spec import SPEC\nBUILDER = PanelAssemblyBuilder(SPEC)\n',
            'complete_builder.py': CompleteAssemblyBuilderRenderer().render('custom_01'),
            'service/__init__.py': '"""Scope: Keep an independent service feature."""\n',
            'service/feature.py': '''"""Scope: Machine an unrelated service hole through the shared feature."""
from assemblies.specification import IDENTITY_LOCAL_TO_PARENT
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from panel_machining_feature import PanelMachiningFeature

class ServiceFeature:
    def apply(self, assembly):
        return PanelMachiningFeature().apply(assembly, (SurfaceDrillingSpec('service', 'host',
            IDENTITY_LOCAL_TO_PARENT, (SurfaceHole('fix', 20, 20, 3, 8),)),))

FEATURE = ServiceFeature()
''',
        }
        for name, text in files.items():
            (owner/name).write_text(text)
        CabinetFeatureManifest().register(root, 'custom_01', 'service.feature', 10,
                                          affected_manufactured_part_paths=('host',))
        return root
