/** Scope: Add screen-space contact and corner shading to the exact reviewed assembly geometry. */

import { EffectComposer, N8AO } from "@react-three/postprocessing";

// A function component declares one reusable contact-shading pass for the live scene.
export function AssemblyContactShading() {
  return (
    <EffectComposer multisampling={4}>
      <N8AO
        aoRadius={14}
        color="#16120f"
        denoiseRadius={4}
        distanceFalloff={1}
        intensity={1.25}
        quality="medium"
      />
    </EffectComposer>
  );
}
