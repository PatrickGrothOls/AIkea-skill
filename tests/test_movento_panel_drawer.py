"""Scope: Prove the drawer candidate applies all mounting cuts on its chosen faces."""
from dataclasses import replace
from math import pi, sqrt
from functools import partial

import pytest
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from construction_requirement_checker import ConstructionRequirementChecker
from construction_result_validator import ConstructionResultValidator
from panel_setup_checker import PanelSetupChecker
from movento_panel_dimensions import MoventoPanelDimensions
from movento_panel_drawer import MoventoPanelDrawer
from movento_panel_machining import MoventoPanelMachining, MoventoPilotChoice
from movento_drawer_installation import MoventoDrawerInstallation, MoventoInstallationRequest


class TestMoventoPanelDrawer:
    @pytest.fixture(scope="class")
    def drawer(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("movento")
        FurnitureDesignProject().initialize(root)
        return root, GeneratedProjectModuleRuntime().execute(root, self.build)

    def build(self):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        recipe=MoventoPanelDrawer()
        dimensions=MoventoPanelDimensions(709,125,724,165,-1,-32,20,"ply16","rail29","front20")
        pilots=MoventoPilotChoice(5,14,2.5,10,"Test preparation; not production qualification")
        spec=recipe.specification("drawer_01",dimensions,pilots)
        return PanelAssemblyBuilder(spec).build()

    def test_real_panel_cuts_and_all_six_chosen_faces(self, drawer):
        _, built=drawer
        assert len(built.parts)==6
        assert ConstructionResultValidator().validate(built)==()
        report=PanelSetupChecker().check(built)
        expected={p.spec.part_id:p.spec.inside_face for p in built.parts}
        for part in report["parts"]:
            assert expected[part["part_id"]] in part["allowed_faces"]
        by_id={op.machining_id:op for op in built.spec.machining}
        assert len(by_id["locking_clips"].holes)==4
        assert len(by_id["rear_hooks"].holes)==2
        assert len(built.cuts)==31  # 12 paired connectors, four grooves and three fixing patterns.

    def test_omitting_locking_preparation_fails_independent_requirement(self, drawer):
        root, built=drawer
        changed=replace(built,spec=replace(built.spec,machining=tuple(
            op for op in built.spec.machining if op.machining_id!="locking_clips")))
        visits=GeneratedAssemblyBuilderLoader().walk(root,changed)
        problems=ConstructionRequirementChecker().check(visits)[0].problems
        assert any("drawer_fixings" in p and "required operation is missing" in p for p in problems)

    def test_complete_500mm_host_pattern_keeps_all_five_fixings(self, drawer):
        root,_=drawer
        request=GeneratedProjectModuleRuntime().execute(root,self.host_pattern)
        assert [(h.x_mm,h.y_mm) for h in request.holes]==[
            (19,-9.575),(37,-9.575),(69,-9.575),(261,-9.575),(293,-9.575)]

    def host_pattern(self):
        from assemblies.specification import PartSpec
        frame=MoventoPanelDrawer.frame
        part=PartSpec("support","support",(),frame((-16,0,0),((0,1,0),(0,0,1),(1,0,0))),
                      local_size_mm=(518,180,16),inside_face=">Z",material_id="ply16")
        return MoventoPanelMachining().host("runner",part,frame((0,0,0)),0,
                                            MoventoPilotChoice(5,14,2.5,10,"test"),frame)

    def test_rejects_tilted_host_even_when_fixing_centers_lie_on_its_face(self, drawer):
        root,_=drawer
        with pytest.raises(ValueError, match="perpendicular"):
            GeneratedProjectModuleRuntime().execute(root,self.tilted_host_pattern)

    def tilted_host_pattern(self):
        from assemblies.specification import PartSpec
        frame=MoventoPanelDrawer.frame
        # Rotate the host about the fixing row: every center still lies on its
        # upper face, but the runner screws would enter that face at 30 degrees.
        c=sqrt(3)/2
        part=PartSpec("support","support",(),frame((-16*c,0,9.575+8),
                      ((0,1,0),(.5,0,c),(c,0,-.5))),local_size_mm=(518,180,16),
                      inside_face=">Z",material_id="ply16")
        return MoventoPanelMachining().host("runner",part,frame((0,0,0)),0,
                                            MoventoPilotChoice(5,14,2.5,10,"test"),frame)

    @pytest.mark.parametrize("as_iterator", [False, True])
    def test_installation_keeps_two_hosts_two_runners_and_two_clips(self, drawer, as_iterator):
        root,_=drawer
        result=GeneratedProjectModuleRuntime().execute(root,partial(self.install,as_iterator))
        assert len(result.parts)==2 and len(result.child_assemblies)==1
        assert len(result.purchased_hardware)==2
        assert len(result.child_assemblies[0].assembly.purchased_hardware)==2
        assert {h.spec.purchase.purchase_id for h in result.purchased_hardware}=={"drawer_02_runners"}
        assert {h.spec.hardware_id:h.spec.mounting_part_id for h in result.purchased_hardware}=={
            "drawer_02_runner_left":"host_left","drawer_02_runner_right":"host_right"}
        assert {h.spec.mounting_part_id for h in result.child_assemblies[0].assembly.purchased_hardware}=={"rail"}
        for part in result.parts:
            assert 518*220*16-part.solid.val().Volume()==pytest.approx(5*pi*2.5**2*14,abs=1e-4)
        assert ConstructionResultValidator().validate(result)==()

    def install(self, as_iterator):
        from assemblies.specification import PartSpec
        from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder
        frame=MoventoPanelDrawer.frame
        parts=(PartSpec("host_left","support",(),frame((-16,0,-40),((0,1,0),(0,0,1),(1,0,0))),
                       local_size_mm=(518,220,16),inside_face=">Z",material_id="ply16"),
               PartSpec("host_right","support",(),frame((725,518,-40),((0,-1,0),(0,0,1),(-1,0,0))),
                       local_size_mm=(518,220,16),inside_face=">Z",material_id="ply16"))
        parent=PanelAssemblyBuilder(PanelAssemblySpec("host_01","drawer host",parts,requirements=())).build()
        request=MoventoInstallationRequest("drawer_02",
            MoventoPanelDimensions(709,125,724,165,-1,-32,20,"ply16","rail29","front20"),
            MoventoPilotChoice(5,14,2.5,10,"test"),frame((0,0,0)),"host_left","host_right")
        installer=MoventoDrawerInstallation()
        if as_iterator:
            return installer.apply_many(parent,iter((request,)))
        return installer.apply(parent,request.drawer_id,request.dimensions,request.pilots,request.placement,
                               request.left_part_id,request.right_part_id)
