/** Scope: Apply a smooth satin paint preview to furniture surfaces and cut edges. */

import { MeshStandardMaterial } from "three";
import { ReviewMaterialScope } from "./ReviewMaterialScope.js";

export class PaintedSurface {
  constructor(color = "#f4f3ee") {
    // A warm white screen preview is not a calibrated RAL colour sample.
    this.material = new MeshStandardMaterial({
      color,
      roughness: 0.55,
      metalness: 0,
      envMapIntensity: 0.85,
    });
  }

  applyTo(mesh) {
    if (!ReviewMaterialScope.preservesSource(mesh)) {
      mesh.material = this.material;
    }
  }
}
