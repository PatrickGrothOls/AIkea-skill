"""Scope: Qualify declared extension participants using current scoped manufacturing evidence."""

from construction_input_fingerprint import ConstructionInputFingerprinter
from fabrication_feature_evidence_checker import FabricationFeatureEvidenceChecker


class ConstructionFeatureQualification:
    """Reuse registered feature reports; plausible geometry alone does not qualify an extension."""

    def resolve(self, root, tree, visits):
        owners = {self._path(item.path): item for item in visits if hasattr(item, "assembly")}
        qualified, features = set(), {}
        for scope, data, subjects in self.current_scopes(root, tree, visits):
            owner = owners[scope.owner_path]
            path = "/".join(owner.path)
            features[f"{path}/feature:{scope.module}"] = subjects
            claimed = data.get("qualified_joint_ids")
            if claimed != list(scope.qualified_joint_ids):
                continue
            for joint in owner.assembly.joints:
                participants = {f"{scope.owner_path}/{part}" for part in joint.participant_ids}
                if joint.joint_id in claimed and participants <= set(scope.expected_paths):
                    qualified.add(f"{path}/joint:{joint.joint_id}")
        return frozenset(qualified), features

    def current_scopes(self, root, tree, visits):
        fingerprint = ConstructionInputFingerprinter().build(root, visits)
        physical = {self._path(item.path): "/".join(item.path) for item in visits
                    if hasattr(item, "part")}
        hardware = {self._path(item.path): "/".join(item.path) for item in visits
                    if hasattr(item, "hardware")}
        current = []
        for scope, data in FabricationFeatureEvidenceChecker().validated_scopes(root, tree, visits):
            if data.get("construction_sha256") != fingerprint:
                continue
            if not set(scope.expected_paths) <= physical.keys() or not scope.expected_paths:
                continue
            installed = data.get("purchased_hardware_paths", [])
            if (not isinstance(installed, list) or installed != list(scope.expected_hardware_paths)
                    or not set(installed) <= hardware.keys()):
                continue
            subjects = (
                {physical[item] for item in scope.expected_paths} | {hardware[item] for item in installed}
            )
            current.append((scope, data, subjects))
        return tuple(current)

    def _path(self, path):
        return "/".join(segment.split(":", 1)[-1] for segment in path)
