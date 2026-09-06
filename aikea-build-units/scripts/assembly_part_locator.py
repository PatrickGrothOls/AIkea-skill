"""Scope: Expose a part's declared assembly frame as a CadQuery location."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from local_to_parent_location import LocalToParentLocation


class AssemblyPartLocator:
    """Read part placement from the assembly-owned specification."""

    def __init__(self) -> None:
        self.location = LocalToParentLocation()

    def locate(self, part: Any, _assembly: Any, _base_height_mm: float) -> cq.Location:
        return self.location.build(part.local_to_parent)


__all__ = ["AssemblyPartLocator"]
