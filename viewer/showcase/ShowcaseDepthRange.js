/** Scope: Keep camera depth precision focused on the visible CAD assembly. */
import { Sphere } from "three";

export class ShowcaseDepthRange {
  constructor(camera, occlusion) {
    this.camera = camera;
    this.occlusion = occlusion;
    this.sphere = new Sphere();
  }

  update(bounds) {
    bounds.getBoundingSphere(this.sphere);
    const distance = this.camera.position.distanceTo(this.sphere.center);
    const radius = this.sphere.radius * 1.1;
    this.camera.near = Math.max(0.005, distance - radius);
    this.camera.far = Math.max(this.camera.near + 1, distance + radius);
    this.camera.updateProjectionMatrix();
    // SSAO compares normalized linear depth; retain physical thresholds as clipping changes.
    const range = this.camera.far - this.camera.near;
    this.occlusion.minDistance = 0.00005 / range;
    this.occlusion.maxDistance = 0.1 / range;
    // SSAOPass caches these uniforms instead of refreshing them in render().
    for (const material of [this.occlusion.ssaoMaterial, this.occlusion.depthRenderMaterial]) {
      material.uniforms.cameraNear.value = this.camera.near;
      material.uniforms.cameraFar.value = this.camera.far;
    }
    this.occlusion.ssaoMaterial.uniforms.cameraProjectionMatrix.value.copy(this.camera.projectionMatrix);
    this.occlusion.ssaoMaterial.uniforms.cameraInverseProjectionMatrix.value.copy(this.camera.projectionMatrixInverse);
  }
}
