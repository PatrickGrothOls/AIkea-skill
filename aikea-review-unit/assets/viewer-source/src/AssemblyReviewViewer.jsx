/** Scope: Display one cabinet GLB with automatic framing and direct orbit controls. */

import { Suspense, useLayoutEffect } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { Box3, Vector3 } from "three";

// A function component is the smallest React boundary for the GLB-loading hook.
function ReviewModel() {
  const { scene } = useGLTF("/model.glb");
  const camera = useThree((state) => state.camera);
  const controls = useThree((state) => state.controls);

  useLayoutEffect(() => {
    scene.rotation.x = -Math.PI / 2;
    scene.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        for (const material of [node.material].flat()) {
          material.metalness = 0;
          material.roughness = 0.78;
          material.needsUpdate = true;
        }
      }
    });
    scene.updateMatrixWorld(true);
    const bounds = new Box3().setFromObject(scene);
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    const verticalFov = camera.fov * Math.PI / 180;
    const horizontalFov = 2 * Math.atan(Math.tan(verticalFov / 2) * camera.aspect);
    const distance = Math.max(
      size.y / (2 * Math.tan(verticalFov / 2)),
      size.x / (2 * Math.tan(horizontalFov / 2)),
      size.z,
    ) * 1.35;
    const viewDirection = new Vector3(1, 0.45, 1).normalize();
    camera.position.copy(center).addScaledVector(viewDirection, distance);
    camera.near = Math.max(distance / 1000, 0.1);
    camera.far = distance * 100;
    camera.lookAt(center);
    camera.updateProjectionMatrix();
    if (controls) {
      controls.target.copy(center);
      controls.update();
    }
  }, [camera, controls, scene]);

  return <primitive object={scene} />;
}

// A function component keeps the viewer as a self-contained render-only asset.
export function AssemblyReviewViewer() {
  return (
    <main className="review-shell">
      <Canvas shadows camera={{ position: [150, 100, 150], fov: 50 }}>
        <color attach="background" args={["#f4f0e8"]} />
        <ambientLight intensity={0.95} />
        <hemisphereLight args={["#ffffff", "#bba98e", 1.1]} />
        <directionalLight
          castShadow
          intensity={2}
          position={[1200, 2600, 3200]}
          shadow-mapSize={[2048, 2048]}
        />
        <OrbitControls enableDamping={false} makeDefault minPolarAngle={-Infinity} maxPolarAngle={Infinity} />
        <Suspense fallback={null}>
          <ReviewModel />
        </Suspense>
      </Canvas>
      <section className="review-card">
        <p className="eyebrow">AIkea visual review</p>
        <h1>Your first cabinet</h1>
        <p>Drag to rotate. Scroll or pinch to zoom.</p>
      </section>
    </main>
  );
}
