/** Scope: Ground a perspective review on a seamless neutral studio sweep. */

import { useEffect, useMemo } from "react";
import { StudioBackdropGeometry } from "./StudioBackdropGeometry.js";
import { StudioBackdropMaterial } from "./StudioBackdropMaterial.js";

// A function component places one presentation surface beneath measured geometry.
export function AssemblyStudioFloor({ modelBounds }) {
  const { center, size, span } = modelBounds;
  const floorHeight = center[1] - size[1] / 2 - Math.max(span * 0.0001, 0.2);
  const geometry = useMemo(() => new StudioBackdropGeometry(span), [span]);
  const material = useMemo(() => new StudioBackdropMaterial(), []);
  useEffect(() => () => geometry.dispose(), [geometry]);
  useEffect(() => () => material.dispose(), [material]);

  return (
    <mesh
      position={[center[0], floorHeight, center[2]]}
      receiveShadow
      geometry={geometry}
      material={material}
    >
    </mesh>
  );
}
