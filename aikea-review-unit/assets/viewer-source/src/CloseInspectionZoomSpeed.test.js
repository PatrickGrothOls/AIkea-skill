/** Scope: Verify close inspection keeps useful wheel travel near small cabinet details. */

import assert from "node:assert/strict";
import test from "node:test";

import { CloseInspectionZoomSpeed } from "./CloseInspectionZoomSpeed.js";

const ORBIT_ZOOM_BASE = 0.95;

// A function is the smallest clear expression of OrbitControls' wheel travel.
function calculateTravel(cameraDistance, deltaY, zoomSpeed) {
  const normalizedDelta = Math.abs(deltaY * 0.01);
  const scale = Math.pow(ORBIT_ZOOM_BASE, zoomSpeed * normalizedDelta);
  return cameraDistance * (1 - scale);
}

test("keeps the ordinary OrbitControls speed while the model is far away", () => {
  const zoom = new CloseInspectionZoomSpeed(2400);

  assert.equal(zoom.calculateForWheel(-100, 1000), 1);
});

test("maintains a model-scale inspection step near a detail", () => {
  const zoom = new CloseInspectionZoomSpeed(2400);
  const speed = zoom.calculateForWheel(-100, 20);
  const travel = calculateTravel(20, -100, speed);

  assert.ok(speed > 1);
  assert.ok(Math.abs(travel - 4.8) < 0.000001);
});

test("does not accelerate zooming away from a detail", () => {
  const zoom = new CloseInspectionZoomSpeed(2400);

  assert.equal(zoom.calculateForWheel(100, 20), 1);
});
