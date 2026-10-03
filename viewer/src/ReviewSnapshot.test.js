/** Scope: Verify quote captures scale large displays without changing the source renderer. */

import assert from "node:assert/strict";
import test from "node:test";
import { ReviewSnapshot } from "./ReviewSnapshot.js";

class SnapshotFixture {
  constructor(width, height, encoded = "data:image/png;base64,aGVsbG8=") {
    this.draws = [];
    this.preview = { getContext: () => ({ drawImage: (...args) => this.draws.push(args) }),
      toDataURL: (type) => { assert.equal(type, "image/png"); return encoded; } };
    this.source = { width, height, ownerDocument: { createElement: () => this.preview } };
    this.events = [];
    const gl = { domElement: this.source, render: () => this.events.push("render") };
    this.snapshot = new ReviewSnapshot({ get: () => ({ gl, scene: {}, camera: {} }) });
  }
}

// Node test registration uses callbacks; the fixture owns capture state and observations.
for (const [width, height] of [[3840, 2100], [7680, 4320], [2160, 3840], [8000, 500]]) {
  test(`bounds a ${width} by ${height} high-DPI preview before submission`, () => {
    const f = new SnapshotFixture(width, height);
    assert.ok(f.snapshot.capture());
    assert.ok(f.preview.width <= 1600 && f.preview.height <= 1600);
    assert.ok(f.preview.width * f.preview.height <= 800000);
    assert.ok(Math.abs(f.preview.width / f.preview.height - width / height) < 0.03);
    assert.deepEqual([f.source.width, f.source.height], [width, height]);
    assert.deepEqual(f.events, ["render"]);
    assert.deepEqual(f.draws[0], [f.source, 0, 0, f.preview.width, f.preview.height]);
  });
}

test("small previews retain their dimensions and oversized encodings cannot be submitted", () => {
  const f = new SnapshotFixture(600, 400);
  assert.ok(f.snapshot.capture());
  assert.deepEqual([f.preview.width, f.preview.height], [600, 400]);
  const oversized = new SnapshotFixture(600, 400, "data:image/png;base64," + "A".repeat(5333336));
  assert.equal(oversized.snapshot.capture(), null);
});
