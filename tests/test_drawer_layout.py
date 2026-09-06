"""Scope: Verify drawer layout identifiers are stable generated child names."""

from __future__ import annotations

import pytest

from cabinet_drawer_plan import DrawerLayout


class TestDrawerLayout:
    """Reject identifiers that could escape or invalidate generated modules."""

    @pytest.mark.parametrize(
        "drawer_id",
        (
            "drawer-01",
            "Drawer_01",
            "1_drawer_01",
            "drawer_1",
            "class",
            "../escaped_01",
        ),
    )
    def test_rejects_unstable_drawer_ids(self, drawer_id: str) -> None:
        with pytest.raises(ValueError, match="stable lowercase"):
            DrawerLayout(drawer_id, bottom_height_mm=356.0)


__all__ = ["TestDrawerLayout"]
