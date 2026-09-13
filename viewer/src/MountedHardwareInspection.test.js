/** Scope: Prove that each explosion level preserves the attachments below that level. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshBasicMaterial, Vector3 } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";
import { ReviewInspectionPath } from "./ReviewInspectionPath.js";

class MountedFurnitureFixture {
  constructor() {
    this.scene = new Group();
    this.add("wall", ["support"], [-100, 0, 0]);
    this.add("fixed runner", ["support", "runner"], [-90, 0, 0]);
    this.add("front", ["drawer_01", "front"], [0, 0, 45]);
    this.add("pull", ["drawer_01", "front", "pull"], [0, 0, 50]);
    this.add("bottom", ["drawer_01", "bottom"], [0, -20, 0]);
    this.add("moving runner", ["drawer_01", "bottom", "runner"], [-70, -22, 0]);
    this.add("clip", ["drawer_01", "bottom", "clip"], [-70, -22, 40]);
    this.add("second bottom", ["drawer_02", "bottom"], [0, 90, 0]);
    this.add("second clip", ["drawer_02", "bottom", "clip"], [-70, 88, 40]);
    this.scene.rotation.set(.2, .4, -.1);
    this.scene.scale.set(1.2, .8, 1.7);
    this.scene.updateMatrixWorld(true);
    this.model = new AssemblyPresentation(this.scene);
  }

  add(name, path, position) {
    const mesh = new Mesh(new BoxGeometry(25, 15, 10), new MeshBasicMaterial());
    mesh.name = name;
    mesh.userData.aikea = { inspection_path: path };
    mesh.position.set(...position);
    this.scene.add(mesh);
  }

  offset(name) {
    const record = this.model.records.find((part) => part.name === name);
    return record.node.getWorldPosition(new Vector3()).sub(record.worldOrigin);
  }

  assertTogether(names) {
    const expected = this.offset(names[0]);
    for (const name of names) assert.ok(this.offset(name).distanceTo(expected) < 1e-8);
  }
}

test("whole furniture keeps both runner sides with their own carrier and repeats drawers independently", () => {
  const fixture = new MountedFurnitureFixture();
  const result = fixture.model.apply("", .7);
  assert.equal(result.visibleCount, 9);
  assert.equal(result.groupCount, 3);
  fixture.assertTogether(["wall", "fixed runner"]);
  fixture.assertTogether(["front", "pull", "bottom", "moving runner", "clip"]);
  fixture.assertTogether(["second bottom", "second clip"]);
  assert.ok(fixture.offset("clip").distanceTo(fixture.offset("second clip")) > 1);
});

test("drawer inspection keeps its fittings attached to each panel", () => {
  const fixture = new MountedFurnitureFixture();
  const result = fixture.model.apply("drawer_01", .7);
  assert.equal(result.visibleCount, 5);
  assert.equal(result.groupCount, 2);
  fixture.assertTogether(["front", "pull"]);
  fixture.assertTogether(["bottom", "moving runner", "clip"]);
  assert.equal(fixture.model.scene.getObjectByName("fixed runner").visible, false);
  assert.equal(fixture.model.scene.getObjectByName("second clip").visible, false);
});

test("panel inspection includes the panel itself and can detach its fittings", () => {
  const fixture = new MountedFurnitureFixture();
  const result = fixture.model.apply("drawer_01__bottom", .7);
  assert.equal(result.visibleCount, 3);
  assert.equal(result.groupCount, 3);
  assert.equal(fixture.model.scene.getObjectByName("bottom").visible, true);
  assert.ok(fixture.offset("bottom").distanceTo(fixture.offset("clip")) > 1);
  assert.equal(fixture.model.catalog.nameFor(fixture.model.scene.getObjectByName("clip")), "clip");
  assert.ok(fixture.model.scopes.includes("support"));
  assert.ok(fixture.model.scopes.includes("drawer_01__bottom"));
});

test("reset restores exact matrices and leaves geometry and source ownership untouched", () => {
  const fixture = new MountedFurnitureFixture();
  const original = fixture.model.records.map((part) => part.node.matrix.toArray());
  const ownership = JSON.stringify(fixture.scene.children.map((part) => part.userData));
  for (const scope of ["", "drawer_01", "drawer_01__bottom", "support", "drawer_02"]) {
    fixture.model.apply(scope, .8);
  }
  const result = fixture.model.apply("", 0);
  assert.equal(result.visibleCount, 9);
  assert.deepEqual(fixture.model.records.map((part) => part.node.matrix.toArray()), original);
  assert.equal(JSON.stringify(fixture.scene.children.map((part) => part.userData)), ownership);
  fixture.model.records.forEach((part, index) => {
    assert.equal(part.node.geometry, fixture.scene.children[index].geometry);
  });
});

test("valid IDs containing double underscores cannot collide with a deeper assembly path", () => {
  const fixture = new MountedFurnitureFixture();
  fixture.scene.clear();
  fixture.add("one ID", ["cabinet__left_01", "panel"], [0, 0, 0]);
  fixture.add("nested IDs", ["cabinet", "left_01", "panel"], [100, 0, 0]);
  const model = new AssemblyPresentation(fixture.scene);
  const flat = ReviewInspectionPath.key(["cabinet__left_01"]);
  const nested = ReviewInspectionPath.key(["cabinet", "left_01"]);
  assert.notEqual(flat, nested);
  assert.ok(model.scopes.includes(flat));
  assert.ok(model.scopes.includes(nested));
  assert.equal(model.apply(flat, .7).visibleCount, 1);
  assert.equal(model.scene.getObjectByName("one ID").visible, true);
  assert.equal(model.apply(nested, .7).visibleCount, 1);
  assert.equal(model.scene.getObjectByName("nested IDs").visible, true);
  assert.equal(ReviewInspectionPath.label(flat), "cabinet  left 01");
});
