"""Scope: Reject timestamp-bytecode staleness for saved assembly inputs and builders."""

import importlib
import os
import py_compile
import sys

import pytest

from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from generated_project_module_runtime import GeneratedProjectModuleRuntime


class TestProjectSourceFreshness:
    @pytest.mark.parametrize("loader", ("specification", "geometry"))
    def test_same_size_same_mtime_edit_bypasses_old_bytecode_in_both_routes(self, tmp_path, loader):
        path = self._project(tmp_path)
        before = path.stat()
        py_compile.compile(str(path), doraise=True)
        path.write_text("VALUE = 51\n")
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        meta_path = list(sys.meta_path)
        if loader == "specification":
            module = CabinetAssemblySpecLoader().load_module(tmp_path, "cabinet_01")
        else:
            module = GeneratedProjectModuleRuntime().execute(tmp_path,
                lambda: importlib.import_module("assemblies.cabinet_01.spec"))
        assert module.VALUE == 51
        assert sys.meta_path == meta_path
        assert "assemblies.cabinet_01.spec" not in sys.modules

    def test_source_error_restores_runtime_instead_of_using_old_valid_bytecode(self, tmp_path):
        path = self._project(tmp_path)
        py_compile.compile(str(path), doraise=True)
        path.write_text("VALUE = ?!\n")
        meta_path, python_path = list(sys.meta_path), list(sys.path)
        with pytest.raises(SyntaxError):
            CabinetAssemblySpecLoader().load_module(tmp_path, "cabinet_01")
        assert sys.meta_path == meta_path and sys.path == python_path

    def _project(self, root):
        parent = root/"assemblies/cabinet_01"
        parent.mkdir(parents=True)
        for package in (parent, parent.parent):
            (package/"__init__.py").write_text('"""Scope: Own the freshness fixture."""\n')
        (parent/"spec.py").write_text("from .value import VALUE\n")
        path = parent/"value.py"
        path.write_text("VALUE = 50\n")
        return path
