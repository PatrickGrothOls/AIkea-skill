/** Scope: Display one cabinet GLB with automatic framing and direct orbit controls. */

import { Suspense, useLayoutEffect, useState } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { useGLTF, useTexture } from "@react-three/drei";
import { Box3, Vector3 } from "three";

import { CloseInspectionControls } from "./CloseInspectionControls";
import { PlywoodSurface } from "./PlywoodSurface";
import { ReviewView } from "./ReviewView";

// A function component is the smallest React boundary for the GLB-loading hook.
function ReviewModel({ onModelFramed, reviewView }) {
  const { scene } = useGLTF("/model.glb");
  const [colorMap, normalMap, roughnessMap] = useTexture([
    "/materials/plywood/plywood_diff_1k.jpg",
    "/materials/plywood/plywood_nor_gl_1k.jpg",
    "/materials/plywood/plywood_rough_1k.jpg",
  ]);
  const camera = useThree((state) => state.camera);
  const controls = useThree((state) => state.controls);

  useLayoutEffect(() => {
    const surface = new PlywoodSurface(colorMap, normalMap, roughnessMap);
    scene.rotation.x = -Math.PI / 2;
    scene.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        surface.applyTo(node);
      }
    });
    scene.updateMatrixWorld(true);
    const bounds = new Box3().setFromObject(scene);
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    onModelFramed(Math.max(size.x, size.y, size.z));
    const verticalFov = camera.fov * Math.PI / 180;
    const horizontalFov = 2 * Math.atan(Math.tan(verticalFov / 2) * camera.aspect);
    const distance = reviewView.cameraDistance(size, verticalFov, horizontalFov);
    const viewDirection = new Vector3(...reviewView.cameraDirection()).normalize();
    camera.up.set(...reviewView.cameraUp());
    camera.position.copy(center).addScaledVector(viewDirection, distance);
    camera.near = Math.max(distance / 1000, 0.1);
    camera.far = distance * 100;
    camera.lookAt(center);
    camera.updateProjectionMatrix();
    if (controls) {
      controls.target.copy(center);
      controls.update();
    }
  }, [camera, colorMap, controls, normalMap, onModelFramed, reviewView, roughnessMap, scene]);

  return <primitive object={scene} />;
}

// A function component keeps the viewer as a self-contained render-only asset.
export function AssemblyReviewViewer() {
  const [modelSpan, setModelSpan] = useState(1);
  const [reviewView] = useState(() => ReviewView.fromSearch(window.location.search));

  return (
    <main className="review-shell">
      <Canvas shadows camera={{ position: [150, 100, 150], fov: 50 }}>
        <color attach="background" args={["#eee9df"]} />
        <ambientLight intensity={0.5} />
        <hemisphereLight args={["#fffaf0", "#8e806d", 0.8]} />
        <directionalLight
          castShadow
          intensity={1.7}
          position={[1200, 2600, 3200]}
          shadow-mapSize={[2048, 2048]}
        />
        <directionalLight intensity={0.7} position={[-1000, -1600, 1800]} />
        <CloseInspectionControls modelSpan={modelSpan} />
        <Suspense fallback={null}>
          <ReviewModel onModelFramed={setModelSpan} reviewView={reviewView} />
        </Suspense>
      </Canvas>
      <section className="review-card">
        <p className="eyebrow">AIkea visual review</p>
        <h1>{reviewView.title}</h1>
        <p>{reviewView.guidance()}</p>
      </section>
    </main>
  );
}
