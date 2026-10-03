"""Scope: Reuse installed engines without provisioning and retain background probe ownership."""
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError
import pytest
from unittest.mock import patch
from blender_bake_runtime import BlenderBakeRuntime


class TestBlenderBakeRuntime:
    def test_installed_cli_reuses_shared_worker_and_preserves_paths(self, tmp_path):
        output = tmp_path/"output with spaces"
        with patch("blender_bake_runtime.shutil.which", return_value="/Apps/Blender CLI"), \
                patch("blender_bake_runtime.BlenderEngineRuntime.ensure") as provision, \
                patch("blender_bake_runtime.subprocess.run", return_value=CompletedProcess([],0,"Blender 5.2.1 LTS\n")):
            command = BlenderBakeRuntime().command(tmp_path/"engine",output,1)
        provision.assert_not_called()
        assert command[:5] == ["/Apps/Blender CLI","--background","--factory-startup","--threads","1"]
        assert command[5:7] == ["--python-exit-code","1"]
        captured = {}
        # Execute only the argv adapter against a mocked run_path, never Blender.
        with patch("runpy.run_path") as run, patch("sys.path", []), patch("sys.argv", []):
            exec(command[-1],captured)
            assert captured["sys"].argv[1] == str(output)
            assert Path(run.call_args.args[0]).name == "run_blender_bake.py"

    def test_no_installed_engine_uses_provisioner(self, tmp_path):
        with patch("blender_bake_runtime.shutil.which", return_value=None), \
                patch("blender_bake_runtime.BlenderEngineRuntime.ensure",return_value=Path("/runtime/python")) as provision:
            command = BlenderBakeRuntime().command(tmp_path/"engine",tmp_path/"out",1)
        provision.assert_called_once()
        assert command[0] == "/runtime/python"
        assert Path(command[1]).name == "run_blender_bake.py"

    def test_incompatible_automatic_cli_uses_compatible_provisioner(self, tmp_path):
        with patch("blender_bake_runtime.shutil.which", return_value="/bin/blender"), \
                patch("blender_bake_runtime.subprocess.run", return_value=CompletedProcess([],0,"Blender 4.5.0\n")), \
                patch("blender_bake_runtime.BlenderEngineRuntime.ensure", return_value=Path("/runtime/python")) as provision:
            command = BlenderBakeRuntime().command(tmp_path/"engine",tmp_path/"out",1)
        provision.assert_called_once()
        assert command[0] == "/runtime/python"

    def test_failed_version_probe_does_not_install_another_engine(self, tmp_path):
        with patch("blender_bake_runtime.shutil.which", return_value="/bin/blender"), \
                patch("blender_bake_runtime.subprocess.run", side_effect=CalledProcessError(-11, [])), \
                patch("blender_bake_runtime.BlenderEngineRuntime.ensure") as provision:
            with pytest.raises(CalledProcessError):
                BlenderBakeRuntime().command(tmp_path/"engine",tmp_path/"out",1)
        provision.assert_not_called()

    def test_explicit_cli_is_left_to_full_worker_probe(self, tmp_path):
        with patch("blender_bake_runtime.subprocess.run") as version, \
                patch("blender_bake_runtime.BlenderEngineRuntime.ensure") as provision:
            command = BlenderBakeRuntime().command(tmp_path/"engine",tmp_path/"out",1, "/selected/blender")
        assert command[0] == "/selected/blender"
        version.assert_not_called()
        provision.assert_not_called()
