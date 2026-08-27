/** Scope: Progressively path-trace one exact assembly scene for photo-quality review. */

import { Pathtracer } from "@react-three/gpu-pathtracer";

export default function AssemblyPhotoRenderer({ children }) {
  return (
    <Pathtracer
      bounces={4}
      dynamicLowRes={false}
      fadeDuration={500}
      filteredGlossyFactor={0.5}
      minSamples={32}
      rasterizeScene
      renderDelay={350}
      resolutionFactor={0.5}
      samples={512}
      tiles={2}
    >
      {children}
    </Pathtracer>
  );
}
