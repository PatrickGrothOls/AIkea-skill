/** Scope: Verify batched input uses one rendering path without an idle loop. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { ShowcaseRenderQueue } from "../showcase/ShowcaseRenderQueue.js";

class RenderQueueVerification {
  verify() {
    const frames = [];
    const drawnStates = [];
    let cameraState = "initial";
    const queue = new ShowcaseRenderQueue(() => drawnStates.push(cameraState), callback => frames.push(callback));
    for (let i = 0; i < 30; i++) {
      cameraState = `rotation-${i}`;
      queue.request();
    }
    assert.equal(frames.length, 1, "A burst of pointer events schedules only one frame");
    frames.shift()();
    assert.deepEqual(drawnStates, ["rotation-29"], "The render uses the latest camera pose");
    assert.equal(frames.length, 0, "No idle loop follows the last pointer event");
    cameraState = "zoomed";
    queue.request();
    frames.shift()();
    assert.deepEqual(drawnStates, ["rotation-29", "zoomed"], "Later gestures use the same draw callback");
  }
}

// node:test requires a callback; the fixture owns the render scheduling verification.
test("showcase batches input into consistent renders of the latest camera state", () => {
  new RenderQueueVerification().verify();
});
