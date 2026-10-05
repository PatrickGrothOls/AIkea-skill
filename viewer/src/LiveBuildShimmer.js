/** Scope: Carry continuous luminous ribbons through assembly surfaces on one shared clock. */
import { Vector3 } from "three";

export class LiveBuildShimmer {
  static period = 1.8;

  constructor() {
    this.uniforms = {
      liveBand: { value: 0 }, liveEchoBand: { value: 0 }, liveStrength: { value: 0 },
      liveOrigin: { value: new Vector3() }, liveScale: { value: 1 }, liveTime: { value: 0 },
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
    this.uniforms.liveTime.value = time;
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
    uniform float liveBand, liveEchoBand, liveStrength, liveScale, liveTime;
    uniform vec3 liveOrigin;
    // Shared scalar falloff uses multiplication: GLSL pow is undefined for negative bases.
    float liveEnvelope(float distance, float width) {
      float scaled = distance / width;
      return exp(-2.0 * scaled * scaled);
    }
    // Continuous scalar fields give every mesh the same flowing ribbon, without particles.
    vec3 liveRibbon(vec3 point, float head, float offset) {
      float across = point.x * 3.4 + point.z * 2.7;
      float bend = sin(across * 2.6 + liveTime * 1.1 + offset) * 0.055
                 + sin(across * 5.1 - liveTime * 0.65 + offset) * 0.022;
      float distance = point.y - head + bend;
      float fold = sin(across * 3.2 + distance * 12.0 - liveTime * 1.4 + offset);
      float taper = 0.70 + 0.30 * sin(across * 1.7 + liveTime * 0.8 + offset);
      float width = 0.010 + 0.009 * (0.5 + 0.5 * fold);
      float pixel = max(fwidth(distance) * 1.3, 0.002);
      float edge = liveEnvelope(distance, max(width * 0.25, pixel));
      float body = liveEnvelope(distance + width, width * 1.8);
      float wake = liveEnvelope(distance + 0.055, 0.065) * 0.22;
      float echo = liveEnvelope(distance + 0.11 + fold * 0.015, max(pixel, 0.003)) * 0.28;
      // A bright continuous crest stretches into a translucent wake, like luminous silk.
      return taper * (vec3(1.25, 1.90, 2.50) * edge
        + vec3(0.18, 0.70, 1.20) * body
        + vec3(0.30, 0.25, 0.85) * (wake + echo));
    }
  `;

  static fragment = `
    vec3 point = (livePosition - liveOrigin) * liveScale;
    float head = (liveBand - liveOrigin.y) * liveScale;
    float echo = (liveEchoBand - liveOrigin.y) * liveScale;
    // Whole ribbons travel together; no spatial grid, point flashes, or per-part phase.
    outgoingLight += liveStrength * (
      liveRibbon(point, head, 0.0) + liveRibbon(point, echo, 1.3) * 0.85);
  `;
}
