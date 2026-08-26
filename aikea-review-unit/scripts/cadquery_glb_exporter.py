"""Scope: Export one named visual cabinet assembly through CadQuery."""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

from unit_mockup import MockupPart


class CadQueryGlbExporter:
    """Preserve CadQuery as the authority for mock-up solids and GLB meshing."""

    def export(
        self,
        assembly_id: str,
        parts: tuple[MockupPart, ...],
        output: Path,
    ) -> None:
        assembly = cq.Assembly(name=assembly_id)
        for part in parts:
            assembly.add(
                part.solid,
                name=part.name,
                color=cq.Color(*part.color),
                loc=part.location,
            )
        assembly.save(
            str(output),
            exportType="GLTF",
            tolerance=0.1,
            angularTolerance=0.1,
        )
