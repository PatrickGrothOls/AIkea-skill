"""Scope: Reject changed or source-swapped KA 4532 purchased geometry."""

import pytest

from hettich_ka_4532_step_signature_test_support import (
    HettichKa4532StepSignatureTestSupport,
)
from hettich_ka_4532_step_signatures import (
    HettichKa4532StepSignatureClassifier,
    HettichKa4532StepSignatureError,
)


class TestHettichKa4532StepSignatureClassifier:
    """Protect role classification with product-specific native measurements."""

    _SUPPORT = HettichKa4532StepSignatureTestSupport()

    def test_classifies_the_exact_solids_independent_of_import_order(self) -> None:
        solids = self._SUPPORT.solids()

        classified = HettichKa4532StepSignatureClassifier().classify(
            (
                solids["right-moving"],
                solids["left-fixed"],
                solids["right-fixed"],
                solids["left-moving"],
            ),
            solids["spacer"],
        )

        assert classified.left_fixed is solids["left-fixed"]
        assert classified.left_moving is solids["left-moving"]
        assert classified.right_moving is solids["right-moving"]
        assert classified.right_fixed is solids["right-fixed"]
        assert classified.spacer is solids["spacer"]

    def test_rejects_changed_geometry_before_assigning_a_role(self) -> None:
        solids = self._SUPPORT.solids()
        solids["left-moving"] = self._SUPPORT.changed("left-moving", 6, 1.0)

        with pytest.raises(HettichKa4532StepSignatureError, match="does not match"):
            self._classify(solids)

    def test_rejects_a_duplicate_solid_in_place_of_another_role(self) -> None:
        solids = self._SUPPORT.solids()
        solids["right-fixed"] = solids["left-fixed"]

        with pytest.raises(HettichKa4532StepSignatureError, match="incomplete"):
            self._classify(solids)

    def test_rejects_spacer_geometry_supplied_as_a_runner_source(self) -> None:
        solids = self._SUPPORT.solids()
        solids["right-fixed"], solids["spacer"] = (
            solids["spacer"],
            solids["right-fixed"],
        )

        with pytest.raises(HettichKa4532StepSignatureError):
            self._classify(solids)

    def _classify(self, solids):
        return HettichKa4532StepSignatureClassifier().classify(
            (
                solids["left-fixed"],
                solids["left-moving"],
                solids["right-moving"],
                solids["right-fixed"],
            ),
            solids["spacer"],
        )
