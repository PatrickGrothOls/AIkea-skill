/** Scope: Configure the shared color pipeline for the interactive review renderer. */

import { AgXToneMapping, PCFShadowMap, SRGBColorSpace } from "three";

// A stateless function matches Canvas's renderer-creation callback directly.
export function configureReviewRenderer({ gl }) {
  gl.outputColorSpace = SRGBColorSpace;
  gl.toneMapping = AgXToneMapping;
  gl.toneMappingExposure = 1.15;
  gl.shadowMap.enabled = true;
  gl.shadowMap.type = PCFShadowMap;
}
