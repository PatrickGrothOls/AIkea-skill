"""Scope: Verify automatic discovery of an existing CadQuery Python runtime."""

from pathlib import Path

import pytest

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError


class StubCadQueryRuntime(CadQueryRuntime):
    """Replace interpreter execution with a fixed set of supported paths."""

    def __init__(
        self,
        current_python: Path,
        environment_roots: tuple[Path, ...],
        override: Path | None,
        supported: set[Path],
    ) -> None:
        super().__init__(current_python, environment_roots, override)
        self.supported = {path.resolve() for path in supported}

    def _supports_cadquery(self, interpreter: Path) -> bool:
        return interpreter.resolve() in self.supported


class TestCadQueryRuntime:
    """Keep runtime selection automatic while retaining one explicit override."""

    def test_uses_explicit_override_first(self, tmp_path: Path) -> None:
        current = self._python(tmp_path / "current" / "bin" / "python")
        override = self._python(tmp_path / "chosen" / "bin" / "python")
        runtime = StubCadQueryRuntime(current, (), override, {override})

        assert runtime.resolve() == override.resolve()

    def test_keeps_a_ready_current_interpreter(self, tmp_path: Path) -> None:
        current = self._python(tmp_path / "conda" / "bin" / "python")
        alternative = self._python(
            tmp_path / "conda" / "envs" / "alternative" / "bin" / "python"
        )
        runtime = StubCadQueryRuntime(
            current,
            (tmp_path / "conda",),
            None,
            {current, alternative},
        )

        assert runtime.resolve() == current.resolve()

    def test_finds_cadquery_in_a_conda_environment(self, tmp_path: Path) -> None:
        current = self._python(tmp_path / "conda" / "bin" / "python")
        cadquery = self._python(tmp_path / "conda" / "envs" / "cad" / "bin" / "python")
        runtime = StubCadQueryRuntime(current, (tmp_path / "conda",), None, {cadquery})

        assert runtime.resolve() == cadquery.resolve()

    def test_rejects_environments_without_cadquery(self, tmp_path: Path) -> None:
        current = self._python(tmp_path / "current" / "bin" / "python")
        runtime = StubCadQueryRuntime(current, (), None, set())

        with pytest.raises(CadQueryRuntimeError, match="No CadQuery Python runtime"):
            runtime.resolve()

    def _python(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path
