/** Scope: Apply one world-space electric glint field with accelerating upward sweeps. */
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
    // Pure shader functions evaluate the same spatial field on every surface fragment.
    float liveHash(vec2 cell) {
      return fract(sin(dot(cell, vec2(127.1, 311.7))) * 43758.5453);
    }
    // Shared procedural sampling avoids storing geometry or per-part particle state.
    float liveStars(vec2 point) {
      vec2 grid = point * 34.0;
      vec2 cell = floor(grid);
      float seed = liveHash(cell);
      vec2 center = vec2(0.25) + 0.5 * vec2(seed, liveHash(cell + 19.3));
      vec2 offset = abs(fract(grid) - center);
      // Screen-space minimum thickness prevents fine sparks aliasing while orbiting.
      vec2 pixel = max(fwidth(grid), vec2(0.018));
      vec2 arm = max(pixel * 0.85, vec2(0.022));
      float core = exp(-dot(offset / max(pixel, vec2(0.055)), offset / max(pixel, vec2(0.055))));
      float cross = exp(-offset.x / arm.x - offset.y * 13.0)
                  + exp(-offset.y / arm.y - offset.x * 13.0);
      float twinkle = pow(0.5 + 0.5 * sin(liveTime * 7.0 + seed * 24.0), 3.0);
      return (core + cross * 0.6) * twinkle * smoothstep(0.52, 0.75, seed);
    }
  `;

  static fragment = `
    vec3 point = (livePosition - liveOrigin) * liveScale;
    float head = (liveBand - liveOrigin.y) * liveScale;
    float echo = (liveEchoBand - liveOrigin.y) * liveScale;
    float arc = 0.035 * sin(point.x * 11.0 + point.z * 7.0 + liveTime * 2.0);
    float distanceToHead = point.y - head + arc;
    float distanceToEcho = point.y - echo + arc;
    float envelope = liveEnvelope(distanceToHead, 0.13)
                   + liveEnvelope(distanceToEcho, 0.13);
    float trail = liveEnvelope(distanceToHead + 0.15, 0.20)
                + liveEnvelope(distanceToEcho + 0.15, 0.20);
    distanceToHead = abs(distanceToHead) < abs(distanceToEcho) ? distanceToHead : distanceToEcho;
    vec3 face = abs(normalize(cross(dFdx(livePosition), dFdy(livePosition))));
    face /= max(face.x + face.y + face.z, 0.0001);
    float stars = liveStars(point.xy) * face.z
                + liveStars(point.zy) * face.x + liveStars(point.xz) * face.y;
    float ripple = sin(point.x * 47.0 + point.z * 33.0 + liveTime * 4.0) * 0.008;
    float threadWidth = max(fwidth(distanceToHead) * 1.2, 0.002);
    float thread = exp(-abs(distanceToHead + ripple) / threadWidth);
    float fragments = smoothstep(0.15, 0.9, sin(point.x * 81.0 + point.z * 59.0 - liveTime * 5.0));
    // Emission is sparse: no broad fill, spotlight, material change, or extra geometry.
    outgoingLight += liveStrength * (
      vec3(1.65, 2.05, 2.50) * stars * (envelope * 3.0 + trail * 1.4)
      + vec3(0.55, 0.90, 1.35) * thread * fragments * 0.8);
  `;
}
