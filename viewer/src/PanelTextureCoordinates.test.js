/** Scope: Check grain orientation, reproducibility, and preservation of CAD vertices. */

import assert from "node:assert/strict";
import test from "node:test";
import { PlaneGeometry } from "three";
import { PanelTextureCoordinates } from "./PanelTextureCoordinates.js";

test("wide drawer fronts carry grain horizontally without changing their geometry", () => {
  const face = new PlaneGeometry(800, 200);
  const positions = face.attributes.position.array.slice();
  const normals = face.attributes.normal.array.slice();
  new PanelTextureCoordinates().applyTo(face, "drawer-01-front");
  const uv = face.attributes.uv;
  assert.ok(Math.abs(uv.getX(1) - uv.getX(0) - 1.6) < 0.00001);
  assert.equal(uv.getY(1), uv.getY(0));
  assert.deepEqual(face.attributes.position.array, positions);
  assert.deepEqual(face.attributes.normal.array, normals);
});

test("tall panels carry grain vertically", () => {
  const face = new PlaneGeometry(600, 2200);
  new PanelTextureCoordinates().applyTo(face, "cabinet-side");
  const uv = face.attributes.uv;
  assert.equal(uv.getX(1), uv.getX(0));
  assert.ok(Math.abs(Math.abs(uv.getX(2) - uv.getX(0)) - 4.4) < 0.00001);
});

test("identical parts have stable but independently offset grain", () => {
  const first = new PlaneGeometry(800, 200);
  const repeated = first.clone();
  const different = first.clone();
  const mapping = new PanelTextureCoordinates();
  mapping.applyTo(first, "drawer-01-front");
  mapping.applyTo(repeated, "drawer-01-front");
  mapping.applyTo(different, "drawer-02-front");
  assert.deepEqual(first.attributes.uv.array, repeated.attributes.uv.array);
  assert.notDeepEqual(first.attributes.uv.array, different.attributes.uv.array);
});
