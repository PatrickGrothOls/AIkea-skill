"""Scope: Audit broad-face setup demands of supported declared panel operations."""

import cadquery as cq
from panel_joint_setup_faces import PanelJointSetupFaces


class PanelSetupChecker:
    """Find opposing/edge entry demands; this is not CAM or tool-reach approval."""

    _FACES = {"<Z", ">Z"}

    def check(self, assembly):
        parts = {part.part_id: part for part in assembly.spec.parts}
        demands = {part_id: [] for part_id in parts}
        for joint in assembly.joints:
            for part_id,faces in PanelJointSetupFaces().resolve(assembly.spec,joint).items():
                demands[part_id].append((joint.joint_id,faces))
        for request in assembly.spec.machining:
            part = parts[request.part_id]
            demands[part.part_id].append((request.machining_id, self._operation_faces(part, request)))
        rows = []
        for part in assembly.spec.parts:
            allowed = set(self._FACES)
            for _, faces in demands[part.part_id]:
                allowed &= faces
            rows.append({
                "part_id": part.part_id,
                "allowed_faces": sorted(allowed),
                "status": "compatible" if allowed else "conflict_or_unsupported",
                "operations": [{"id": name, "entry_faces": sorted(faces)}
                               for name, faces in demands[part.part_id]],
            })
        return {
            "scope": "Declared broad-face access for Cabineo, miter, Korrekt and surface operations",
            "machining_ready": False,
            "remaining": "Actual subtraction, connection coverage, stock, tool reach, workholding and CAM remain separate checks",
            "status": "compatible" if all(row["allowed_faces"] for row in rows) else "conflict_or_unsupported",
            "parts": rows,
        }

    def _operation_faces(self, part, request):
        if request.operation_type == "system_32":
            return {part.inside_face} & self._FACES
        if request.operation_type not in {"surface_holes", "surface_pocket", "surface_groove", "stepped_surface_recess"}:
            return set()
        axis = request.surface_to_part.axis_basis.local_z_in_parent
        faces = self._entry_faces(cq.Vector(axis.x, axis.y, axis.z))
        if not faces:
            return set()
        thickness = part.local_size_mm[2]
        depth = min(hole.depth_mm for hole in request.holes) if request.operation_type == "surface_holes" else request.depth_mm
        return set(self._FACES) if depth >= thickness else faces

    def _entry_faces(self, axis):
        if abs(axis.x) > 1e-7 or abs(axis.y) > 1e-7 or abs(abs(axis.z) - 1) > 1e-7:
            return set()
        return {"<Z" if axis.z > 0 else ">Z"}
