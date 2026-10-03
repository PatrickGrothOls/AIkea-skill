"""Scope: Orient and position a Cabineo cutter from one local face and edge."""

from __future__ import annotations

import cadquery as cq


class CabineoCutterPlacement:
    """Apply the proven orthogonal face-and-edge placement rules."""

    _ROTATIONS = {
        ("<Z", "<Y"): (),
        ("<Z", ">Y"): (("Z", 180),),
        ("<Z", "<X"): (("Z", -90),),
        ("<Z", ">X"): (("Z", 90),),
        (">Z", "<Y"): (("Y", 180),),
        (">Z", ">Y"): (("Z", 180), ("Y", 180)),
        (">Z", "<X"): (("Z", -90), ("X", 180)),
        (">Z", ">X"): (("Z", 90), ("X", 180)),
        ("<X", "<Y"): (("Y", 90),),
        ("<X", ">Y"): (("Y", 90), ("X", 180)),
        ("<X", "<Z"): (("Y", 90), ("X", 90)),
        ("<X", ">Z"): (("Y", 90), ("X", -90)),
        (">X", "<Y"): (("Y", -90),),
        (">X", ">Y"): (("Y", -90), ("X", 180)),
        (">X", "<Z"): (("Y", -90), ("X", 90)),
        (">X", ">Z"): (("Y", -90), ("X", -90)),
        ("<Y", "<X"): (("X", -90), ("Y", -90)),
        ("<Y", ">X"): (("X", -90), ("Y", 90)),
        ("<Y", "<Z"): (("X", -90), ("Y", 180)),
        ("<Y", ">Z"): (("X", -90),),
        (">Y", "<X"): (("X", 90), ("Y", 90)),
        (">Y", ">X"): (("X", 90), ("Y", -90)),
        (">Y", "<Z"): (("X", 90),),
        (">Y", ">Z"): (("X", 90), ("Y", 180)),
    }
    _AXIS_VECTOR = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}
    _FACE_DEPTH = {
        "<Z": ("Z", 1),
        ">Z": ("Z", -1),
        "<Y": ("Y", 1),
        ">Y": ("Y", -1),
        "<X": ("X", 1),
        ">X": ("X", -1),
    }

    def orient(self, shape: cq.Shape, face: str, edge: str) -> cq.Shape:
        rotations = self._ROTATIONS.get((face, edge))
        if rotations is None:
            raise ValueError(f"Unsupported (face, edge) combination: ({face}, {edge})")
        for axis_name, angle in rotations:
            shape = shape.rotate(
                (0, 0, 0),
                self._AXIS_VECTOR[axis_name],
                angle,
            )
        return shape

    def translate(
        self,
        shape: cq.Shape,
        face: str,
        edge: str,
        primary_offset_mm: float,
        panel_thickness_mm: float,
        edge_position_mm: float,
    ) -> cq.Shape:
        depth_axis, depth_sign = self._FACE_DEPTH[face]
        edge_axis = edge[-1]
        slide_axis = ({"X", "Y", "Z"} - {depth_axis, edge_axis}).pop()
        face_position = panel_thickness_mm if depth_sign < 0 else 0.0
        coordinates = {
            depth_axis: face_position,
            edge_axis: edge_position_mm,
            slide_axis: primary_offset_mm,
        }
        return shape.translate(
            (coordinates["X"], coordinates["Y"], coordinates["Z"])
        )


__all__ = ["CabineoCutterPlacement"]
