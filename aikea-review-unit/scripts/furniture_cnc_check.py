"""Scope: Check every manufactured tree part in its local CNC cutting frame."""

from math import isfinite

from cnc_work_area import CNC_2500_X_2000_8MM


class FurnitureCncCheck:
    """Validate blanks and actual geometry independently of assembled dimensions."""

    def __init__(self, work_area=CNC_2500_X_2000_8MM):
        self.work_area = work_area

    def check(self, visits) -> dict:
        checked = []
        oversized = []
        for item in visits:
            if type(item).__name__ != "AssemblyTreePart":
                continue
            part = item.part
            bounds = part.solid.val().BoundingBox()
            actual = (bounds.xlen, bounds.ylen, bounds.zlen)
            declared = part.spec.local_size_mm or actual
            if len(declared) != 3 or any(not isfinite(value) or value <= 0 for value in declared):
                raise ValueError(
                    f"{'/'.join(item.path)}: local_size_mm must be empty or three finite positive dimensions"
                )
            size = tuple(max(declared[index], actual[index]) for index in range(3))
            record = {"part": "/".join(item.path), "blank_size_mm": list(size)}
            checked.append(record)
            if not self.work_area.fits(*size[:2]) or max(size) > max(
                self.work_area.usable_x_mm, self.work_area.usable_y_mm
            ):
                oversized.append(record)
        return {
            "status": "invalid" if oversized else "valid",
            "profile_id": self.work_area.profile_id,
            "usable_xy_mm": [self.work_area.usable_x_mm, self.work_area.usable_y_mm],
            "checked_part_count": len(checked),
            "parts": checked,
            "oversized_parts": oversized,
            "scope": "Local blank extents with 90-degree rotation; stock, grain and toolpaths need separate checks.",
        }
