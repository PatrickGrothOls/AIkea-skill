"""Scope: Publish complete immutable part GLBs before an atomic live revision."""

from hashlib import sha256
import json
from pathlib import Path
import time
from uuid import uuid4

from cadquery_glb_exporter import CadQueryGlbExporter


class LiveBuildStore:
    """One writer owns this disposable preview cache; it is not review evidence."""

    def __init__(self, directory: Path):
        self.directory = directory
        directory.mkdir(parents=True, exist_ok=True)
        self.parts = {}
        self.revision = 0
        self.session = uuid4().hex
        self.cache = {}

    def publish(self, part, owner, identity):
        # Retain solid references so Python cannot recycle an identity mid-build.
        key = (id(part.solid), str(part.location.toTuple()), part.color)
        cached = self.cache.get(key)
        if cached is None:
            temporary = self.directory / "export.glb"
            CadQueryGlbExporter().export("live_part", (part,), temporary)
            digest = sha256(temporary.read_bytes()).hexdigest()
            temporary.replace(self.directory / f"{digest}.glb")
            self.cache[key] = (part.solid, digest)
        else:
            digest = cached[1]
        self.parts[identity] = {"id": identity, "owner": owner,
                                 "url": f"/parts/{digest}.glb", "hash": digest}

    def status(self, state, active="", message="", source=None, problems=()):
        self.revision += 1
        payload = {"session": self.session, "revision": self.revision,
                   "state": state, "active": active, "message": message,
                   "updated": time.time(), "parts": list(self.parts.values()),
                   "fabrication_ready": False, "source": source, "problems": list(problems)}
        temporary = self.directory / "revision.tmp"
        temporary.write_text(json.dumps(payload) + "\n")
        temporary.replace(self.directory / "revision.json")

    def begin(self):
        self.cache.clear()
        self.status("building", message="Building saved design; previous parts may be out of date")
