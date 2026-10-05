"""Scope: Place genuine build events in the declared root frame for live display."""

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart


class LiveBuildObserver:
    """Unknown custom parent frames wait for the final tree, never guess placement."""

    def __init__(self, store, assembly_id):
        self.store = store
        self.frames = [((assembly_id,), cq.Location())]

    def push(self, spec):
        path, placement = self.frames[-1]
        self.frames.append((path + (spec.assembly_id,),
                            placement * LocalToParentLocation().build(spec.local_to_parent)))
        self.store.status("building", "/".join(self.frames[-1][0]))

    def pop(self):
        self.frames.pop()

    def started(self, spec):
        path, _ = self.frames[-1]
        if spec.assembly_id == path[-1]:
            self.store.status("building", "/".join(path), f"Building {spec.assembly_id}")

    def part(self, spec, built):
        path, frame = self.frames[-1]
        if spec.assembly_id != path[-1]:
            return
        name = "__".join((*path[1:], built.spec.part_id))
        part = MockupPart(name, built.solid,
                          frame * LocalToParentLocation().build(built.spec.local_to_parent),
                          (0.78, 0.69, 0.55, 1.0))
        self.store.publish(part, "/".join(path), "/".join((*path, f"part:{built.spec.part_id}")))
        self.store.status("building", "/".join(path), f"Built {built.spec.part_id}")

    def checking(self, visits, parts):
        # Reconcile feature-modified panels and exact hardware from the actual tree.
        physical = [visit for visit in visits if not hasattr(visit, "assembly")]
        identities = []
        for part, visit in zip(parts, physical, strict=True):
            identity = "/".join(visit.path)
            identities.append(identity)
            self.store.publish(part, "/".join(visit.path[:-1]), identity)
        self.store.parts = {identity: self.store.parts[identity] for identity in identities}
        self.store.status("checking", self.frames[0][0][0], "Checking the complete assembly")

    def finished(self, report):
        passed = report["status"] == "valid" and report["construction_status"] == "verified_operations"
        problems = [problem for check in report["construction_checks"]
                    if not check["passed"] for problem in check["problems"]]
        if report["status"] != "valid":
            problems.append("Geometry or contact checks failed; inspect the complete geometry report.")
        self.store.status("checked" if passed else "failed", message=(
            "Build checks passed · formal review still required" if passed else
            "Checks need attention · this preview is not ready to build"),
            source=report["construction_sha256"], problems=problems)
