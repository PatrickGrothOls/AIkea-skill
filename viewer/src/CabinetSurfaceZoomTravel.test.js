/** Scope: Verify cabinet-centred zoom keeps useful travel until the surface is reached. */

import assert from "node:assert/strict";
import test from "node:test";

import { CabinetSurfaceZoomTravel } from "./CabinetSurfaceZoomTravel.js";

test("uses proportional travel while the cabinet surface is far away", () => {
  const zoomTravel = new CabinetSurfaceZoomTravel(2400);

  assert.ok(
    Math.abs(zoomTravel.calculateForWheel(-100, 1000, 1000, 0.1) - 50)
      < 0.000001,
  );
});

test("keeps a model-scale step near the cabinet surface", () => {
  const zoomTravel = new CabinetSurfaceZoomTravel(2400);

  assert.ok(
    Math.abs(zoomTravel.calculateForWheel(-100, 20, 20, 0.1) - 4.8)
      < 0.000001,
  );
  assert.ok(
    Math.abs(zoomTravel.calculateForWheel(-100, 5, 5, 0.1) - 4.8)
      < 0.000001,
  );
});

test("stops before the camera clipping plane crosses the surface", () => {
  const zoomTravel = new CabinetSurfaceZoomTravel(2400);

  assert.ok(
    Math.abs(zoomTravel.calculateForWheel(-100, 1, 1, 0.1) - 0.9)
      < 0.000001,
  );
});

test("stops before crossing the cabinet rotation point", () => {
  const zoomTravel = new CabinetSurfaceZoomTravel(2400);
  const travel = zoomTravel.calculateForWheel(-250, 783, 86.7, 3.45);

  assert.ok(Math.abs(travel - 12) < 0.000001);
  assert.ok(travel < 86.7 - 3.45);
});

test("returns negative travel when zooming away from the surface", () => {
  const zoomTravel = new CabinetSurfaceZoomTravel(2400);

  assert.ok(zoomTravel.calculateForWheel(100, 20, 20, 0.1) < 0);
});
