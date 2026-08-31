"""Scope: Apply generic local review motions to accumulated assembly-tree frames."""

from __future__ import annotations

from typing import Any

from assembly_tree_review_plan import AssemblyTreeReviewPlan
from local_to_parent_location import LocalToParentLocation
from unit_mockup import UnitMockupInputError


class AssemblyTreePoseResolver:
    """Rebuild posed assembly frames while preserving every saved relative frame."""

    def __init__(self) -> None:
        self.locations = LocalToParentLocation()

    def assembly_locations(
        self,
        assemblies: dict[tuple[str, ...], Any],
        plan: AssemblyTreeReviewPlan,
    ) -> dict[tuple[str, ...], Any]:
        resolved: dict[tuple[str, ...], Any] = {}
        originals = {
            path: self.locations.build(item.local_to_root)
            for path, item in assemblies.items()
        }
        for path in sorted(assemblies, key=len):
            if len(path) == 1:
                location = originals[path]
            else:
                parent_path = path[:-1]
                if parent_path not in resolved:
                    raise UnitMockupInputError(
                        ["assembly tree contains a child without its parent"]
                    )
                local_frame = originals[parent_path].inverse * originals[path]
                location = resolved[parent_path] * local_frame
            motion = plan.motion_for(path)
            resolved[path] = location * motion if motion is not None else location
        return resolved

    def item_location(
        self,
        item: Any,
        assemblies: dict[tuple[str, ...], Any],
        posed_assemblies: dict[tuple[str, ...], Any],
    ) -> Any:
        owner_path = item.path[:-1]
        original_owner = self.locations.build(
            assemblies[owner_path].local_to_root
        )
        original_item = self.locations.build(item.local_to_root)
        return posed_assemblies[owner_path] * (
            original_owner.inverse * original_item
        )


__all__ = ["AssemblyTreePoseResolver"]
