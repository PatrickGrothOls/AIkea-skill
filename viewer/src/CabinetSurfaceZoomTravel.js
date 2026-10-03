/** Scope: Calculate camera travel without crossing the cabinet surface or rotation point. */

const ORBIT_ZOOM_BASE = 0.95;
const WHEEL_DELTA_SCALE = 0.01;
const MODEL_SPAN_PER_DETAIL_STEP = 500;

export class CabinetSurfaceZoomTravel {
  constructor(modelSpan) {
    this.minimumTravel = modelSpan / MODEL_SPAN_PER_DETAIL_STEP;
  }

  calculateForWheel(
    deltaY,
    surfaceDistance,
    rotationCenterDistance,
    nearDistance,
  ) {
    const normalizedDelta = Math.abs(deltaY * WHEEL_DELTA_SCALE);
    const orbitScale = Math.pow(ORBIT_ZOOM_BASE, normalizedDelta);
    const minimumTravel = this.minimumTravel * normalizedDelta;
    const limitingDistance = Math.min(
      surfaceDistance,
      rotationCenterDistance,
    );

    if (deltaY < 0) {
      const proportionalTravel = limitingDistance * (1 - orbitScale);
      const availableTravel = Math.max(limitingDistance - nearDistance, 0);
      return Math.min(
        Math.max(proportionalTravel, minimumTravel),
        availableTravel,
      );
    }

    const proportionalTravel = limitingDistance * (1 / orbitScale - 1);
    return -Math.max(proportionalTravel, minimumTravel);
  }
}
