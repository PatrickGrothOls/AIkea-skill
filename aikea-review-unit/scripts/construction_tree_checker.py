"""Scope: Report construction integrity for every owner in a complete built tree."""

from construction_result_validator import ConstructionResultValidator
from fabrication_readiness_report import FabricationReadinessCheck
from part_construction_error import PartConstructionError


class ConstructionTreeChecker:
    """Apply the shared output checks to configured, custom and extended builders."""

    def check(self, visits, qualified_operations=frozenset()):
        problems, extensions = [], []
        for visit in visits:
            if not hasattr(visit, "assembly"):
                continue
            path = "/".join(visit.path)
            try:
                unqualified = ConstructionResultValidator().validate(visit.assembly)
            except PartConstructionError as error:
                problems.append(f"{path}: {error}")
                continue
            extensions.extend(f"{path}/joint:{joint.joint_id}: {joint.joint_type} needs qualification"
                              for joint in unqualified
                              if f"{path}/joint:{joint.joint_id}" not in qualified_operations)
        return (
            FabricationReadinessCheck("construction.applied_operations", not problems, tuple(problems)),
            FabricationReadinessCheck("construction.extension_qualification", not extensions, tuple(extensions)),
        )
