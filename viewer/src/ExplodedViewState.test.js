/** Scope: Keep isolated and separated poses distinct from a complete assembled review. */

import assert from "node:assert/strict";
import test from "node:test";
import { ExplodedViewState } from "./ExplodedViewState.js";

test("inspection URL clamps separation and rejects nonnumeric values", () => {
  for (const [search, expected] of [["", 0], ["?explode=.65", .65],
    ["?explode=-1", 0], ["?explode=20", 1], ["?explode=oops", 0]]) {
    assert.equal(ExplodedViewState.fromSearch(search).amount, expected);
  }
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
