"""Scope: Compose the measured four-bay wardrobe from independently complete children."""
import cadquery as cq
from assemblies.design_primitives import P
from assemblies.vilja_inputs import INPUTS as I
from assemblies.cabinet_builder import CabinetBuilder
from assemblies.base_builder import BaseBuilder
from assemblies.specification import BuiltChildAssembly, ChildAssemblySpec
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder


class WardrobeBuilder:
    def build(self):
        children=[]
        base=BaseBuilder().build()
        children.append(BuiltChildAssembly(ChildAssemblySpec(base.spec.assembly_id,base.spec.purpose,P.frame()),base))
        for index in range(4):
            built=CabinetBuilder(index).build()
            child=ChildAssemblySpec(built.spec.assembly_id,built.spec.purpose,P.frame((I.cabinet_x(index),0,95)))
            children.append(BuiltChildAssembly(child,built))
        spec=PanelAssemblySpec('furniture_01','Vilja wardrobe — provisional GRASS closed fit',(),child_assemblies=tuple(c.spec for c in children))
        return PanelAssemblyBuilder(spec,children=tuple(children)).build()


BUILDER=WardrobeBuilder()
ENVELOPE=cq.Workplane('XZ').polyline(((0,0),(2475,0),(2475,724),(990,2374),(0,2374))).close().extrude(450).translate((0,432,0))
