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

test("door approval is submitted to the bounded local endpoint", async () => {
  const originalFetch = global.fetch;
  let request;
  global.fetch = async (url, options) => {
    request = { url, options };
    return {
      ok: true,
      json: async () => ({ status: "approved" }),
    };
  };
  try {
    const result = await new ReviewDecisionClient().submit("approved");

    assert.equal(result.status, "approved");
    assert.equal(request.url, "/api/review-decision");
    assert.equal(request.options.method, "POST");
    assert.deepEqual(JSON.parse(request.options.body), { decision: "approved" });
  } finally {
    global.fetch = originalFetch;
  }
});
