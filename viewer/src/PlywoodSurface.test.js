/** Scope: Verify that plywood face and cut-edge geometry are distinguished by local normals. */

import assert from "node:assert/strict";
import test from "node:test";
import {
  BoxGeometry,
  BufferGeometry,
  Float32BufferAttribute,
  Mesh,
  MeshStandardMaterial,
  Texture,
} from "three";

import { isPlywoodFace, PlywoodSurface } from "./PlywoodSurface.js";

function geometryWithNormals(normals) {
  const geometry = new BufferGeometry();
  geometry.setAttribute("normal", new Float32BufferAttribute(normals, 3));
  return geometry;
}

test("recognizes a broad plywood face from its local normal", () => {
  const geometry = geometryWithNormals([0, 0, 1, 0, 0, 1, 0, 0, 1]);

  assert.equal(isPlywoodFace(geometry), true);
});

test("recognizes a plywood cut edge from its local normal", () => {
  const geometry = geometryWithNormals([1, 0, 0, 1, 0, 0, 1, 0, 0]);

  assert.equal(isPlywoodFace(geometry), false);
});

test("preserves the source material for a review-only guide mesh", () => {
  const sourceMaterial = new MeshStandardMaterial({
    color: "#3a8ab8",
    opacity: 0.45,
    transparent: true,
  });
  const mesh = new Mesh(new BoxGeometry(1, 1, 1), sourceMaterial);
  mesh.name = "review_only__runner_left__760h5000s_mounting_zone_part";
  const surface = new PlywoodSurface(
    new Texture(),
    new Texture(),
    new Texture(),
    1,
  );

  surface.applyTo(mesh);

  assert.equal(mesh.material, sourceMaterial);
  assert.equal(mesh.material.opacity, 0.45);
});

test("preserves the manufacturer material for source CAD hardware", () => {
  const sourceMaterial = new MeshStandardMaterial({
    color: "#363a3e",
    metalness: 0.8,
    roughness: 0.35,
  });
  const mesh = new Mesh(new BoxGeometry(1, 1, 1), sourceMaterial);
  mesh.name = "runner_left__source_cad_part";
  const surface = new PlywoodSurface(
    new Texture(),
    new Texture(),
    new Texture(),
    1,
  );

  surface.applyTo(mesh);

  assert.equal(mesh.material, sourceMaterial);
  assert.equal(mesh.material.metalness, 0.8);
});
