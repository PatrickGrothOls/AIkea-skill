/** Scope: Verify whole-cabinet panel inspection retains mounted fittings and moving illumination. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial, PlaneGeometry, Vector3 } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";
import { ExplodedViewState } from "./ExplodedViewState.js";
import { LightingSource } from "./LightingSource.js";
import { ReviewInspectionPath } from "./ReviewInspectionPath.js";

class CabinetFixture {
  constructor() {
    const root = new Group();
    for (const [cabinet, x] of [["left", -200], ["right", 200]]) {
      this.add(root, `${cabinet} side`, [cabinet, "side"], [x, 0, 0], "panel");
      this.add(root, `${cabinet} shelf`, [cabinet, "shelf"], [x+80, 0, 0], "panel");
      this.add(root, `${cabinet} front`, [cabinet, "front"], [x+80, 0, 150], "panel");
      this.add(root, `${cabinet} hinge`, [cabinet, "side", "hinge"], [x+5, 20, 0], "hardware");
      const emitter = this.add(root, `${cabinet}__light_source__strip`,
        [cabinet, "side", "strip"], [x+5, 0, 0], "hardware", new PlaneGeometry(4, 100));
      emitter.rotation.y = Math.PI/2;
    }
    root.rotation.set(.2, .3, -.1);
    root.position.set(14, 23, 51);
    this.model = new AssemblyPresentation(root);
  }

  add(root, name, path, position, kind, geometry = new BoxGeometry(12, 140, 100)) {
    const mesh = new Mesh(geometry, new MeshStandardMaterial({ color: "#ffe1b0" }));
    mesh.name = name;
    mesh.position.set(...position);
    mesh.userData.aikea = { kind, inspection_path: path };
    root.add(mesh);
    return mesh;
  }

  offset(name) {
    const record = this.model.records.find((part) => part.name === name);
    return record.node.getWorldPosition(new Vector3()).sub(record.worldOrigin);
  }
}

test("all-panel separation opens every cabinet and preserves each panel's mounted fittings", () => {
  const fixture = new CabinetFixture();
  const result = fixture.model.apply("", 1, "panels");
  assert.equal(result.visibleCount, 10);
  assert.equal(result.groupCount, 6);
  for (const cabinet of ["left", "right"]) {
    const side = fixture.offset(`${cabinet} side`);
    assert.ok(side.distanceTo(fixture.offset(`${cabinet} front`)) > 1);
    assert.ok(side.distanceTo(fixture.offset(`${cabinet} shelf`)) > 1);
    assert.ok(side.distanceTo(fixture.offset(`${cabinet} hinge`)) < 1e-8);
    assert.ok(side.distanceTo(fixture.offset(`${cabinet}__light_source__strip`)) < 1e-8);
  }
});

test("exploded light sources follow actual panel transforms and exclude isolated-away cabinets", () => {
  const fixture = new CabinetFixture();
  const before = LightingSource.collect(fixture.model.scene);
  fixture.model.apply("", .8, "panels");
  const after = LightingSource.collect(fixture.model.scene);
  assert.equal(after.length, 2);
  for (const source of after) {
    const original = before.find((item) => item.name === source.name);
    const movement = new Vector3(...source.position).sub(new Vector3(...original.position));
    assert.ok(movement.distanceTo(fixture.offset(source.name)) < 1e-8);
    assert.ok(Number.isFinite(source.intensity) && source.intensity > 0);
    assert.equal(source.intensity, original.intensity);
  }
  fixture.model.apply(ReviewInspectionPath.key(["left"]), .8, "panels");
  assert.equal(LightingSource.collect(fixture.model.scene).length, 1);
});

test("all-panel inspection resets exactly and still permits deeper fitting inspection", () => {
  const fixture = new CabinetFixture();
  const original = fixture.model.records.map((record) => record.node.matrix.toArray());
  fixture.model.apply("", 3, "panels");
  const focused = fixture.model.apply(ReviewInspectionPath.key(["left", "side"]), .5, "panels");
  assert.equal(focused.groupCount, 3);
  fixture.model.apply("", 0, "panels");
  assert.deepEqual(fixture.model.records.map((record) => record.node.matrix.toArray()), original);
});

test("inspection controls default to opening panels and preserve the explicit grouping choice", () => {
  const state = ExplodedViewState.fromSearch("?explode=1");
  assert.equal(state.detail, "panels");
  const grouped = state.withDetail("assemblies").withAmount(2).withScope("left").withSelectedPart("side");
  assert.equal(grouped.detail, "assemblies");
});
