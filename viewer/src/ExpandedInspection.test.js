/** Scope: Verify extra spacing for aligned units and individual physical-part focus. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshBasicMaterial, Vector3 } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";
import { ReviewInspectionPath } from "./ReviewInspectionPath.js";

class StackedDrawers {
  constructor() {
    this.scene = new Group();
    this.add("case", [800, 800, 10], [0, 0, -100], ["case"]);
    for (const [name, y] of [["lower", -100], ["upper", 100]]) {
      this.add(`${name} panel`, [100, 60, 100], [0, y, 0], [name, "panel"]);
      this.add(`${name} fitting`, [100, 60, 10], [0, y, 55], [name, "panel", "fitting"]);
    }
    this.model = new AssemblyPresentation(this.scene);
  }

  add(name, size, position, path) {
    const mesh = new Mesh(new BoxGeometry(...size), new MeshBasicMaterial());
    mesh.name = name;
    mesh.position.set(...position);
    mesh.userData.aikea = { inspection_path: path };
    this.scene.add(mesh);
  }

  offset(name) {
    const record = this.model.records.find((part) => part.name === name);
    return record.node.getWorldPosition(new Vector3()).sub(record.worldOrigin);
  }
}

test("extra separation spreads aligned drawers while their fittings stay attached", () => {
  const fixture = new StackedDrawers();
  fixture.model.apply("", 1);
  assert.deepEqual(fixture.offset("lower panel"), fixture.offset("upper panel"));
  fixture.model.apply("", 3);
  const lower = fixture.model.scene.getObjectByName("lower panel");
  const upper = fixture.model.scene.getObjectByName("upper panel");
  assert.ok(upper.position.y - lower.position.y > 200);
  for (const name of ["lower", "upper"]) {
    assert.deepEqual(fixture.offset(`${name} panel`), fixture.offset(`${name} fitting`));
  }
  fixture.model.apply("", 0);
  assert.deepEqual(fixture.offset("lower panel").toArray(), [0, 0, 0]);
});

test("every physical piece can be focused through its explicit identity", () => {
  const fixture = new StackedDrawers();
  for (const record of fixture.model.records) {
    const scope = fixture.model.scopeForPart(record.name);
    assert.ok(fixture.model.scopes.includes(scope));
    fixture.model.apply(scope, 0);
    assert.equal(record.node.visible, true);
  }
  assert.equal(fixture.model.apply(fixture.model.scopeForPart("lower panel"), 0).visibleCount, 2);
  assert.equal(fixture.model.apply(fixture.model.scopeForPart("lower fitting"), 3).visibleCount, 1);
  assert.equal(fixture.model.apply("", 0).visibleCount, 5);
});

test("leading and trailing underscores cannot turn a selectable leaf into an empty scope", () => {
  const fixture = new StackedDrawers();
  fixture.scene.clear();
  for (const [index, path] of [
    ["drawer_01", "rail_", "clip"], ["drawer_01", "rail", "_clip"],
    ["drawer_01", "rail___", "_clip_"], ["drawer_01", "rail%5F", "clip"],
  ].entries()) {
    fixture.add(`part ${index}`, [10, 10, 10], [index * 50, 0, 0], path);
    assert.deepEqual(ReviewInspectionPath.segments(ReviewInspectionPath.key(path)), path);
  }
  const model = new AssemblyPresentation(fixture.scene);
  for (const record of model.records) {
    assert.equal(model.apply(model.scopeForPart(record.name), 0).visibleCount, 1);
    assert.equal(record.node.visible, true);
  }
});
