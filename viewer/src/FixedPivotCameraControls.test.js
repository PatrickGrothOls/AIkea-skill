/** Scope: Verify cursor zoom and orbit share one unchanged model-centre pivot. */

import assert from "node:assert/strict";
import test from "node:test";

import {
  BoxGeometry,
  Group,
  Mesh,
  MeshBasicMaterial,
  PerspectiveCamera,
  Vector2,
  Vector3,
} from "three";

import { FixedPivotCameraControls } from "./FixedPivotCameraControls.js";

const TOLERANCE = 0.000001;

// A factory keeps every test on the same explicit perspective-camera contract.
function createCamera() {
  const camera = new PerspectiveCamera(50, 1, 0.1, 1000);
  camera.position.set(0, 0, 10);
  camera.lookAt(0, 0, 0);
  camera.updateMatrixWorld();
  return camera;
}

// A factory gives pointer rays one off-centre cabinet surface to intersect.
function createModel() {
  const model = new Group();
  const detail = new Mesh(
    new BoxGeometry(2, 2, 2),
    new MeshBasicMaterial(),
  );
  detail.position.x = 2;
  model.add(detail);
  model.updateMatrixWorld(true);
  return model;
}

test("keeps the pointed surface at the same screen position while zooming", () => {
  const camera = createCamera();
  const controls = new FixedPivotCameraControls(camera, 100);
  controls.rotationCenter.set(0, 0, 0);
  controls.setModelRoot(createModel());
  const pointedSurface = new Vector3(2, 0, 1);
  const pointer = new Vector2(
    pointedSurface.clone().project(camera).x,
    pointedSurface.clone().project(camera).y,
  );

  const before = pointedSurface.clone().project(camera);
  const orientationBefore = camera.quaternion.clone();
  const pivotBefore = controls.rotationCenter.clone();
  const changed = controls.zoomTowardPointer(pointer, -100);
  const after = pointedSurface.clone().project(camera);

  assert.equal(changed, true);
  assert.ok(camera.position.x > 0);
  assert.ok(camera.position.z < 10);
  assert.ok(Math.abs(after.x - before.x) < TOLERANCE);
  assert.ok(Math.abs(after.y - before.y) < TOLERANCE);
  assert.ok(camera.quaternion.angleTo(orientationBefore) < TOLERANCE);
  assert.ok(controls.rotationCenter.distanceTo(pivotBefore) < TOLERANCE);
});

test("orbits the camera pose around the unchanged model centre", () => {
  const camera = createCamera();
  const controls = new FixedPivotCameraControls(camera, 100);
  controls.rotationCenter.set(0, 0, 0);
  controls.setModelRoot(createModel());
  const pointer = new Vector2(0.25, 0);
  controls.zoomTowardPointer(pointer, -100);
  const pivotBefore = controls.rotationCenter.clone();
  const pivotScreenBefore = pivotBefore.clone().project(camera);
  const distanceBefore = camera.position.distanceTo(pivotBefore);
  const positionBefore = camera.position.clone();
  const orientationBefore = camera.quaternion.clone();

  assert.equal(controls.orbitByPointerDelta(0, 0, 800), false);
  assert.ok(camera.position.distanceTo(positionBefore) < TOLERANCE);
  assert.ok(camera.quaternion.angleTo(orientationBefore) < TOLERANCE);

  controls.orbitByPointerDelta(80, -40, 800);

  const pivotScreenAfter = pivotBefore.clone().project(camera);
  assert.ok(camera.position.distanceTo(positionBefore) > 0);
  assert.ok(
    Math.abs(camera.position.distanceTo(pivotBefore) - distanceBefore)
      < TOLERANCE,
  );
  assert.ok(Math.abs(pivotScreenAfter.x - pivotScreenBefore.x) < TOLERANCE);
  assert.ok(Math.abs(pivotScreenAfter.y - pivotScreenBefore.y) < TOLERANCE);
  assert.ok(controls.rotationCenter.distanceTo(pivotBefore) < TOLERANCE);
});

test("pans only the camera across its viewing plane", () => {
  const camera = createCamera();
  const controls = new FixedPivotCameraControls(camera, 100);
  const model = createModel();
  controls.rotationCenter.set(0, 0, 0);
  controls.setModelRoot(model);
  const cameraPositionBefore = camera.position.clone();
  const cameraOrientationBefore = camera.quaternion.clone();
  const modelPositionBefore = model.position.clone();
  const rotationCenterBefore = controls.rotationCenter.clone();
  const rotationCenterScreenBefore = rotationCenterBefore.clone().project(camera);

  const changed = controls.panCameraByPixels(-80, 40, 800);

  const rotationCenterScreenAfter = rotationCenterBefore.clone().project(camera);
  assert.equal(changed, true);
  assert.ok(camera.position.distanceTo(cameraPositionBefore) > 0);
  assert.ok(camera.quaternion.angleTo(cameraOrientationBefore) < TOLERANCE);
  assert.ok(model.position.distanceTo(modelPositionBefore) < TOLERANCE);
  assert.ok(controls.rotationCenter.distanceTo(rotationCenterBefore) < TOLERANCE);
  assert.ok(rotationCenterScreenAfter.x > rotationCenterScreenBefore.x);
  assert.ok(rotationCenterScreenAfter.y < rotationCenterScreenBefore.y);

  controls.orbitByPointerDelta(80, -40, 800);
  const rotationCenterScreenAfterOrbit = rotationCenterBefore
    .clone()
    .project(camera);
  assert.ok(
    Math.abs(rotationCenterScreenAfterOrbit.x - rotationCenterScreenAfter.x)
      < TOLERANCE,
  );
  assert.ok(
    Math.abs(rotationCenterScreenAfterOrbit.y - rotationCenterScreenAfter.y)
      < TOLERANCE,
  );
  assert.ok(model.position.distanceTo(modelPositionBefore) < TOLERANCE);
});
