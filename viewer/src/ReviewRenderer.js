/** Scope: Configure the shared color pipeline for the interactive review renderer. */

import { AgXToneMapping, SRGBColorSpace } from "three";

// This stateless callback configures the renderer supplied by React Three Fiber.
export function configureReviewRenderer({ gl }, exposure = 1.15) {
  gl.outputColorSpace = SRGBColorSpace;
  gl.toneMapping = AgXToneMapping;
  gl.toneMappingExposure = exposure;
}
