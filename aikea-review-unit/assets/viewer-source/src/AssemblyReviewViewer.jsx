/** Scope: Display one generated assembly GLB with realistic materials, automatic framing, and direct orbit controls. */

import { Suspense, useLayoutEffect, useState } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { useGLTF, useTexture } from "@react-three/drei";
import {
  AgXToneMapping,
  Box3,
  SRGBColorSpace,
  Vector3,
} from "three";

import { AssemblyReviewFloor } from "./AssemblyReviewFloor";
import { AssemblyReviewLighting } from "./AssemblyReviewLighting";
import { CloseInspectionControls } from "./CloseInspectionControls";
import { PlywoodSurface } from "./PlywoodSurface";
import { ReviewView } from "./ReviewView";

function configureReviewRenderer({ gl }) {
  gl.outputColorSpace = SRGBColorSpace;
  gl.toneMapping = AgXToneMapping;
  gl.toneMappingExposure = 0.9;
}

// A function component is the smallest React boundary for the GLB-loading hook.
function ReviewModel({ onModelMeasured, reviewView }) {
  const { scene } = useGLTF("/model.glb");
  const [colorMap, normalMap, roughnessMap] = useTexture([
    "/materials/plywood/plywood_diff_1k.jpg",
    "/materials/plywood/plywood_nor_gl_1k.jpg",
    "/materials/plywood/plywood_rough_1k.jpg",
  ]);
  const camera = useThree((state) => state.camera);
  const controls = useThree((state) => state.controls);
  const renderer = useThree((state) => state.gl);

  useLayoutEffect(() => {
    const surface = new PlywoodSurface(
      colorMap,
      normalMap,
      roughnessMap,
      renderer.capabilities.getMaxAnisotropy(),
    );
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
    onModelMeasured({
      center: center.toArray(),
      size: size.toArray(),
      span: Math.max(size.x, size.y, size.z),
    });
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
  }, [camera, colorMap, controls, normalMap, onModelMeasured, renderer, reviewView, roughnessMap, scene]);

  return <primitive object={scene} />;
}

// A function component keeps the viewer as a self-contained render-only asset.
export function AssemblyReviewViewer() {
  const [modelBounds, setModelBounds] = useState({
    center: [0, 0, 0],
    size: [1, 1, 1],
    span: 1,
  });
  const [reviewView] = useState(() => ReviewView.fromSearch(window.location.search));

  return (
    <main className="review-shell">
      <Canvas
        camera={{ position: [150, 100, 150], fov: 50 }}
        dpr={[1, 2]}
        gl={{ antialias: true, powerPreference: "high-performance" }}
        onCreated={configureReviewRenderer}
        shadows="variance"
      >
        <color attach="background" args={["#d8d5ce"]} />
        <AssemblyReviewLighting modelBounds={modelBounds} />
        {reviewView.showsFloor() && (
          <AssemblyReviewFloor modelBounds={modelBounds} />
        )}
        <CloseInspectionControls modelSpan={modelBounds.span} />
        <Suspense fallback={null}>
          <ReviewModel onModelMeasured={setModelBounds} reviewView={reviewView} />
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
