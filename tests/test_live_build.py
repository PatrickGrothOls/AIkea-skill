"""Scope: Verify real per-part CAD publication and honest live-build failure states."""

import json
from pathlib import Path

from furniture_design_project import FurnitureDesignProject
from live_build_store import LiveBuildStore
from watch_furniture_build import FurnitureBuildWatcher
from live_build_progress import LiveBuildProgress


class RecordingLiveStore(LiveBuildStore):
    def __init__(self, directory):
        super().__init__(directory)
        self.events = []

    def status(self, *args, **kwargs):
        super().status(*args, **kwargs)
        self.events.append(json.loads((self.directory / "revision.json").read_text()))


class TestLiveBuild:
    def project(self, root):
        FurnitureDesignProject().initialize(root)
        package = root / "assemblies/furniture_01"
        package.mkdir()
        (package / "__init__.py").write_text("")
        builder = package / "builder.py"
        builder.write_text('''"""Scope: Build two real placed panels for live preview verification."""
import cadquery as cq
from assemblies.specification import PartSpec, IDENTITY_LOCAL_TO_PARENT, LocalToParentPlacement, Point3D
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder
ENVELOPE = cq.Workplane("XY").box(500, 500, 500, centered=False)
class Builder:
    def build(self):
        placement = LocalToParentPlacement(Point3D(120, 0, 0), IDENTITY_LOCAL_TO_PARENT.axis_basis)
        parts = (
            PartSpec("first", "panel", (), IDENTITY_LOCAL_TO_PARENT, local_size_mm=(100, 100, 18)),
            PartSpec("second", "panel", (), placement, local_size_mm=(100, 100, 18)),
        )
        result = PanelAssemblyBuilder(PanelAssemblySpec("furniture_01", "test", parts)).build()
        return result
BUILDER = Builder()
''')
        return builder

    def test_streams_actual_parts_before_complete_checks_and_reconciles_removals(self, tmp_path):
        builder = self.project(tmp_path)
        store = RecordingLiveStore(tmp_path / "live")
        watcher = FurnitureBuildWatcher(tmp_path, "furniture_01", store)
        report = watcher.rebuild()
        assert report["part_count"] == 2
        assert LiveBuildProgress.current.get() is None
        events = [event for event in store.events if event["message"].startswith("Built ")]
        assert [len(event["parts"]) for event in events] == [1, 2]
        assert events[0]["active"] == "furniture_01"
        assert store.events.index(events[-1]) < next(i for i, e in enumerate(store.events) if e["state"] == "checking")
        for part in store.parts.values():
            asset = store.directory / Path(part["url"]).name
            assert asset.read_bytes().startswith(b"glTF")
        assert not store.events[-1]["fabrication_ready"]
        unchanged = dict(store.parts)
        watcher.rebuild()
        assert store.parts == unchanged
        builder.write_text(builder.read_text().replace('"test", parts)', '"test", parts[:1])'))
        watcher.rebuild()
        assert list(store.parts) == ["furniture_01/part:first"]

    def test_failed_edit_keeps_geometry_and_stops_active_status(self, tmp_path):
        builder = self.project(tmp_path)
        store = RecordingLiveStore(tmp_path / "live")
        watcher = FurnitureBuildWatcher(tmp_path, "furniture_01", store)
        watcher.rebuild()
        previous = dict(store.parts)
        builder.write_text("this is not valid python!")
        assert watcher.rebuild() is None
        assert store.parts == previous
        assert store.events[-1]["state"] == "failed"
        assert store.events[-1]["active"] == ""
        assert "SyntaxError" in store.events[-1]["problems"][0]

    def test_failed_mid_build_keeps_completed_parts(self, tmp_path):
        builder = self.project(tmp_path)
        builder.write_text(builder.read_text().replace("return result", 'raise RuntimeError("test stop after panels")'))
        store = RecordingLiveStore(tmp_path / "live")
        assert FurnitureBuildWatcher(tmp_path, "furniture_01", store).rebuild() is None
        assert len(store.parts) == 2
        assert store.events[-1]["state"] == "failed"
        assert LiveBuildProgress.current.get() is None

    def test_unchanged_inputs_do_not_rebuild(self, tmp_path, monkeypatch):
        self.project(tmp_path)
        watcher = FurnitureBuildWatcher(tmp_path, "furniture_01", RecordingLiveStore(tmp_path / "live"))
        builds = []
        monkeypatch.setattr(watcher, "rebuild", lambda: builds.append(True))
        monkeypatch.setattr("watch_furniture_build.time.sleep", lambda _: None)
        watcher.tick()
        watcher.tick()
        assert builds == [True]

    def test_nested_events_use_declared_rotated_parent_frames(self, tmp_path):
        from test_furniture_geometry_check import TestFurnitureGeometryCheck as Fixture
        builder = self.project(tmp_path)
        source = Fixture().design_source().replace(
            "import cadquery as cq", "import cadquery as cq\nfrom live_build_progress import LiveBuildChild")
        source = source.replace("        return PanelAssemblyBuilder(root, children=(\n            BuiltChildAssembly(child_spec, PanelAssemblyBuilder(child).build()),)).build()",
            "        with LiveBuildChild(child_spec):\n            built = PanelAssemblyBuilder(child).build()\n"
            "        return PanelAssemblyBuilder(root, children=(BuiltChildAssembly(child_spec, built),)).build()")
        builder.write_text(source)
        store = RecordingLiveStore(tmp_path / "live")
        report = FurnitureBuildWatcher(tmp_path, "furniture_01", store).rebuild()
        assert report["status"] == "valid"
        event = next(e for e in store.events if e["message"] == "Built surface")
        assert event["active"] == "furniture_01/raised_01"
        assert event["parts"][0]["id"] == "furniture_01/raised_01/part:surface"
        # Early and final geometry share the exact same placed asset.
        assert event["parts"][0]["hash"] == store.parts["furniture_01/raised_01/part:surface"]["hash"]
