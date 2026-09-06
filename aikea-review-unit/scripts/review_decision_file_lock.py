"""Scope: Serialize review-record transitions through one stable sidecar lock."""

from __future__ import annotations

import fcntl
from pathlib import Path
from types import TracebackType


class ReviewDecisionFileLock:
    """Hold an exclusive process-wide lock for one review record."""

    def __init__(self, review_path: Path) -> None:
        self.path = review_path.with_name(f".{review_path.name}.lock")
        self._file = None

    def __enter__(self) -> ReviewDecisionFileLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("a+b")
        fcntl.flock(self._file.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(
        self,
        _error_type: type[BaseException] | None,
        _error: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        if self._file is not None:
            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
            self._file.close()
            self._file = None


__all__ = ["ReviewDecisionFileLock"]
