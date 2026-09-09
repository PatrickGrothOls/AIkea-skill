"""Scope: Count Cabineos only when layout and both participants' cuts agree."""

from collections import Counter

from cabineo_connector_layout import CabineoConnectorLayout


class CabineoItemCounter:
    """Retain a traceable occurrence for every verified connector and insert."""

    def count(self, visit, unresolved: list[dict]) -> list[dict]:
        assembly = visit.assembly
        owner = "/".join(visit.path)
        parts = {part.spec.part_id: part.spec for part in assembly.parts}
        joint_ids = [joint.joint_id for joint in assembly.joints]
        if len(joint_ids) != len(set(joint_ids)):
            raise ValueError(f"duplicate joint IDs in {owner}")
        unknown = {cut.joint_id for cut in assembly.cuts} - set(joint_ids)
        for joint_id in sorted(unknown):
            unresolved.append(dict(code="cut.unknown_joint", path=f"{owner}/{joint_id}"))
        occurrences = []
        for joint in assembly.joints:
            path = f"{owner}/joint:{joint.joint_id}"
            if joint.joint_type == "cabineo":
                occurrences.extend(self._joint(path, joint, parts, assembly.cuts, unresolved))
            elif joint.joint_type == "unresolved":
                unresolved.append(dict(code="joint.unresolved", path=path, purpose=joint.purpose))
        return occurrences

    def _joint(self, path, joint, parts, cuts, unresolved) -> list[dict]:
        participants = (joint.source_part_id, joint.target_part_id)
        if len(set(participants)) != 2 or not set(participants) <= parts.keys():
            unresolved.append(dict(code="cabineo.invalid_participants", path=path))
            return []
        positions = CabineoConnectorLayout().positions(joint, parts[joint.source_part_id])
        expected = Counter(
            (index, part_id)
            for index in range(1, len(positions) + 1)
            for part_id in participants
        )
        actual = Counter(
            (cut.connector_index, cut.part_id)
            for cut in cuts if cut.joint_id == joint.joint_id
        )
        if actual != expected:
            unresolved.append(dict(code="cabineo.cut_mismatch", path=path))
            return []
        owner = path.rsplit("/joint:", 1)[0]
        return [
            dict(
                path=f"{path}/connector:{index}",
                source_part_path=f"{owner}/part:{joint.source_part_id}",
                receiver_part_path=f"{owner}/part:{joint.target_part_id}",
                source_edge_position_mm=position,
            )
            for index, position in enumerate(positions, start=1)
        ]
