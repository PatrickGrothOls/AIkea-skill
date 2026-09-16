"""Scope: Own explicit face-local lighting route and provisional installation dimensions."""

from dataclasses import dataclass
from math import hypot, isfinite
from typing import Literal

from recessed_luminaire_profile import RecessedLuminaireProfile


@dataclass(frozen=True)
class ConnectorPocket:
    """Installed pocket envelope including clearance; not bare connector dimensions."""

    length_mm: float
    width_mm: float
    depth_mm: float
    corner_radius_mm: float
    light_setback_mm: float


@dataclass(frozen=True)
class LightingRouteSpec:
    assembly_id: str
    part_id: str
    run_id: str
    face: Literal["<Z", ">Z"]
    front_edge_mm: tuple[tuple[float, float], tuple[float, float]]
    inset_mm: float
    start_margin_mm: float
    end_margin_mm: float
    profile: RecessedLuminaireProfile
    color_temperature_k: int
    cable_width_mm: float
    cable_depth_mm: float
    cutter_radius_mm: float
    minimum_stock_mm: float
    connector_end: Literal["none", "start", "end"] = "none"
    connector_pocket: ConnectorPocket | None = None

    def __post_init__(self):
        if self.face not in ("<Z", ">Z"):
            raise ValueError("lighting routing requires a broad machining face")
        if self.connector_end not in ("none", "start", "end"):
            raise ValueError("connector end must be none, start or end")
        if (self.connector_end == "none") != (self.connector_pocket is None):
            raise ValueError("connector pocket and connector end must be supplied together")
        values = (self.inset_mm, self.cable_width_mm, self.cable_depth_mm,
                  self.cutter_radius_mm, self.minimum_stock_mm,
                  self.profile.groove_width_mm, self.profile.groove_depth_mm)
        if any(not isfinite(v) or v <= 0 for v in values):
            raise ValueError("routing dimensions must be finite and positive")
        if any(not isfinite(v) or v < 0 for v in (self.start_margin_mm, self.end_margin_mm)):
            raise ValueError("end margins must be finite and nonnegative")
        if any(not isfinite(v) for point in self.front_edge_mm for v in point):
            raise ValueError("front edge coordinates must be finite")
        if self.edge_length_mm <= 0:
            raise ValueError("front edge needs distinct endpoints")
        if self.cable_width_mm >= self.profile.groove_width_mm:
            raise ValueError("rear cable relief must retain profile seating shoulders")
        if self.cable_depth_mm <= self.profile.groove_depth_mm:
            raise ValueError("cable depth is total depth and must extend behind the profile")
        if 2*self.cutter_radius_mm >= self.cable_width_mm:
            raise ValueError("cutter radius must fit the cable relief")
        pocket = self.connector_pocket
        if pocket is not None:
            dimensions = (pocket.length_mm, pocket.width_mm, pocket.depth_mm,
                          pocket.corner_radius_mm, pocket.light_setback_mm)
            if any(not isfinite(v) or v <= 0 for v in dimensions):
                raise ValueError("connector pocket dimensions must be finite and positive")
            if pocket.light_setback_mm > pocket.length_mm:
                raise ValueError("connector pocket must reach the light start")
            if 2*pocket.corner_radius_mm >= min(pocket.length_mm, pocket.width_mm):
                raise ValueError("connector cutter radius must fit its pocket")

    @property
    def edge_length_mm(self):
        start, end = self.front_edge_mm
        return hypot(end[0]-start[0], end[1]-start[1])
