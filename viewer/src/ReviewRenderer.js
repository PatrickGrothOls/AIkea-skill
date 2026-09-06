/** Scope: Configure the shared color pipeline for the interactive review renderer. */

import { AgXToneMapping, SRGBColorSpace } from "three";

export function configureReviewRenderer({ gl }) {
  gl.outputColorSpace = SRGBColorSpace;
  gl.toneMapping = AgXToneMapping;
  gl.toneMappingExposure = 1.15;
}
