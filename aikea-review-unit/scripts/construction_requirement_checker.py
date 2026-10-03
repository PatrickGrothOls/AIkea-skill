"""Scope: Reconcile declared construction obligations with exact physical participants."""

from fabrication_readiness_report import FabricationReadinessCheck


class ConstructionRequirementChecker:
    """Check declared coverage; never infer a missing brief or certify structural capacity."""

    def check(self, visits, feature_operations=None):
        assemblies = tuple(item for item in visits if hasattr(item, "assembly"))
        physical = {"/".join(item.path): item for item in visits
                    if hasattr(item, "part") or hasattr(item, "hardware")}
        operations = dict(feature_operations or {})
        for item in assemblies:
            owner = "/".join(item.path)
            for joint in item.assembly.joints:
                if joint.joint_type != "unresolved":
                    operations[f"{owner}/joint:{joint.joint_id}"] = {
                        f"{owner}/part:{part}" for part in joint.participant_ids
                    }
            for request in getattr(item.assembly.spec, "machining", ()):
                operations[f"{owner}/machining:{request.machining_id}"] = {
                    f"{owner}/part:{request.part_id}"
                }
        covered, problems = set(), []
        for item in assemblies:
            owner = "/".join(item.path)
            requirements = getattr(item.assembly.spec, "requirements", None)
            if requirements is None:
                problems.append(f"{owner}: construction requirements have not been assessed")
                continue
            ids = [requirement.requirement_id for requirement in requirements]
            if len(ids) != len(set(ids)):
                problems.append(f"{owner}: duplicate requirement IDs")
            for requirement in requirements:
                subjects = {f"{owner}/{path}" for path in requirement.subject_paths}
                covered.update(subjects)
                error = self._requirement(owner, requirement, subjects, physical, operations)
                if error:
                    problems.append(f"{owner}/requirement:{requirement.requirement_id}: {error}")
        problems.extend(f"{path}: no declared support, attachment or intentional disposition"
                        for path in physical.keys() - covered)
        return (
            FabricationReadinessCheck("construction.requirement_coverage", not problems, tuple(sorted(problems))),
            self._identities(physical),
        )

    def _requirement(self, owner, requirement, subjects, physical, operations):
        if not requirement.requirement_id.strip() or not requirement.description.strip():
            return "an ID and description are required"
        if not subjects or not subjects <= physical.keys():
            return "subjects must name existing owner-relative physical paths"
        if len(subjects) != len(requirement.subject_paths):
            return "duplicate physical subjects"
        if requirement.disposition == "operations":
            paths = tuple(f"{owner}/{path}" for path in requirement.operation_paths)
            if not paths or any(path not in operations for path in paths):
                return "required operation is missing, unfinished or lacks feature evidence"
            affected = set().union(*(operations[path] for path in paths))
            if not subjects <= affected:
                return "the referenced operations do not cover every required participant"
            return None
        if requirement.disposition in {"loose", "floor_contact"}:
            if requirement.operation_paths or not requirement.basis.strip():
                return "an intentional disposition needs a rationale and no operation claim"
            if any(hasattr(physical[path], "hardware") for path in subjects):
                return "purchased hardware needs an explicit installation operation"
            return None
        return "unresolved construction requirement"

    def _identities(self, physical):
        missing = []
        for path, item in physical.items():
            if hasattr(item, "part"):
                if not getattr(item.part.spec, "material_id", "").strip():
                    missing.append(f"{path}: missing selected material")
            elif not all(getattr(item.hardware.spec, field, "").strip()
                         for field in ("manufacturer", "product_code", "hardware_asset_id")):
                missing.append(f"{path}: missing exact purchased product identity")
        return FabricationReadinessCheck("construction.material_and_product_identity", not missing, tuple(missing))
