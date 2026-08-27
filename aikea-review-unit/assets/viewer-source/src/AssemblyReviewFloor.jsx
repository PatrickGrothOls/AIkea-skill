/** Scope: Ground a perspective assembly review on a neutral shadow-catching floor. */

export function AssemblyReviewFloor({ modelBounds }) {
  const { center, size, span } = modelBounds;
  const floorHeight = center[1] - size[1] / 2 - Math.max(span * 0.0001, 0.2);

  return (
    <mesh
      position={[center[0], floorHeight, center[2]]}
      receiveShadow
      rotation={[-Math.PI / 2, 0, 0]}
    >
      <planeGeometry args={[span * 30, span * 30]} />
      <shadowMaterial color="#4e4438" opacity={0.14} transparent />
    </mesh>
  );
}
