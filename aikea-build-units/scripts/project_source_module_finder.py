"""Scope: Load authored assembly modules from current source instead of timestamp bytecode."""

from importlib.abc import MetaPathFinder
from importlib.machinery import PathFinder, SourceFileLoader
from pathlib import Path


class CurrentProjectSourceLoader(SourceFileLoader):
    def get_code(self, fullname):
        path = self.get_filename(fullname)
        return self.source_to_code(self.get_data(path), path)


class ProjectSourceModuleFinder(MetaPathFinder):
    def __init__(self, project_root):
        self.directory = (Path(project_root) / "assemblies").resolve()

    def find_spec(self, fullname, path=None, target=None):
        if fullname != "assemblies" and not fullname.startswith("assemblies."):
            return None
        spec = PathFinder.find_spec(fullname, path, target)
        if spec is None or not isinstance(spec.loader, SourceFileLoader):
            return None
        if not Path(spec.origin).resolve().is_relative_to(self.directory):
            return None
        spec.loader = CurrentProjectSourceLoader(fullname, spec.origin)
        return spec
