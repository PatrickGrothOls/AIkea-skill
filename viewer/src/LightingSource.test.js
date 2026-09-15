/** Scope: Verify nested exported emitter identity, placement and material ownership. */
import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial, PlaneGeometry, Texture } from "three";
import { LightingSource } from "./LightingSource.js";
import { LightingSurface } from "./LightingSurface.js";
import { PlywoodSurface } from "./PlywoodSurface.js";
import { ReviewMeshName } from "./ReviewMeshName.js";

class LightingFixture {
  static mesh(name) {
    const mesh = new Mesh(new PlaneGeometry(600, 4), new MeshStandardMaterial({color: "#ffbd77"}));
    mesh.name = name;
    return mesh;
  }
}

test("retains two identical run IDs in different parent assemblies", () => {
  const root = new Group();
  const first = LightingFixture.mesh("left_01__light_source__apex__run_01__3200k_part_0");
  const duplicate = LightingFixture.mesh("left_01__light_source__apex__run_01__3200k_part_1");
  const second = LightingFixture.mesh("right_01__light_source__apex__run_01__3200k_part_0");
  second.position.set(100, 200, 300);
  second.rotation.y = Math.PI / 2;
  root.add(first, duplicate, second);
  root.updateMatrixWorld(true);
  const sources = LightingSource.collect(root);
  assert.equal(sources.length, 2);
  assert.deepEqual(sources[0].position, [0, 0, 0.5]);
  assert.ok(Math.abs(sources[1].position[0] - 100.5) < 1e-6);
  assert.equal(sources[1].position[2], 300);
  assert.equal(sources[1].width, 600);
  assert.equal(sources[1].height, 4);
});

test("keeps nested purchased lights out of plywood materials and lights emitters", () => {
  const plywood = new PlywoodSurface(new Texture(), new Texture(), new Texture(), 1);
  for (const role of ["purchased_light__", "light_source__", "review_only__"]) {
    const mesh = LightingFixture.mesh(`owner_01__${role}fixture`);
    const source = mesh.material;
    plywood.applyTo(mesh);
    assert.equal(mesh.material, source);
    if (role === "light_source__") {
      new LightingSurface(true).applyTo(mesh);
      assert.equal(mesh.material.emissiveIntensity, 1.5);
      assert.equal(source.emissiveIntensity, 1);
    }
  }
  assert.equal(ReviewMeshName.hasRole("mylight_source__panel", "light_source__"), false);
});

test("counts the six GLTF primitive meshes of an emitter as one source", () => {
  const root = new Group();
  for (const owner of ["left_01", "right_01"]) {
    const group = new Group();
    group.name = `${owner}__light_source__apex__run_01__3200k`;
    const top = LightingFixture.mesh(`${group.name}_5`);
    const bottom = LightingFixture.mesh(`${group.name}_6`);
    bottom.geometry.translate(0, 0, -0.2);
    group.add(top, bottom);
    root.add(group);
  }
  root.updateMatrixWorld(true);
  const sources = LightingSource.collect(root);
  assert.equal(sources.length, 2);
  assert.equal(sources[0].name, "left_01__light_source__apex__run_01__3200k");
  assert.equal(sources[0].position[2], 0.5);
});

test("consolidated emitter solid keeps the same outward face and follows its host", () => {
  const root = new Group();
  const mesh = LightingFixture.mesh("right_side__light_source__run_01");
  mesh.geometry = new BoxGeometry(600, 4, 0.2);
  mesh.geometry.translate(0, 0, -0.1);
  root.add(mesh);
  root.position.set(25, 30, 100);
  root.rotation.y = Math.PI / 2;
  root.updateMatrixWorld(true);
  const [source] = LightingSource.collect(root);
  assert.equal(source.width, 600);
  assert.equal(source.height, 4);
  assert.ok(Math.abs(source.position[0] - 25.5) < 1e-6);
  assert.equal(source.position[1], 30);
  assert.equal(source.position[2], 100);
});
