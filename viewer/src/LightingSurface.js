/** Scope: Give exported light emitters their lit or unlit review material. */

import { Color } from "three";

import { LIGHT_SOURCE_PREFIX } from "./LightingSource.js";

export class LightingSurface {
  constructor(enabled) {
    this.enabled = enabled;
  }

  applyTo(mesh) {
    if (!mesh.name.startsWith(LIGHT_SOURCE_PREFIX)) {
      return;
    }
    const materials = [mesh.material].flat().map((source) => {
      const material = source.clone();
      const lightColor = source.color.clone();
      material.color = this.enabled ? lightColor : new Color("#6d6b66");
      material.emissive = this.enabled ? lightColor : new Color("#000000");
      material.emissiveIntensity = this.enabled ? 1.5 : 0;
      material.metalness = 0;
      material.roughness = 0.45;
      material.toneMapped = !this.enabled;
      material.needsUpdate = true;
      return material;
    });
    mesh.material = Array.isArray(mesh.material) ? materials : materials[0];
  }
}
