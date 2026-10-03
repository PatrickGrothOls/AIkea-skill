/** Scope: Keep camera depth precision focused on the visible CAD assembly. */
import { Sphere } from "three";

export class ShowcaseDepthRange {
  constructor(camera) {
    this.camera = camera;
    this.sphere = new Sphere();
  }

  update(bounds) {
    bounds.getBoundingSphere(this.sphere);
    const distance = this.camera.position.distanceTo(this.sphere.center);
    const radius = this.sphere.radius * 1.1;
    this.camera.near = Math.max(0.005, distance - radius);
    this.camera.far = Math.max(this.camera.near + 1, distance + radius);
    this.camera.updateProjectionMatrix();
  }
}
