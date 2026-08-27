/** Scope: Ground a perspective assembly review on one neutral studio floor. */

export function AssemblyStudioFloor({ modelBounds }) {
  const { center, size, span } = modelBounds;
  const floorHeight = center[1] - size[1] / 2 - Math.max(span * 0.0001, 0.2);

  return (
    <mesh
      position={[center[0], floorHeight, center[2]]}
      receiveShadow
      rotation={[-Math.PI / 2, 0, 0]}
    >
      <planeGeometry args={[span * 30, span * 30]} />
      <meshStandardMaterial
        color="#c9c5bd"
        envMapIntensity={0.75}
        metalness={0}
        roughness={0.95}
      />
    </mesh>
  );
}
