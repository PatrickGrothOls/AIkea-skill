/** Scope: Fit changed inspection bounds while preserving the user's viewing direction. */

import { Vector3 } from "three";

export class ReviewCameraFraming {
  frame(camera, controls, reviewView, center, size) {
    const direction = this.previousCenter
      ? camera.position.clone().sub(this.previousCenter).normalize()
      : new Vector3(...reviewView.cameraDirection()).normalize();
    const verticalFov = camera.fov * Math.PI / 180;
    const horizontalFov = 2 * Math.atan(Math.tan(verticalFov / 2) * camera.aspect);
    const distance = reviewView.cameraDistance(size, verticalFov, horizontalFov);
    camera.up.set(...reviewView.cameraUp());
    camera.position.copy(center).addScaledVector(direction, distance);
    camera.near = Math.max(distance / 1000, 0.1);
    camera.far = distance * 100;
    camera.lookAt(center);
    camera.updateProjectionMatrix();
    if (controls) {
      controls.rotationCenter.copy(center);
      controls.update();
    }
    this.previousCenter = center.clone();
  }
}
