/** Scope: Animate part arrival and bind the assembly glint field without changing CAD geometry. */

import { Box3 } from "three";
import { LiveBuildShimmer } from "./LiveBuildShimmer.js";

export class LiveBuildSurface {
  constructor(scene, reducedMotion, delay = 0) {
    this.scene = scene;
    this.reducedMotion = reducedMotion;
    this.elapsed = 0;
    this.delay = reducedMotion ? 0 : delay;
    this.duration = reducedMotion ? 0 : 0.95;
    this.materials = [];
    this.bounds = new Box3().setFromObject(scene);
    this.shimmer = new LiveBuildShimmer();
    this.uniforms = this.shimmer.uniforms;
    scene.traverse((node) => {
      if (!node.isMesh) return;
      for (const material of [node.material].flat()) {
        if (this.materials.includes(material)) continue;
        this.materials.push(material);
        material.transparent = !reducedMotion;
        material.opacity = reducedMotion ? 1 : 0;
        material.onBeforeCompile = (shader) => this.shimmer.apply(shader);
        material.customProgramCacheKey = () => "aikea-live-shimmer-v3";
      }
    });
  }

  update(delta, time, active, bounds = this.bounds) {
    this.elapsed += delta;
    const progress = this.reducedMotion ? 1 : Math.min(1, Math.max(0, (this.elapsed - this.delay) / this.duration));
    const opacity = progress * progress * (3 - 2 * progress);
    this.scene.visible = progress > 0;
    for (const material of this.materials) {
      material.opacity = opacity;
      if (opacity === 1 && material.transparent) {
        material.transparent = false;
        material.needsUpdate = true;
      }
    }
    this.shimmer.update(time, active && !this.reducedMotion, bounds);
  }

  arriving() {
    return this.elapsed < this.delay + this.duration;
  }
}
