/** Scope: Prove inspection grouping, isolation and exact reset without changing source geometry. */

import assert from "node:assert/strict";
import test from "node:test";
import { Box3, BoxGeometry, Group, Mesh, MeshBasicMaterial, Vector3 } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";

class FurnitureFixture {
  constructor() {
    this.scene = new Group();
    this.add("side", [10, 100, 80], [-100, 0, 0]);
    this.add("drawer__front", [100, 50, 10], [0, 0, 0]);
    this.add("drawer__visible_front", [100, 50, 10], [0, 0, 15]);
    this.add("drawer__back", [100, 50, 10], [0, 0, -70]);
    this.add("drawer__tray__bottom", [80, 5, 60], [0, -15, -35]);
    this.scene.updateMatrixWorld(true);
  }

  add(name, size, position) {
    const mesh = new Mesh(new BoxGeometry(...size), new MeshBasicMaterial());
    mesh.name = name;
    mesh.position.set(...position);
    this.scene.add(mesh);
    return mesh;
  }

  positions(scene = this.scene) {
    return scene.children.map((mesh) => mesh.position.toArray());
  }
}

test("whole assembly separates child units without changing their internal placement", () => {
  const fixture = new FurnitureFixture();
  const model = new AssemblyPresentation(fixture.scene);
  const result = model.apply("", 1);
  assert.equal(result.groupCount, 2);
  assert.equal(result.visibleCount, 5);
  assert.deepEqual(model.scopes, ["drawer", "drawer__tray"]);
  const offsets = model.records.filter((record) => record.name.startsWith("drawer__"))
    .map((record) => record.node.position.clone().sub(record.position).toArray());
  assert.deepEqual(offsets, offsets.map(() => offsets[0]));
  assert.ok(new Vector3(...offsets[0]).length() > 0);
  assert.deepEqual(fixture.positions(), new FurnitureFixture().positions());
});

test("drawer focus hides the carcass and opens gaps between aligned front layers", () => {
  const model = new AssemblyPresentation(new FurnitureFixture().scene);
  const result = model.apply("drawer", 1);
  assert.equal(result.visibleCount, 4);
  assert.equal(model.scene.getObjectByName("side").visible, false);
  const front = model.scene.getObjectByName("drawer__front");
  const visible = model.scene.getObjectByName("drawer__visible_front");
  assert.ok(visible.position.z - front.position.z > 15);
  assert.ok(model.scene.getObjectByName("drawer__back").position.z < -70);
  assert.equal(model.apply("drawer__tray", 0).visibleCount, 1);
});

test("repeated inspection restores exact local transforms and leaves source vertices untouched", () => {
  const fixture = new FurnitureFixture();
  fixture.scene.rotation.set(0.2, 0.6, -0.1);
  fixture.scene.scale.set(1.2, 0.8, 2);
  fixture.scene.position.set(47, 83, -23);
  fixture.scene.updateMatrixWorld(true);
  const model = new AssemblyPresentation(fixture.scene);
  const original = model.records.map((record) => ({
    matrix: record.node.matrix.toArray(),
    vertices: [...record.node.geometry.attributes.position.array],
  }));
  for (const amount of [0.4, 1, 0.2, 0.9]) {
    const expected = model.apply("drawer", amount).bounds;
    const active = model.records.filter((record) => record.node.visible);
    const actual = active.reduce((bounds, record) => bounds.expandByObject(record.node),
      new Box3());
    assert.ok(actual.min.distanceTo(expected.min) < 1e-8);
    assert.ok(actual.max.distanceTo(expected.max) < 1e-8);
  }
  model.apply("", 0);
  model.records.forEach((record, index) => {
    assert.deepEqual(record.node.matrix.toArray(), original[index].matrix);
    assert.deepEqual([...record.node.geometry.attributes.position.array], original[index].vertices);
  });
  assert.deepEqual(fixture.positions(), new FurnitureFixture().positions());
});

test("hidden ancestors remain hidden and are excluded from inspection bounds", () => {
  const fixture = new FurnitureFixture();
  const hidden = new Group();
  hidden.visible = false;
  const mesh = new Mesh(new BoxGeometry(5000, 5000, 5000), new MeshBasicMaterial());
  mesh.name = "hidden__piece";
  hidden.add(mesh);
  fixture.scene.add(hidden);
  const model = new AssemblyPresentation(fixture.scene);
  assert.equal(model.apply("", 1).visibleCount, 5);
  model.apply("", 0);
  assert.equal(model.scene.getObjectByName("hidden__piece").visible, true);
  assert.equal(model.scene.getObjectByName("hidden__piece").parent.visible, false);
});

test("unnamed flat imports retain separate selectable pieces", () => {
  const fixture = new FurnitureFixture();
  fixture.scene.children.forEach((mesh) => { mesh.name = ""; });
  const model = new AssemblyPresentation(fixture.scene);
  assert.equal(model.apply("", 0.6).groupCount, 5);
  assert.deepEqual(model.scopes, []);
  assert.equal(new Set(model.records.map((record) => record.name)).size, 5);
});
