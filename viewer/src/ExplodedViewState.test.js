/** Scope: Keep isolated and separated poses distinct from a complete assembled review. */

import assert from "node:assert/strict";
import test from "node:test";
import { ExplodedViewState } from "./ExplodedViewState.js";

test("inspection URL clamps separation and rejects nonnumeric values", () => {
  for (const [search, expected] of [["", 0], ["?explode=.65", .65],
    ["?explode=-1", 0], ["?explode=2.5", 2.5], ["?explode=20", 3], ["?explode=oops", 0]]) {
    assert.equal(ExplodedViewState.fromSearch(search).amount, expected);
  }
});

test("picking preserves the exact inspection scope through separation changes", () => {
  const selected = new ExplodedViewState(3).withSelectedPart("vendor_mesh", "drawer__rail__clip");
  assert.equal(selected.withAmount(2).selectedScope, "drawer__rail__clip");
  const focused = selected.withScope(selected.selectedScope);
  assert.equal(focused.scope, "drawer__rail__clip");
  assert.equal(focused.selectedPart, "");
  assert.equal(focused.wholeAssembled, false);
});

test("a collapsed isolated drawer cannot become a whole-assembly approval view", () => {
  const original = new ExplodedViewState();
  const drawer = original.withScope("drawer").withAmount(0).withSelectedPart("drawer__front");
  assert.equal(original.wholeAssembled, true);
  assert.equal(drawer.wholeAssembled, false);
  assert.equal(original.selectedPart, "");
  assert.equal(drawer.selectedPart, "drawer__front");
  assert.equal(original.withAmount(.01).wholeAssembled, false);
  assert.equal(new ExplodedViewState().wholeAssembled, true);
});
