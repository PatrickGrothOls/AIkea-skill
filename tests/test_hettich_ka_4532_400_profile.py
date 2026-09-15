"""Scope: Test exact 400 mm identity, role classification and official opening verification."""
from dataclasses import dataclass, replace
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from hettich_ka_4532_400_profile import HETTICH_KA_4532_400
from hettich_ka_4532_400_step_set import HettichKa4532FourHundredClassifier, HettichKa4532FourHundredStepLoader
from hettich_ka_4532_400_opening_check import HettichKa4532FourHundredOpeningCheck


@dataclass(frozen=True)
class MeasuredSolid:
    values: tuple[float, ...]
    valid: bool = True

    def isValid(self):
        return self.valid

    def BoundingBox(self):
        return SimpleNamespace(**dict(zip(("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"), self.values[:6])))

    def Volume(self):
        return self.values[-1]


class TestKa4532FourHundredProfile:
    def members(self):
        # Saved independent native source observations; no source geometry is distributed.
        return [MeasuredSolid(row) for row in (
            (0, 8.777139874, -9.5, 392.983917012, -22.85009328, 22.85009328, 37318.87023579049),
            (4.2, 12.5, -9.5, 390.54, -12.149518924, 12.149518924, 19221.9871163936),
            (188.5, 196.8, -9.5, 390.54, -12.149518924, 12.149518924, 19221.987116393564),
            (192.222860126, 201, -9.5, 392.983917012, -22.85009328, 22.85009328, 37318.87027145874))]

    def test_400_drawing_datums_do_not_inherit_the_500_pattern(self):
        profile = HETTICH_KA_4532_400
        fixed, moving = profile.fixing_patterns
        assert profile.article == "9114274" and profile.minimum_cabinet_depth_mm == 404
        assert fixed.front_depth_axes_mm == (37, 165, 229)
        assert moving.front_depth_axes_mm == (37, 165, 291)
        assert profile.native_front_mm+profile.native_to_front_offset_mm == 2
        assert 261 not in fixed.front_depth_axes_mm and 325 not in fixed.front_depth_axes_mm

    def test_roles_are_independent_of_import_order(self):
        source = self.members()
        actual = HettichKa4532FourHundredClassifier().classify(tuple(reversed(source)))
        assert actual["left-fixed"] is source[0] and actual["right-fixed"] is source[3]
        assert actual["left-moving"] is source[1] and actual["right-moving"] is source[2]

    @pytest.mark.parametrize("failure", ("duplicate", "missing", "length", "volume", "invalid"))
    def test_wrong_members_fail_before_placement(self, failure):
        members = self.members()
        if failure == "duplicate":
            members[-1] = members[0]
        elif failure == "missing":
            members.pop()
        elif failure == "invalid":
            members[0] = replace(members[0], valid=False)
        else:
            values = list(members[0].values)
            values[3 if failure == "length" else 6] += 100
            members[0] = MeasuredSolid(tuple(values))
        with pytest.raises(ValueError):
            HettichKa4532FourHundredClassifier().classify(members)

    def test_changed_file_is_rejected_before_import(self, tmp_path):
        (tmp_path/"9114274.stp").write_text("changed source")
        with pytest.raises(ValueError):
            HettichKa4532FourHundredStepLoader().load(tmp_path)

    def test_exact_source_all_twelve_openings_and_wrong_axis(self):
        source = os.environ.get("AIKEA_TEST_KA4532_400_SOURCE")
        if source is None:
            pytest.skip("Supply project-local unchanged vendor STEP for the integration check")
        step_set = HettichKa4532FourHundredStepLoader().load(Path(source))
        checker = HettichKa4532FourHundredOpeningCheck()
        report = checker.verify(step_set)
        assert report["status"] == "PASS" and report["opening_count"] == 12
        assert not report["manufacturing_authority"]
        assert all(row["corridor_intersection_mm3"] <= 1e-5 for row in report["openings"])
        with pytest.raises(ValueError, match="cylindrical boundary"):
            checker.require_opening(step_set.members["left-fixed"], 249.5, 6.4, 0)
