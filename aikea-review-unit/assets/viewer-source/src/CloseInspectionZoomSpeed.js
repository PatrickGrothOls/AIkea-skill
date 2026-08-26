/** Scope: Calculate OrbitControls wheel speed for model-scale close inspection. */

const DEFAULT_ZOOM_SPEED = 1;
const ORBIT_ZOOM_BASE = 0.95;
const WHEEL_DELTA_SCALE = 0.01;
const MODEL_SPAN_PER_DETAIL_STEP = 500;
const MAX_DISTANCE_SHARE_PER_STEP = 0.8;

export class CloseInspectionZoomSpeed {
  constructor(modelSpan) {
    this.minimumTravel = modelSpan / MODEL_SPAN_PER_DETAIL_STEP;
  }

  calculateForWheel(deltaY, cameraDistance) {
    if (deltaY >= 0) {
      return DEFAULT_ZOOM_SPEED;
    }

    const normalizedDelta = Math.abs(deltaY * WHEEL_DELTA_SCALE);
    const defaultScale = Math.pow(
      ORBIT_ZOOM_BASE,
      DEFAULT_ZOOM_SPEED * normalizedDelta,
    );
    const defaultTravel = cameraDistance * (1 - defaultScale);
    const minimumTravel = this.minimumTravel * normalizedDelta;
    if (defaultTravel >= minimumTravel) {
      return DEFAULT_ZOOM_SPEED;
    }

    const closeTravel = Math.min(
      minimumTravel,
      cameraDistance * MAX_DISTANCE_SHARE_PER_STEP,
    );
    const closeScale = 1 - closeTravel / cameraDistance;
    return Math.log(closeScale) / (Math.log(ORBIT_ZOOM_BASE) * normalizedDelta);
  }
}
