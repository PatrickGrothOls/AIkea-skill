"""Scope: Reject two-face and edge machining while permitting through holes."""

from types import SimpleNamespace as Value
from panel_setup_checker import PanelSetupChecker


class TestPanelSetupChecker:
    def assembly(self, requests):
        part = Value(part_id="panel", local_size_mm=(300, 200, 16), inside_face=">Z")
        return Value(spec=Value(parts=(part,), machining=requests), joints=())

    def request(self, name, inward_z, depth):
        axis = Value(x=0, y=0, z=inward_z)
        return Value(machining_id=name, part_id="panel", operation_type="surface_pocket",
                     surface_to_part=Value(axis_basis=Value(local_z_in_parent=axis)), depth_mm=depth)

    def test_blind_operations_on_opposite_faces_conflict(self):
        result = PanelSetupChecker().check(self.assembly((self.request("top", -1, 5), self.request("bottom", 1, 5))))
        assert result["status"] == "conflict_or_unsupported"

    def test_through_opening_can_share_the_other_blind_entry_face(self):
        result = PanelSetupChecker().check(self.assembly((self.request("top", -1, 5), self.request("through", 1, 16))))
        assert result["parts"][0]["allowed_faces"] == [">Z"]
        assert result["machining_ready"] is False

    def test_edge_or_tilted_operation_is_not_a_broad_face_setup(self):
        request = self.request("edge", 0, 16)
        request.surface_to_part.axis_basis.local_z_in_parent.x = 1
        assert PanelSetupChecker().check(self.assembly((request,)))["status"] == "conflict_or_unsupported"

    def test_unknown_operation_does_not_silently_pass(self):
        request = self.request("novel", 1, 5)
        request.operation_type = "novel"
        assert PanelSetupChecker().check(self.assembly((request,)))["status"] == "conflict_or_unsupported"

    def placement(self, origin, axes):
        return Value(origin_in_parent=Value(x_mm=origin[0], y_mm=origin[1], z_mm=origin[2]),
                     axis_basis=Value(**{name: Value(x=axis[0], y=axis[1], z=axis[2])
                                        for name, axis in zip(("local_x_in_parent", "local_y_in_parent", "local_z_in_parent"), axes)}))

    def test_receiver_face_is_transformed_from_the_actual_joint_edge(self):
        flat = self.placement((0, 0, 0), ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        upright = self.placement((300, 0, 0), ((0, 1, 0), (0, 0, 1), (1, 0, 0)))
        parts = (Value(part_id="shelf", local_to_parent=flat), Value(part_id="side", local_to_parent=upright))
        joint = Value(joint_type="cabineo", joint_id="seam", source_part_id="shelf", target_part_id="side", source_face=">Z", source_edge=">X")
        assembly = Value(spec=Value(parts=parts, machining=()), joints=(joint,))
        report = PanelSetupChecker().check(assembly)
        assert report["parts"][0]["allowed_faces"] == [">Z"]
        assert report["parts"][1]["allowed_faces"] == ["<Z"]

    def test_a_centre_panel_receiving_from_both_directions_requires_two_setups(self):
        flat = self.placement((0, 0, 0), ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        upright = self.placement((300, 0, 0), ((0, 1, 0), (0, 0, 1), (1, 0, 0)))
        parts = (Value(part_id="shelf", local_to_parent=flat), Value(part_id="divider", local_to_parent=upright))
        joints = tuple(Value(joint_type="cabineo", joint_id="seam" + edge, source_part_id="shelf", target_part_id="divider", source_face=">Z", source_edge=edge) for edge in ("<X", ">X"))
        report = PanelSetupChecker().check(Value(spec=Value(parts=parts, machining=()), joints=joints))
        assert report["parts"][1]["allowed_faces"] == []

    def test_korrekt_through_bores_share_a_blind_panel_setup(self):
        frame=self.placement((0,0,0),((1,0,0),(0,1,0),(0,0,1)))
        assembly=self.assembly((self.request('top',-1,5),))
        assembly.spec.parts[0].local_to_parent=frame
        plate=Value(hardware_id='plate',local_to_parent=frame)
        assembly.spec.purchased_hardware=(plate,)
        assembly.joints=(Value(joint_type='korrekt_mounting',joint_id='feet',part_id='panel',hardware_id='plate'),)
        assert PanelSetupChecker().check(assembly)['parts'][0]['allowed_faces']==['>Z']
        plate.local_to_parent=self.placement((0,0,0),((1,0,0),(0,0,1),(0,-1,0)))
        assert PanelSetupChecker().check(assembly)['status']=='conflict_or_unsupported'

    def test_miter_half_spaces_resolve_each_actual_access_face(self):
        side=Value(part_id='side',inside_face='>Z',local_size_mm=(200,200,16),
            local_to_parent=self.placement((0,0,0),((0,1,0),(0,0,1),(1,0,0))))
        top=Value(part_id='top',inside_face='<Z',local_size_mm=(200,200,16),
            local_to_parent=self.placement((0,0,184),((1,0,0),(0,1,0),(0,0,1))))
        joint=Value(joint_type='equal_thickness_miter',joint_id='corner',participant_ids=('side','top'))
        assembly=Value(spec=Value(parts=(side,top),machining=()),joints=(joint,))
        result=PanelSetupChecker().check(assembly)
        assert [p['allowed_faces'] for p in result['parts']]==[['>Z'],['<Z']]
        opposite=self.request('opposing_blind_cut',1,5);opposite.part_id='side'
        assembly.spec.machining=(opposite,)
        assert PanelSetupChecker().check(assembly)['parts'][0]['allowed_faces']==[]
