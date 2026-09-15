/** Scope: Verify reversible door removal preserves cabinet fittings, geometry and inspection state. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";
import { ReviewAssetChoice } from "./ReviewAssetChoice.js";
import { ExplodedViewState } from "./ExplodedViewState.js";
import { ReviewInspectionPath } from "./ReviewInspectionPath.js";

class DoorFixture {
  constructor() {
    this.root = new Group();
    for (const path of [
      ["cabinet", "door_panel"], ["cabinet", "door_panel", "hinge"],
      ["cabinet", "side", "hinge_plate"], ["cabinet", "shelf"],
      ["cabinet", "drawer_01", "front"], ["cabinet", "side", "light"],
    ]) {
      const mesh = new Mesh(new BoxGeometry(10, 50, 30), new MeshStandardMaterial());
      mesh.name = path.join("__");
      mesh.userData.aikea = { inspection_path: path, kind: path.length === 2 ? "panel" : "hardware" };
      mesh.position.x = this.root.children.length * 20;
      this.root.add(mesh);
    }
    this.model = new AssemblyPresentation(this.root);
  }
}

test("hide doors and door-mounted hinges, retain plates, drawers and lights, then restore exactly", () => {
  const { model, root } = new DoorFixture();
  const original = model.records.map(({ node }) => node.matrix.toArray());
  assert.equal(model.hasDoors, true);
  assert.equal(model.apply("", 0, "panels", true).visibleCount, 4);
  assert.deepEqual(model.records.map(({ node }) => node.visible), [false, false, true, true, true, true]);
  assert.equal(model.apply("", 1, "panels", true).visibleCount, 4);
  assert.equal(model.apply("", 0, "panels", false).visibleCount, 6);
  assert.deepEqual(model.records.map(({ node }) => node.matrix.toArray()), original);
  assert.ok(root.children.every((node) => node.visible));
  assert.ok(model.records.every(({ node }, i) => node.geometry === root.children[i].geometry));
});

test("hiding an isolated door retains finite framing and can be restored", () => {
  const { model } = new DoorFixture();
  const scope = ReviewInspectionPath.key(["cabinet", "door_panel"]);
  const hidden = model.apply(scope, .65, "panels", true);
  assert.equal(hidden.visibleCount, 0);
  assert.equal(hidden.bounds.isEmpty(), false);
  assert.equal(model.apply(scope, .65, "panels", false).visibleCount, 2);
});

test("door removal chooses the inspection asset without changing explosion state", () => {
  const manifest = { assembled: { url: "/model.glb", baked: true },
    inspection: { url: "/inspection.glb", baked: false } };
  const assets = new ReviewAssetChoice(manifest);
  const state = new ExplodedViewState();
  assert.equal(assets.select(state, true), manifest.inspection);
  assert.equal(state.amount, 0);
  assert.equal(assets.select(state, false), manifest.assembled);
  assert.equal(new ReviewAssetChoice({ ...manifest, inspection: null }).select(state, true), manifest.assembled);
});
