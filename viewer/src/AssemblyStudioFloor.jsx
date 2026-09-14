/** Scope: Ground a perspective review on a seamless neutral studio sweep. */

import { useEffect, useMemo } from "react";
import { StudioBackdropGeometry } from "./StudioBackdropGeometry.js";

// A function component places one presentation surface beneath measured geometry.
export function AssemblyStudioFloor({ modelBounds }) {
  const { center, size, span } = modelBounds;
  const floorHeight = center[1] - size[1] / 2 - Math.max(span * 0.0001, 0.2);
  const geometry = useMemo(() => new StudioBackdropGeometry(span), [span]);
  useEffect(() => () => geometry.dispose(), [geometry]);

  return (
    <mesh
      position={[center[0], floorHeight, center[2]]}
      receiveShadow
      geometry={geometry}
    >
      <meshStandardMaterial
        color="#ded3c2"
        envMapIntensity={0.75}
        metalness={0}
        roughness={0.95}
      />
    </mesh>
  );
}
