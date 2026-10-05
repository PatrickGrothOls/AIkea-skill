/** Scope: Animate arrival and a soft moving highlight without changing CAD geometry. */

import { Box3 } from "three";

export class LiveBuildSurface {
  constructor(scene, reducedMotion) {
    this.scene = scene;
    this.reducedMotion = reducedMotion;
    this.elapsed = 0;
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
          shader.vertexShader = `varying float liveHeight;\n${shader.vertexShader}`
            .replace("#include <project_vertex>",
              "#include <project_vertex>\nliveHeight = (modelMatrix * vec4(transformed, 1.0)).y;");
          shader.fragmentShader = `varying float liveHeight;
            uniform float liveBand; uniform float liveStrength; uniform float liveWidth;
            ${shader.fragmentShader}`.replace("#include <opaque_fragment>", `
              float band = 1.0 - smoothstep(0.0, liveWidth, abs(liveHeight - liveBand));
              outgoingLight += vec3(0.48, 0.36, 0.20) * band * liveStrength;
              #include <opaque_fragment>`);
        };
        material.customProgramCacheKey = () => "aikea-live-band-v1";
      }
    });
  }

  update(delta, time, active, bounds = this.bounds) {
    this.elapsed += delta;
    const opacity = this.reducedMotion ? 1 : Math.min(1, this.elapsed / 0.45);
    for (const material of this.materials) {
      material.opacity = opacity;
      if (opacity === 1 && material.transparent) {
        material.transparent = false;
        material.needsUpdate = true;
      }
    }
    const height = Math.max(1, bounds.max.y - bounds.min.y);
    this.uniforms.liveBand.value = bounds.min.y + height * (0.5 - Math.cos(time * 1.6) * 0.5);
    this.uniforms.liveWidth.value = height * 0.16;
    this.uniforms.liveStrength.value = active && !this.reducedMotion ? 0.6 : 0;
  }
}
