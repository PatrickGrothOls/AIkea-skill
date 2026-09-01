/** Scope: Verify the browser review client loads and saves its one decision. */

import assert from "node:assert/strict";
import test from "node:test";

import { ReviewDecisionClient } from "./ReviewDecisionClient.js";

test("missing review data keeps an ordinary visual review decision-free", async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => ({ status: 404 });
  try {
    assert.equal(await new ReviewDecisionClient().load(), null);
  } finally {
    global.fetch = originalFetch;
  }
});

test("visual approval is submitted to the bounded local endpoint", async () => {
  const originalFetch = global.fetch;
  const requests = [];
  global.fetch = async (url, options) => {
    requests.push({ url, options });
    if (url === "/review-data.json") {
      return {
        ok: true,
        json: async () => ({
          review_type: "fabrication_assembly",
          status: "proposed",
          decision_token: "session-token",
        }),
      };
    }
    return {
      ok: true,
      json: async () => ({ status: "approved" }),
    };
  };
  try {
    const client = new ReviewDecisionClient();
    const review = await client.load();
    const result = await client.submit("approved");

    assert.equal(review.decision_token, undefined);
    assert.equal(result.status, "approved");
    assert.equal(requests[1].url, "/api/review-decision");
    assert.equal(requests[1].options.method, "POST");
    assert.equal(
      requests[1].options.headers["X-AIkea-Review-Token"],
      "session-token",
    );
    assert.deepEqual(JSON.parse(requests[1].options.body), { decision: "approved" });
  } finally {
    global.fetch = originalFetch;
  }
});

test("a decision cannot be submitted before its session is loaded", async () => {
  await assert.rejects(
    new ReviewDecisionClient().submit("approved"),
    /loaded before deciding/,
  );
});
