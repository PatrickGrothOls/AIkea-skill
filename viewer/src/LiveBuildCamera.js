/** Scope: Ease automatic framing between CAD revisions without overriding user orbit. */

import { Vector3 } from "three";

export class LiveBuildCamera {
  constructor() {
    this.position = new Vector3();
    this.target = new Vector3();
    this.initialized = false;
    this.moving = false;
  }

  fit(bounds, camera, controls, reducedMotion) {
    if (!bounds || bounds.isEmpty()) return;
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    const vertical = camera.fov * Math.PI / 180;
    const limitingFov = Math.min(vertical, 2 * Math.atan(Math.tan(vertical / 2) * camera.aspect));
    this.distance = size.length() / (2 * Math.sin(limitingFov / 2)) * 1.1;
    this.position.copy(center).addScaledVector(new Vector3(1, 0.65, 1.5).normalize(), this.distance);
    this.target.copy(center);
    camera.near = Math.max(this.distance / 10000, 0.001);
    camera.far = Math.max(this.distance * 100, 100);
    camera.updateProjectionMatrix();
    this.moving = true;
    if (!this.initialized || reducedMotion) this.update(1, camera, controls, true);
    this.initialized = true;
  }

  update(delta, camera, controls, immediate = false) {
    if (!this.moving) return;
    const blend = immediate ? 1 : 1 - Math.exp(-delta * 5);
    camera.position.lerp(this.position, blend);
    controls.target.lerp(this.target, blend);
    if (camera.position.distanceTo(this.position) + controls.target.distanceTo(this.target) < this.distance * 0.0001) {
      camera.position.copy(this.position);
      controls.target.copy(this.target);
      this.moving = false;
    }
    controls.update();
  }

  stop() {
    this.moving = false;
  }
}
