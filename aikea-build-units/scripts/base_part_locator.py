"""Scope: Expose a base part's declared frame as a CadQuery location."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from local_to_parent_location import LocalToParentLocation


class BasePartLocator:
    """Read structural-base placement from the assembly-owned specification."""

    def __init__(self) -> None:
        self.location = LocalToParentLocation()

    def locate(self, part: Any, _base: Any) -> cq.Location:
        return self.location.build(part.local_to_parent)


__all__ = ["BasePartLocator"]
