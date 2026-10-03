/** Scope: Light the studio backdrop without unoccluded cabinet-strip spill. */

import { MeshStandardMaterial, ShaderChunk } from "three";

export class StudioBackdropMaterial extends MeshStandardMaterial {
  constructor() {
    super({ color: "#ded3c2", envMapIntensity: 0.75, metalness: 0, roughness: 0.95 });
  }

  onBeforeCompile(shader) {
    // Inspection strip lights have no shadow maps. Exclude their contribution
    // from the backdrop so light cannot appear to pass through the cabinet base.
    const backdropLighting = ShaderChunk.lights_fragment_begin.replace(
      "#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )",
      "#if 0 // Cabinet strip illumination is limited to the furniture.",
    );
    shader.fragmentShader = shader.fragmentShader.replace(
      "#include <lights_fragment_begin>", backdropLighting,
    );
  }

  customProgramCacheKey() {
    return "studio-backdrop-without-strip-spill-v1";
  }
}
