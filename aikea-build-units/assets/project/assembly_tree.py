"""Scope: Traverse every physical item in a recursively built assembly tree."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TypeAlias

from .assembly_placement import (
    IDENTITY_LOCAL_TO_PARENT,
    LocalToParentPlacement,
)
from .specification import (
    BuiltAssembly,
    BuiltPart,
    BuiltPurchasedHardware,
)


class AssemblyTreeError(ValueError):
    """Report a built physical item that cannot be placed in the tree."""


@dataclass(frozen=True)
class AssemblyTreeAssembly:
    """Expose one assembly and its accumulated frame at the tree root."""

    path: tuple[str, ...]
    assembly: BuiltAssembly
    local_to_root: LocalToParentPlacement


@dataclass(frozen=True)
class AssemblyTreePart:
    """Expose one manufactured part in the root assembly frame."""

    path: tuple[str, ...]
    part: BuiltPart
    local_to_root: LocalToParentPlacement


@dataclass(frozen=True)
class AssemblyTreeHardware:
    """Expose one purchased item and its optional physical root placement."""

    path: tuple[str, ...]
    hardware: BuiltPurchasedHardware
    local_to_root: LocalToParentPlacement | None


AssemblyTreeItem: TypeAlias = (
    AssemblyTreeAssembly | AssemblyTreePart | AssemblyTreeHardware
)


class AssemblyTreeWalker:
    """Walk arbitrary assembly depth while accumulating every local frame."""

    def walk(
        self,
        root: BuiltAssembly,
        root_placement: LocalToParentPlacement = IDENTITY_LOCAL_TO_PARENT,
    ) -> tuple[AssemblyTreeItem, ...]:
        root_path = (root.spec.assembly_id,)
        return tuple(self._walk_assembly(root, root_path, root_placement))

    def _walk_assembly(
        self,
        assembly: BuiltAssembly,
        path: tuple[str, ...],
        local_to_root: LocalToParentPlacement,
    ) -> Iterator[AssemblyTreeItem]:
        yield AssemblyTreeAssembly(path, assembly, local_to_root)
        for part in assembly.parts:
            yield AssemblyTreePart(
                path + (f"part:{part.spec.part_id}",),
                part,
                local_to_root.compose_child(part.spec.local_to_parent),
            )
        for hardware in assembly.purchased_hardware:
            placement = hardware.spec.local_to_parent
            if hardware.has_geometry and placement is None:
                raise AssemblyTreeError(
                    "geometric hardware has no local placement: "
                    f"{'/'.join(path)}/{hardware.spec.hardware_id}"
                )
            yield AssemblyTreeHardware(
                path + (f"hardware:{hardware.spec.hardware_id}",),
                hardware,
                local_to_root.compose_child(placement) if placement else None,
            )
        for child in assembly.child_assemblies:
            child_path = path + (child.spec.assembly_id,)
            child_to_root = local_to_root.compose_child(child.spec.local_to_parent)
            yield from self._walk_assembly(
                child.assembly,
                child_path,
                child_to_root,
            )


__all__ = [
    "AssemblyTreeAssembly",
    "AssemblyTreeError",
    "AssemblyTreeHardware",
    "AssemblyTreeItem",
    "AssemblyTreePart",
    "AssemblyTreeWalker",
]
