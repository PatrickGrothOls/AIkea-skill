/** Scope: Verify attached fittings cannot change a panel's inspection separation axis. */
import assert from "node:assert/strict";
import test from "node:test";
import { Box3, Vector3 } from "three";
import { ExplodedGroupLayout } from "./ExplodedGroupLayout.js";

class PanelLayoutFixture {
  static box(min, max) {
    return new Box3(new Vector3(...min), new Vector3(...max));
  }
}

test("tall hinged front separates forward instead of through the floor", () => {
  const panel = PanelLayoutFixture.box([0, 0, 432], [600, 2200, 450]);
  const group = {bounds:PanelLayoutFixture.box([0, 0, 410], [600, 2200, 450]),
    records:[{kind:"panel", bounds:panel}, {kind:"hardware"}]};
  const envelope = PanelLayoutFixture.box([0, 0, 0], [2400, 2200, 450]);
  const face = new ExplodedGroupLayout().nearestFace(group, envelope);
  assert.equal(face.axis, "z");
  assert.equal(face.sign, 1);
});

test("full height side retains lateral separation with hinge plates and lighting", () => {
  const panel = PanelLayoutFixture.box([0, 0, 0], [16, 2200, 432]);
  const group = {bounds:PanelLayoutFixture.box([0, 0, 0], [55, 2200, 450]),
    records:[{kind:"panel", bounds:panel}, {kind:"hardware"}, {kind:"hardware"}]};
  const envelope = PanelLayoutFixture.box([0, 0, 0], [2400, 2200, 450]);
  const face = new ExplodedGroupLayout().nearestFace(group, envelope);
  assert.equal(face.axis, "x");
  assert.equal(face.sign, -1);
});
