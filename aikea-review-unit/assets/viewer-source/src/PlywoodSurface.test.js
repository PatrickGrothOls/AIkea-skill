/** Scope: Verify that plywood face and cut-edge geometry are distinguished by local normals. */

import assert from "node:assert/strict";
import test from "node:test";
import { BufferGeometry, Float32BufferAttribute } from "three";

import { isPlywoodFace } from "./PlywoodSurface.js";

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
