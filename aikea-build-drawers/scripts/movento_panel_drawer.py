"""Scope: Compose one four-sided MOVENTO drawer through shared panel and joint tools."""
from movento_panel_machining import MoventoPanelMachining
from movento_captured_bottom import MoventoCapturedBottom


class MoventoPanelDrawer:
    """A construction candidate with all cuts; fit/material approval remains explicit.

    The visible front is also the structural front. A horizontal front support
    carries the vertical locking screws, avoiding edge drilling of that front.
    The bottom is captured by all four walls. Wall cuts use inner faces;
    support cuts use its underside. Rear hook bores pass through from inside.
    """

    def specification(self, assembly_id, dimensions, pilots):
        from assemblies.panel_assembly import PanelAssemblySpec
        from assemblies.specification import ConstructionRequirementSpec as Requirement
        parts = self.parts(dimensions)
        joints = self.joints(dimensions)
        grooves = MoventoCapturedBottom().grooves(dimensions, self.frame)
        machining = grooves + MoventoPanelMachining().drawer(dimensions, pilots, self.frame)
        required = (
            Requirement("panel_connections", "Join the walls/support and cut four retaining grooves", tuple(
                "part:"+part.part_id for part in parts if part.part_id!="bottom"),
                tuple("joint:"+joint.joint_id for joint in joints) +
                tuple("machining:"+groove.machining_id for groove in grooves),
                "operations", "Paired wall/support Cabineos and a four-edge captured floor"),
            Requirement("captured_floor_fit", "Qualify four-edge floor retention, stock fit and load",
                        ("part:bottom",)),
            Requirement("drawer_fixings", "Prepare locking devices and rear hooks", ("part:rail", "part:back"),
                ("machining:locking_clips", "machining:rear_hooks", "machining:runner_relief"),
                "operations", "Blum TD-132/1 plus unchanged clip CAD; " + pilots.basis),
            Requirement("installation_fit", "Qualify exact installed runner/clip CAD, motion and fastener/material fit",
                        tuple("part:"+part.part_id for part in parts)),
            Requirement("support_stock", "Prepare 14.5 mm finished support stock in the underside setup",
                        ("part:rail",)),
        )
        return PanelAssemblySpec(assembly_id, "MOVENTO four-sided drawer", parts, joints,
                                 machining=machining, requirements=required)

    def parts(self, d):
        w, h, inside = d.clear_width_mm, d.box_height_mm, d.inside_width_mm
        bottom = MoventoCapturedBottom()
        floor_size, floor_origin = bottom.floor(d)
        rows = (
            ("left", "drawer_side", (490,h,16), (5,0,0), ((0,1,0),(0,0,1),(1,0,0)), ">Z", d.panel_material),
            ("right", "drawer_side", (490,h,16), (w-5,490,0), ((0,-1,0),(0,0,1),(-1,0,0)), ">Z", d.panel_material),
            ("back", "drawer_back", (inside,h-.5,16), (21,490,.5), ((1,0,0),(0,0,1),(0,-1,0)), ">Z", d.panel_material),
            ("bottom", "drawer_bottom", floor_size, floor_origin, self.IDENTITY, "<Z", d.bottom_material),
            ("rail", "locking_device_support", (inside,64,bottom.underside_mm), (21,0,0), self.IDENTITY, "<Z", d.rail_material),
            ("front", "drawer_front", (d.front_width_mm,d.front_height_mm,d.front_thickness_mm),
             (d.front_left_mm,0,d.front_bottom_mm), ((1,0,0),(0,0,1),(0,-1,0)), "<Z", d.front_material),
        )
        from assemblies.specification import PartSpec
        return tuple(PartSpec(identifier, role, (), self.frame(origin, axes), local_size_mm=size,
                             inside_face=face, material_id=material)
                     for identifier, role, size, origin, axes, face, material in rows)

    def joints(self, dimensions):
        from assemblies.specification import CabineoJointSpec
        rows = (("left","front",">Z","<X"), ("right","front",">Z",">X"),
                ("back","left",">Z","<X"), ("back","right",">Z",">X"))
        positions = MoventoCapturedBottom().wall_positions(dimensions.box_height_mm)
        joints = tuple(CabineoJointSpec(f"{a}_to_{b}", a,b,face,edge,"explicit",
                       connector_positions_mm=tuple(p-(.5 if a=="back" else 0) for p in positions))
                       for a,b,face,edge in rows)
        return joints + tuple(CabineoJointSpec("rail_to_"+side,"rail",side,"<Z",edge,"explicit",
                                              connector_positions_mm=(16,52))
                              for side,edge in (("left","<X"),("right",">X")))

    IDENTITY = ((1,0,0),(0,1,0),(0,0,1))

    @staticmethod
    def frame(origin, axes=IDENTITY):
        from assemblies.specification import LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
        return LocalToParentPlacement(Point3D(*origin), AxisBasis(*(AxisDirection(*a) for a in axes)))


__all__ = ["MoventoPanelDrawer"]
