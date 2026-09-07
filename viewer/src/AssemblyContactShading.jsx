/** Scope: Finish interactive assembly renders with contact shading and tone mapping. */

import { EffectComposer, N8AO, ToneMapping } from "@react-three/postprocessing";

// A function component composes these stateless postprocessing effects.
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
      <ToneMapping />
    </EffectComposer>
  );
}
