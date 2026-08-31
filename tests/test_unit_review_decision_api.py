"""Scope: Verify the loopback viewer can persist its door-opening decision."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.request import Request, urlopen

from unit_review_server import UnitReviewServer


class TestUnitReviewDecisionApi(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name)
        viewer = root / "viewer"
        viewer.mkdir()
        (viewer / "index.html").write_text("review", encoding="utf-8")
        model = root / "model.glb"
        model.write_bytes(b"glb")
        self.review = root / "door-openings.json"
        self.review.write_text(
            json.dumps(
                {
                    "review_type": "door_openings",
                    "status": "proposed",
                    "doors": [],
                }
            ),
            encoding="utf-8",
        )
        self.server = UnitReviewServer(viewer, model, 0, self.review)
        self.addCleanup(self.server.close)

    def test_approval_post_updates_the_project_review_record(self) -> None:
        request_thread = Thread(target=self.server.httpd.handle_request)
        request_thread.start()
        request = Request(
            f"{self.server.url}api/review-decision",
            data=json.dumps({"decision": "approved"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=2) as response:
            result = json.loads(response.read())

        request_thread.join(timeout=2)
        self.assertFalse(request_thread.is_alive())
        self.assertEqual(result["status"], "approved")
        saved = json.loads(self.review.read_text(encoding="utf-8"))
        self.assertEqual(saved["status"], "approved")


if __name__ == "__main__":
    unittest.main()
