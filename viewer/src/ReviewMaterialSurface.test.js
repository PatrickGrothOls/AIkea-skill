/** Scope: Ensure the display respects supplied finishes, UVs, geometry, and untextured HDF. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Mesh, MeshStandardMaterial, Texture } from "three";
import { ReviewMaterialSurface } from "./ReviewMaterialSurface.js";

class FallbackProbe {
  constructor() { this.meshes = []; }
  applyTo(mesh) { this.meshes.push(mesh); }
}

test("authored wood keeps its maps, finish values, normals, UVs, and positions", () => {
  const fallback = new FallbackProbe();
  const material = new MeshStandardMaterial({ map: new Texture(), roughness: .8 });
  const mesh = new Mesh(new BoxGeometry(400, 180, 16), material);
  const original = Object.fromEntries(Object.entries(mesh.geometry.attributes)
    .map(([key, attribute]) => [key, attribute.array.slice()]));
  new ReviewMaterialSurface(fallback, 16).applyTo(mesh);
  assert.equal(mesh.material, material);
  assert.equal(material.roughness, .8);
  assert.equal(material.map.anisotropy, 8);
  assert.equal(fallback.meshes.length, 0);
  for (const [key, buffer] of Object.entries(original)) {
    assert.deepEqual(mesh.geometry.attributes[key].array, buffer);
  }
});

test("declared untextured HDF is never replaced by a wood-grain material", () => {
  const fallback = new FallbackProbe();
  const material = new MeshStandardMaterial({ color: "#91765b", roughness: .88 });
  material.userData.aikea = { material_id: "SELECTED_6mm_HDF" };
  const mesh = new Mesh(new BoxGeometry(400, 500, 6), material);
  new ReviewMaterialSurface(fallback, 4).applyTo(mesh);
  assert.equal(mesh.material, material);
  assert.equal(material.map, null);
  assert.equal(fallback.meshes.length, 0);
});

test("old undeclared GLBs retain the existing fallback", () => {
  const fallback = new FallbackProbe();
  const mesh = new Mesh(new BoxGeometry(), new MeshStandardMaterial());
  new ReviewMaterialSurface(fallback, 4).applyTo(mesh);
  assert.deepEqual(fallback.meshes, [mesh]);
});
