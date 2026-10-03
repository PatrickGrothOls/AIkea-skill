"""Scope: Prove Korrekt configured and authored bases share operations, ownership and missing-work checks."""
from dataclasses import replace
import importlib
from pathlib import Path
import pytest
import yaml
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from construction_requirement_checker import ConstructionRequirementChecker
from construction_tree_checker import ConstructionTreeChecker
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from physical_item_counter import PhysicalItemCounter
from korrekt_base_feature import KorrektBaseFeature
from korrekt_base_layout import KorrektBaseLayout


class TestConfiguredBaseConstruction:
    @pytest.fixture(scope="class")
    def base(self,tmp_path_factory):
        root = tmp_path_factory.mktemp("configured-base")
        project = yaml.safe_load((Path(__file__).parent/"fixtures/review-unit-aikea.yaml").read_text())
        AssemblyTaxonomyGenerator().generate(project,root)
        return (*GeneratedProjectModuleRuntime().execute(root,self._build),root)

    def _build(self):
        values = importlib.import_module("assemblies.specification")
        panels = importlib.import_module("assemblies.panel_assembly")
        tree = importlib.import_module("assemblies.assembly_tree").AssemblyTreeWalker()
        configured = importlib.import_module("assemblies.base_01.builder").BUILDER.build()
        spec = importlib.import_module("assemblies.base_01.spec").SPEC
        feature = KorrektBaseFeature(KorrektBaseLayout(spec.height_mm,spec.part("deck_01").local_size_mm[2])).feature(spec)
        direct = panels.PanelAssemblySpec(spec.assembly_id,spec.purpose,spec.parts,spec.joints,
            machining=spec.machining,requirements=spec.requirements)
        custom = feature.apply(panels.PanelAssemblyBuilder(direct,allow_unresolved=True).build())
        view = importlib.import_module("assemblies.base_01.parts.deck_01.builder").BUILDER.build()
        return values,panels,tree,configured,custom,view,direct,feature

    def test_preserves_geometry_cuts_and_individual_part_access(self,base):
        _,_,_,configured,custom,view,_,_,_ = base
        assert configured.spec.width_mm == pytest.approx(2978)
        assert len(configured.parts) == len(custom.parts) == 4
        assert configured.joints == custom.joints
        assert len(configured.cuts) == len(custom.cuts) == 16
        assert len(configured.purchased_hardware) == 32
        for actual,expected in zip(configured.parts,custom.parts):
            self._same_solid(actual.solid,expected.solid)
        self._same_solid(view.solid,configured.parts[0].solid)

    def test_counts_and_unresolved_work_are_identical(self,base):
        _,_,tree,configured,custom,_,_,_,_ = base
        left,right = (PhysicalItemCounter().count(tree.walk(b)) for b in (configured,custom))
        assert left == right
        assert {row["product_code"]:row["quantity"] for row in left["purchased_summary"]} == {"61854":16,"70151":16}
        assert any(item["code"] == "joint.unresolved" for item in left["unresolved"])
        assert ConstructionRequirementChecker().check(tree.walk(configured)) == ConstructionRequirementChecker().check(tree.walk(custom))

    def test_removal_retains_an_unfulfilled_independent_requirement(self,base):
        _,_,tree,_,custom,_,_,_,_ = base
        joint = next(j for j in custom.joints if j.joint_type == "korrekt_mounting")
        joints = tuple(j for j in custom.joints if j != joint)
        changed = replace(custom,spec=replace(custom.spec,joints=joints),joints=joints,
            cuts=tuple(c for c in custom.cuts if c.joint_id != joint.joint_id))
        problems = ConstructionRequirementChecker().check(tree.walk(changed))[0].problems
        assert any("required operation is missing" in item for item in problems)

    def test_custom_parent_and_renamed_deck_preserve_explicit_component(self,base):
        v,panels,tree,_,custom,_,direct,feature,root = base
        spec = replace(direct,parts=tuple(replace(p,role="custom_platform_top") if p.part_id.startswith("deck") else p for p in direct.parts))
        adapted = GeneratedProjectModuleRuntime().execute(root,
            lambda: feature.apply(panels.PanelAssemblyBuilder(spec,allow_unresolved=True).build()))
        placement = v.LocalToParentPlacement(v.Point3D(100,300,200),v.IDENTITY_AXIS_BASIS)
        child = v.ChildAssemblySpec(spec.assembly_id,spec.purpose,placement)
        owner = v.CompositeAssemblySpec("custom_01","layout",(child,),requirements=())
        nested = v.BuiltAssembly(owner,(),(),child_assemblies=(v.BuiltChildAssembly(child,adapted),))
        visits = tree.walk(nested)
        assert visits[1].local_to_root == placement
        self._same_solid(adapted.parts[0].solid,custom.parts[0].solid)
        assert all(check.passed for check in ConstructionTreeChecker().check(visits) if check.code == "construction.applied_operations")

    def _same_solid(self,actual,expected):
        assert actual.val().cut(expected.val()).Volume() == pytest.approx(0,abs=1e-5)
        assert expected.val().cut(actual.val()).Volume() == pytest.approx(0,abs=1e-5)
