"""Scope: Expose the first complete cabinet for bounded integration checks."""
import cadquery as cq
from assemblies.cabinet_builder import CabinetBuilder
BUILDER=CabinetBuilder(0)
ENVELOPE=cq.Workplane('XY').box(600,450,2274,centered=False).translate((-1,-18,0))
