/** Scope: Check strip output, outward orientation and lighting control across poses. */
import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial, Vector3 } from "three";
import { ShowcaseLighting } from "../showcase/ShowcaseLighting.js";

class StripFixture {
  constructor() {
    this.root = new Group();
    this.root.scale.setScalar(0.001);
    this.mesh = new Mesh(new BoxGeometry(600, 4, 8), new MeshStandardMaterial());
    this.mesh.rotation.y = Math.PI / 2;
    this.root.add(this.mesh);
    this.root.updateMatrixWorld(true);
    this.original = this.mesh.geometry.attributes.position.array.slice();
    this.lighting = new ShowcaseLighting([{name: "shelf_light", node: this.mesh}]);
    this.root.updateMatrixWorld(true);
  }
}

test("strip output scales with CAD length and emits away from its diffuser", () => {
  const fixture = new StripFixture();
  const [light] = fixture.lighting.lights;
  assert.ok(Math.abs(light.width - 0.6) < 1e-9);
  assert.ok(Math.abs(light.height - 0.004) < 1e-9);
  assert.ok(Math.abs(light.power - 1.8) < 1e-9);
  const outward = new Vector3(0, 0, -1).transformDirection(light.matrixWorld);
  assert.ok(outward.distanceTo(new Vector3(1, 0, 0)) < 1e-9);
  assert.deepEqual(fixture.mesh.geometry.attributes.position.array, fixture.original);
});

test("off persists across poses and spill stays inside the supported interior view", () => {
  const {lighting} = new StripFixture();
  const [light] = lighting.lights;
  lighting.setPose("assembled", false);
  assert.equal(light.visible, true);
  lighting.setEnabled(false);
  assert.equal(light.visible, false);
  assert.equal(lighting.emitter.emissiveIntensity, 0);
  lighting.setPose("assembled", false);
  assert.equal(light.visible, false);
  lighting.setEnabled(true);
  assert.equal(light.visible, true);
  assert.equal(lighting.emitter.emissiveIntensity, 6);
  for (const [mode, doors] of [["exploded", false], ["assembled", true]]) {
    lighting.setPose(mode, doors);
    assert.equal(light.visible, false);
  }
});
