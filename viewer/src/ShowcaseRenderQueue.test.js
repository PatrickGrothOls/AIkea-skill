/** Scope: Verify bounded drag rendering and restoration of the full resting view. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { ShowcaseRenderQueue } from "../showcase/ShowcaseRenderQueue.js";

class RenderQueueVerification {
  verify() {
    const frames = [];
    const draws = [];
    const queue = new ShowcaseRenderQueue(moving => draws.push(moving), callback => frames.push(callback));
    queue.setInteracting(true);
    for (let i = 0; i < 30; i++) queue.request();
    assert.equal(frames.length, 1, "A burst of pointer events schedules only one frame");
    frames.shift()();
    assert.deepEqual(draws, [true], "Movement uses the lightweight scene pass");
    queue.request();
    queue.setInteracting(false);
    assert.equal(frames.length, 1);
    frames.shift()();
    assert.deepEqual(draws, [true, false], "Release restores full effects even with a pending drag frame");
    assert.equal(frames.length, 0, "No permanent render loop remains after release");
    queue.setInteracting(true);
    queue.setInteracting(false);
    frames.shift()();
    assert.deepEqual(draws, [true, false, false], "A wheel gesture ending within one frame renders its final state");
  }
}

// node:test requires a callback; the fixture owns the interaction lifecycle verification.
test("showcase batches drag updates and restores the full render on release", () => {
  new RenderQueueVerification().verify();
});
