/** Scope: Calculate signed camera travel toward the cabinet surface under the pointer. */

const ORBIT_ZOOM_BASE = 0.95;
const WHEEL_DELTA_SCALE = 0.01;
const MODEL_SPAN_PER_DETAIL_STEP = 500;

export class PointerZoomTravel {
  constructor(modelSpan) {
    this.minimumTravel = modelSpan / MODEL_SPAN_PER_DETAIL_STEP;
  }

  calculateForWheel(deltaY, surfaceDistance, nearDistance) {
    const normalizedDelta = Math.abs(deltaY * WHEEL_DELTA_SCALE);
    const orbitScale = Math.pow(ORBIT_ZOOM_BASE, normalizedDelta);
    const minimumTravel = this.minimumTravel * normalizedDelta;

    if (deltaY < 0) {
      const proportionalTravel = surfaceDistance * (1 - orbitScale);
      const availableTravel = Math.max(surfaceDistance - nearDistance, 0);
      return Math.min(
        Math.max(proportionalTravel, minimumTravel),
        availableTravel,
      );
    }

    const proportionalTravel = surfaceDistance * (1 / orbitScale - 1);
    return -Math.max(proportionalTravel, minimumTravel);
  }
}
