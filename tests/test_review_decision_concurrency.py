"""Scope: Verify review decisions serialize across independent processes."""

from __future__ import annotations

import json
from multiprocessing import get_context
from pathlib import Path

from review_decision_store import ReviewDecisionConflict, ReviewDecisionStore


class PausingReviewDecisionStore(ReviewDecisionStore):
    """Pause the first decision while it holds the transition lock."""

    def __init__(self, path: Path, before_write, release_write) -> None:
        super().__init__(path)
        self.before_write = before_write
        self.release_write = release_write

    def _write_atomically(self, record: dict) -> None:
        self.before_write.set()
        if not self.release_write.wait(timeout=5):
            raise TimeoutError("timed out waiting to finish the first decision")
        super()._write_atomically(record)


class DecisionProcess:
    """Run one decision attempt in a spawn-safe subprocess."""

    @staticmethod
    def pause_before_write(path, before_write, release_write, results) -> None:
        store = PausingReviewDecisionStore(path, before_write, release_write)
        DecisionProcess._record_result(store, "approved", results)

    @staticmethod
    def decide(path, started, results) -> None:
        started.set()
        DecisionProcess._record_result(
            ReviewDecisionStore(path),
            "change_requested",
            results,
        )

    @staticmethod
    def _record_result(store, decision, results) -> None:
        try:
            store.decide(decision)
        except ReviewDecisionConflict:
            results.put(("conflict", decision))
        else:
            results.put(("success", decision))


class TestReviewDecisionConcurrency:
    """Protect the one-way transition across separate store processes."""

    def test_conflicting_processes_cannot_both_decide(self, tmp_path) -> None:
        review = tmp_path / "reviews/door-openings.json"
        review.parent.mkdir()
        review.write_text(
            json.dumps(
                {
                    "review_type": "door_openings",
                    "status": "proposed",
                    "message": "Review the door.",
                    "doors": [],
                }
            ),
            encoding="utf-8",
        )
        context = get_context("spawn")
        before_write = context.Event()
        release_write = context.Event()
        second_started = context.Event()
        results = context.Queue()
        first = context.Process(
            target=DecisionProcess.pause_before_write,
            args=(review, before_write, release_write, results),
        )
        second = context.Process(
            target=DecisionProcess.decide,
            args=(review, second_started, results),
        )

        first.start()
        assert before_write.wait(timeout=5)
        second.start()
        assert second_started.wait(timeout=5)
        try:
            second.join(timeout=0.5)
            assert second.is_alive(), "second decision bypassed the process lock"
        finally:
            release_write.set()
            first.join(timeout=5)
            second.join(timeout=5)

        assert (first.exitcode, second.exitcode) == (0, 0)
        assert {results.get(timeout=2), results.get(timeout=2)} == {
            ("success", "approved"),
            ("conflict", "change_requested"),
        }
        assert json.loads(review.read_text(encoding="utf-8"))["status"] == "approved"


__all__ = ["TestReviewDecisionConcurrency"]
