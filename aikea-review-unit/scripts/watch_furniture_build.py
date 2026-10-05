"""Scope: Keep one local preview open and rebuild stable saved construction inputs."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import webbrowser

from build_furniture_design import FurnitureDesignBuild
from construction_input_fingerprint import ConstructionInputFingerprinter
from live_build_observer import LiveBuildObserver
from live_build_progress import LiveBuildProgress
from live_build_server import LiveBuildServer
from live_build_store import LiveBuildStore


class FurnitureBuildWatcher:
    """Serial builds coalesce saves; changed-in-flight inputs trigger another build."""

    def __init__(self, project, assembly, store):
        self.project, self.assembly, self.store = project, assembly, store
        self.fingerprint = ConstructionInputFingerprinter()
        self.previous = None

    def rebuild(self):
        observer = LiveBuildObserver(self.store, self.assembly)
        self.store.begin()
        # Authored Python/CAD execution is the external boundary. Preserve failures
        # here, never suppress them inside geometry or construction validation.
        try:
            with LiveBuildProgress(observer):
                return FurnitureDesignBuild().build(
                    self.project, self.assembly, self.store.directory / "complete.glb", progress=observer)
        except Exception as error:
            self.store.status("failed", message="The saved design could not be rebuilt. Previous geometry is retained.",
                              problems=(f"{type(error).__name__}: {error}",))
            return None

    def tick(self):
        snapshot = self.fingerprint.source_inputs(self.project)
        if snapshot == self.previous:
            return
        time.sleep(0.6)
        if self.fingerprint.source_inputs(self.project) != snapshot:
            return
        self.previous = snapshot
        self.rebuild()


class WatchFurnitureBuildCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        parser.add_argument("--assembly", default="furniture_01")
        parser.add_argument("--port", type=int, default=0)
        parser.add_argument("--no-open", action="store_true")
        args = parser.parse_args()
        viewer = Path(__file__).resolve().parents[1] / "assets/viewer"
        with TemporaryDirectory(prefix="aikea-live-") as directory:
            store = LiveBuildStore(Path(directory))
            store.status("waiting", message="Waiting for the first saved design")
            server = LiveBuildServer(viewer, store.directory, args.port)
            server.start()
            print(json.dumps({"url": server.url, "mode": "live-draft"}), flush=True)
            if not args.no_open:
                webbrowser.open(server.url)
            watcher = FurnitureBuildWatcher(args.project.resolve(), args.assembly, store)
            try:
                while True:
                    watcher.tick()
                    time.sleep(0.5)
            except KeyboardInterrupt:
                store.status("paused", message="Live build stopped")
            finally:
                server.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(WatchFurnitureBuildCommand().run())
