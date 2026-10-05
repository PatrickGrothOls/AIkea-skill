/** Scope: Move straight white energy lines and soft halos through the active assembly. */
import { Vector3 } from "three";

export class LiveBuildShimmer {
  static period = 1.8;

  constructor() {
    this.uniforms = {
      liveBand: { value: 0 }, liveEchoBand: { value: 0 }, liveStrength: { value: 0 },
      liveOrigin: { value: new Vector3() }, liveScale: { value: 1 },
    };
  }

  update(time, active, bounds) {
    const height = Math.max(1, bounds.max.y - bounds.min.y);
    // Overlap two accelerating waves on the same clock, independent of part arrivals.
    for (const [index, key] of ["liveBand", "liveEchoBand"].entries()) {
      const phase = (time / LiveBuildShimmer.period + index * 0.5) % 1;
      this.uniforms[key].value = bounds.min.y + height * (phase * phase * 1.7 - 0.3);
    }
    this.uniforms.liveStrength.value = active ? 0.6 : 0;
    this.uniforms.liveOrigin.value.copy(bounds.min);
    this.uniforms.liveScale.value = 1 / height;
  }

  apply(shader) {
    Object.assign(shader.uniforms, this.uniforms);
    shader.vertexShader = `varying vec3 livePosition;\n${shader.vertexShader}`
      .replace("#include <project_vertex>",
        "#include <project_vertex>\nlivePosition = (modelMatrix * vec4(transformed, 1.0)).xyz;");
    shader.fragmentShader = `${LiveBuildShimmer.declarations}\n${shader.fragmentShader}`
      .replace("#include <opaque_fragment>", `${LiveBuildShimmer.fragment}\n#include <opaque_fragment>`);
  }

  static declarations = `
    varying vec3 livePosition;
    uniform float liveBand, liveEchoBand, liveStrength, liveScale;
    uniform vec3 liveOrigin;
    // Shared scalar falloff uses multiplication: GLSL pow is undefined for negative bases.
    float liveEnvelope(float distance, float width) {
      float scaled = distance / width;
      return exp(-2.0 * scaled * scaled);
    }
    // Height alone keeps the line straight and aligned across every part of the assembly.
    vec3 liveEnergyLine(float height, float head) {
      float distance = height - head;
      float pixel = max(fwidth(distance) * 1.3, 0.002);
      float core = liveEnvelope(distance, max(0.003, pixel));
      float halo = liveEnvelope(distance, 0.020);
      float aura = liveEnvelope(distance, 0.055);
      // Neutral emission gives a white electrical core with a soft, symmetric halo.
      return vec3(core * 4.0 + halo * 0.65 + aura * 0.12);
    }
  `;

  static fragment = `
    vec3 point = (livePosition - liveOrigin) * liveScale;
    float head = (liveBand - liveOrigin.y) * liveScale;
    float echo = (liveEchoBand - liveOrigin.y) * liveScale;
    // Preserve the approved accelerating motion; the lines never bend or ripple.
    outgoingLight += liveStrength * (
      liveEnergyLine(point.y, head) + liveEnergyLine(point.y, echo) * 0.85);
  `;
}
