"""Scope: Verify loopback decisions require a loaded same-origin session."""

from __future__ import annotations

import json

from review_server_test_support import ReviewServerTestSupport


class TestUnitReviewDecisionApi:
    """Protect token, origin, media type, and one-decision semantics."""

    def test_approval_post_updates_the_project_review_record(self, tmp_path) -> None:
        support, server, review = self._door_server(tmp_path)
        try:
            token = self._token(support, server)

            status, content = support.request(
                server,
                "api/review-decision",
                "POST",
                {"decision": "approved"},
                self._headers(server, token),
            )
        finally:
            server.close()

        assert status == 200
        assert json.loads(content)["status"] == "approved"
        assert json.loads(review.read_text(encoding="utf-8"))["status"] == "approved"

    def test_rejects_missing_token_origin_or_json_type(self, tmp_path) -> None:
        support, server, review = self._door_server(tmp_path)
        try:
            token = self._token(support, server)
            cases = (
                ({"Content-Type": "application/json", "Origin": server.url[:-1]}, 403),
                (
                    {
                        "Content-Type": "application/json",
                        "X-AIkea-Review-Token": token,
                    },
                    403,
                ),
                (
                    {
                        "Content-Type": "text/plain",
                        "Origin": server.url[:-1],
                        "X-AIkea-Review-Token": token,
                    },
                    415,
                ),
            )
            statuses = tuple(
                support.request(
                    server,
                    "api/review-decision",
                    "POST",
                    {"decision": "approved"},
                    headers,
                )[0]
                for headers, _expected in cases
            )
        finally:
            server.close()

        assert statuses == tuple(expected for _headers, expected in cases)
        assert json.loads(review.read_text(encoding="utf-8"))["status"] == "proposed"

    def test_a_second_post_cannot_replace_the_first_decision(self, tmp_path) -> None:
        support, server, review = self._door_server(tmp_path)
        try:
            token = self._token(support, server)
            headers = self._headers(server, token)
            first = support.request(
                server,
                "api/review-decision",
                "POST",
                {"decision": "approved"},
                headers,
            )[0]
            second = support.request(
                server,
                "api/review-decision",
                "POST",
                {"decision": "change_requested"},
                headers,
            )[0]
        finally:
            server.close()

        assert (first, second) == (200, 409)
        assert json.loads(review.read_text(encoding="utf-8"))["status"] == "approved"

    def _door_server(self, root):
        support = ReviewServerTestSupport(root)
        model = support.write_model()
        review = support.write_json(
            "reviews/door-openings.json",
            {
                "review_type": "door_openings",
                "status": "proposed",
                "message": "Review the door.",
                "doors": [],
            },
        )
        return support, support.start(model, review), review

    def _token(self, support, server):
        status, content = support.request(server, "review-data.json")
        assert status == 200
        return json.loads(content)["decision_token"]

    def _headers(self, server, token):
        return {
            "Content-Type": "application/json",
            "Origin": server.url[:-1],
            "X-AIkea-Review-Token": token,
        }


__all__ = ["TestUnitReviewDecisionApi"]
