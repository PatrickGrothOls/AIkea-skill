"""Scope: Declare a rectangular layered front and its unmachined adhesive joint."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class FrameBorders:
    left_mm: float
    right_mm: float
    bottom_mm: float
    top_mm: float


@dataclass(frozen=True)
class FramedFrontSpec:
    assembly_id: str
    width_mm: float
    height_mm: float
    backing_thickness_mm: float
    frame_thickness_mm: float
    borders: FrameBorders
    opening_corner_radius_mm: float
    purpose: str = "framed front"
    adhesive_product: str | None = None

    def __post_init__(self):
        b = self.borders
        dimensions = (self.width_mm, self.height_mm, self.backing_thickness_mm,
                      self.frame_thickness_mm, b.left_mm, b.right_mm,
                      b.bottom_mm, b.top_mm)
        if not all(isfinite(value) and value > 0 for value in dimensions):
            raise ValueError("front dimensions and borders must be finite and positive")
        if min(self.opening_size_mm) <= 0:
            raise ValueError("frame borders must leave a positive opening")
        radius = self.opening_corner_radius_mm
        if not isfinite(radius) or not 0 <= radius < min(self.opening_size_mm)/2:
            raise ValueError("opening corner radius must fit inside the opening")

    @property
    def opening_size_mm(self):
        return (self.width_mm-self.borders.left_mm-self.borders.right_mm,
                self.height_mm-self.borders.bottom_mm-self.borders.top_mm)

    @property
    def total_thickness_mm(self):
        return self.backing_thickness_mm+self.frame_thickness_mm


@dataclass(frozen=True)
class AppliedFrameGlueJoint:
    adhesive_product: str | None = None
    joint_id: str = "frame_to_backing"
    participant_ids: tuple[str, str] = ("backing", "frame")
    purpose: str = "applied frame attachment"
    joint_type: str = "face_glue"
    strength_verified: bool = False
