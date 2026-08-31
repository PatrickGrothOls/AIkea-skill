/** Scope: Add screen-space contact and corner shading to the exact reviewed assembly geometry. */

import { EffectComposer, N8AO } from "@react-three/postprocessing";

export function AssemblyContactShading() {
  return (
    <EffectComposer multisampling={4}>
      <N8AO
        aoRadius={65}
        color="#30271e"
        denoiseRadius={8}
        distanceFalloff={1}
        intensity={1.7}
        quality="medium"
      />
    </EffectComposer>
  );
}
