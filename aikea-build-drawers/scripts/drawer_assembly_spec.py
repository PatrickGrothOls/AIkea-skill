"""Scope: Define one resolved drawer child assembly without vendor CAD geometry."""

from __future__ import annotations

from dataclasses import dataclass

from drawer_box_spec import DrawerBoxSpec, DrawerPartSpec


@dataclass(frozen=True, slots=True)
class DrawerAssemblySpec:
    """Own the wooden box and selected purchased-runner identity."""

    assembly_id: str
    purpose: str
    runner_product_code: str
    runner_item_number: str
    hardware_geometry_state: str
    box: DrawerBoxSpec
    child_assemblies: tuple = ()
    purchased_hardware: tuple = ()
    joints: tuple = ()
    machining: tuple = ()
    requirements: tuple | None = None

    @property
    def parts(self) -> tuple[DrawerPartSpec, ...]:
        return self.box.parts

    def part(self, part_id: str) -> DrawerPartSpec:
        return self.box.part(part_id)


__all__ = ["DrawerAssemblySpec"]
