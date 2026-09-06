"""Scope: Build Cabineo pocket and brass-insert receiver machining volumes."""

from functools import lru_cache

import cadquery as cq

from cabineo_profile import CabineoProfile


class CabineoCutterGeometry:
    """Construct the cutter directly in the source face-and-edge frame."""

    @staticmethod
    @lru_cache(maxsize=4)
    def build(profile: CabineoProfile) -> cq.Shape:
        radius = profile.pocket_radius_mm
        bores = tuple(
            cq.Solid.makeCylinder(
                radius,
                profile.pocket_depth_mm,
                cq.Vector(0, center, 0),
                cq.Vector(0, 0, 1),
            )
            for center in profile.pocket_centers_mm
        )
        source_region = cq.Solid.makeBox(
            2 * radius,
            profile.pocket_rear_center_mm + radius,
            profile.pocket_depth_mm,
            cq.Vector(-radius, 0, 0),
        )
        pocket = bores[0].fuse(*bores[1:]).intersect(source_region)
        receiver = cq.Solid.makeCylinder(
            profile.receiver_diameter_mm / 2,
            profile.receiver_depth_mm,
            cq.Vector(0, 0, profile.receiver_axis_height_mm),
            cq.Vector(0, -1, 0),
        )
        return pocket.fuse(receiver).clean()


__all__ = ["CabineoCutterGeometry"]
