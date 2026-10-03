"""Scope: Verify alternate Riex geometry keeps physical ownership and exact CAD provenance."""

from types import SimpleNamespace

from riex_review_identity import RiexReviewIdentity
from unit_mockup import MockupPart


class TestRiexReviewIdentity:
    def test_open_pose_keeps_panel_hinge_and_plate_paths(self):
        hardware = tuple(SimpleNamespace(spec=SimpleNamespace(hardware_id=name,
            mounting_part_id=owner, product_code=code, hardware_asset_id=asset,
            geometry_selector=None)) for name, owner, code, asset in (
                ('hinge_01_hinge', 'door', 'F000001', 'riex-nc70-f000001-closed'),
                ('hinge_01_plate', 'side', 'F000049', 'riex-nc70-f000049-h0-euroscrew-plate')))
        assembly = SimpleNamespace(purchased_hardware=hardware)
        plan = SimpleNamespace(door_part_id='door', placements=(SimpleNamespace(hinge_id='hinge_01'),))
        parts = tuple(MockupPart(name, object(), object(), (.5, .5, .5, 1)) for name in
                      ('door', 'side', 'hinge_01__source_cad', 'hinge_01_plate__source_cad'))
        opened = RiexReviewIdentity().apply(parts, assembly, plan)
        assert [part.inspection_path for part in opened] == [
            ('door',), ('door', 'hinge_01_hinge'), ('side', 'hinge_01_plate')]
        assert [part.review_kind for part in opened] == ['panel', 'hardware', 'hardware']
        assert opened[1].source_hardware_asset_id == 'riex-nc70-f000001-open'
        assert opened[2].source_hardware_asset_id == hardware[1].spec.hardware_asset_id
        for original, posed in zip((parts[0], parts[2], parts[3]), opened):
            assert posed.solid is original.solid
            assert posed.location is original.location
