/** Scope: Animate arrival and a soft moving highlight without changing CAD geometry. */

import { Box3 } from "three";

export class LiveBuildSurface {
  constructor(scene, reducedMotion, delay = 0) {
    this.scene = scene;
    this.reducedMotion = reducedMotion;
    this.elapsed = 0;
    this.delay = reducedMotion ? 0 : delay;
    this.duration = reducedMotion ? 0 : 0.95;
    this.materials = [];
    this.bounds = new Box3().setFromObject(scene);
    this.uniforms = { liveBand: { value: 0 }, liveStrength: { value: 0 }, liveWidth: { value: 1 } };
    scene.traverse((node) => {
      if (!node.isMesh) return;
      for (const material of [node.material].flat()) {
        if (this.materials.includes(material)) continue;
        this.materials.push(material);
        material.transparent = !reducedMotion;
        material.opacity = reducedMotion ? 1 : 0;
        material.onBeforeCompile = (shader) => {
          Object.assign(shader.uniforms, this.uniforms);
          shader.vertexShader = `varying vec3 livePosition;\n${shader.vertexShader}`
            .replace("#include <project_vertex>",
              "#include <project_vertex>\nlivePosition = (modelMatrix * vec4(transformed, 1.0)).xyz;");
          shader.fragmentShader = `varying vec3 livePosition;
            uniform float liveBand; uniform float liveStrength; uniform float liveWidth;
            ${shader.fragmentShader}`.replace("#include <opaque_fragment>", `
              float sweep = (livePosition.y - liveBand) / liveWidth;
              float band = exp(-sweep * sweep * 3.0);
              float threads = 0.5 + 0.5 * sin(sweep * 32.0 + livePosition.x / liveWidth * 5.0);
              float glint = pow(threads, 8.0) * band;
              outgoingLight += (vec3(0.40, 0.30, 0.16) * band
                + vec3(0.95, 0.84, 0.62) * glint) * liveStrength;
              #include <opaque_fragment>`);
        };
        material.customProgramCacheKey = () => "aikea-live-shimmer-v2";
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
    const height = Math.max(1, bounds.max.y - bounds.min.y);
    // Wrap outside the furniture so the next upward sweep starts invisibly below it.
    this.uniforms.liveBand.value = bounds.min.y + height * ((time % 3.2) / 3.2 * 1.6 - 0.3);
    this.uniforms.liveWidth.value = height * 0.12;
    this.uniforms.liveStrength.value = active && !this.reducedMotion ? 0.6 : 0;
  }

  arriving() {
    return this.elapsed < this.delay + this.duration;
  }
}
