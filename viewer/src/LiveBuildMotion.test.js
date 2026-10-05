/** Scope: Verify upward-only shimmer, eased arrivals and interruptible camera framing. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { Box3, BoxGeometry, Group, Mesh, MeshStandardMaterial, PerspectiveCamera, Vector3 } from "three";
import { LiveBuildSurface } from "./LiveBuildSurface.js";
import { LiveBuildCamera } from "./LiveBuildCamera.js";

test("shimmer travels upward and wraps outside the model; delayed parts ease in", () => {
  const model = new Group();
  model.add(new Mesh(new BoxGeometry(), new MeshStandardMaterial()));
  const surface = new LiveBuildSurface(model, false, 0.2);
  let previous = -Infinity;
  for (let time = 0; time < 3.2; time += 0.1) {
    surface.update(0, time, true);
    assert.ok(surface.uniforms.liveBand.value > previous);
    previous = surface.uniforms.liveBand.value;
  }
  assert.ok(previous > surface.bounds.max.y);
  surface.update(0.1, 3.2, true);
  assert.ok(surface.uniforms.liveBand.value < surface.bounds.min.y);
  assert.equal(model.visible, false);
  surface.update(0.575, 3.3, true);
  assert.ok(Math.abs(surface.materials[0].opacity - 0.5) < 0.001);
  surface.update(0.5, 3.4, false);
  assert.equal(surface.materials[0].opacity, 1);
  assert.equal(surface.arriving(), false);
  assert.equal(surface.uniforms.liveStrength.value, 0);
});

test("automatic framing glides to growing bounds and stops when the user orbits", () => {
  const camera = new PerspectiveCamera(40, 16 / 9);
  const controls = { target: new Vector3(), update() {} };
  const framing = new LiveBuildCamera();
  framing.fit(new Box3(new Vector3(), new Vector3(1, 1, 1)), camera, controls, false);
  const initial = camera.position.clone();
  framing.fit(new Box3(new Vector3(), new Vector3(2, 3, 1)), camera, controls, false);
  assert.deepEqual(camera.position, initial);
  const distance = camera.position.distanceTo(framing.position);
  framing.update(1 / 60, camera, controls);
  assert.ok(camera.position.distanceTo(framing.position) < distance);
  assert.ok(camera.position.distanceTo(initial) < distance / 5);
  framing.stop();
  const interrupted = camera.position.clone();
  framing.update(1, camera, controls);
  assert.deepEqual(camera.position, interrupted);
  framing.fit(new Box3(new Vector3(), new Vector3(4, 3, 1)), camera, controls, true);
  assert.deepEqual(camera.position, framing.position);
  assert.equal(framing.moving, false);
});
