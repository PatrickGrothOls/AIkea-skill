/** Scope: Display one generated assembly GLB with realistic materials, automatic framing, and direct orbit controls. */

import { lazy, Suspense, useLayoutEffect, useState } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { useGLTF, useTexture } from "@react-three/drei";
import {
  Box3,
  Vector3,
} from "three";

import { AssemblyContactShading } from "./AssemblyContactShading";
import { AssemblyStudioFloor } from "./AssemblyStudioFloor";
import { AssemblyStudioEnvironment } from "./AssemblyStudioEnvironment";
import { AssemblyStudioLights } from "./AssemblyStudioLights";
import { AssemblyLighting } from "./AssemblyLighting";
import { CloseInspectionControls } from "./CloseInspectionControls";
import { LightingSource } from "./LightingSource";
import { LightingSurface } from "./LightingSurface";
import { PlywoodSurface } from "./PlywoodSurface";
import { ReviewGuidanceCard } from "./ReviewGuidanceCard";
import { ReviewApprovalPanel } from "./ReviewApprovalPanel";
import { configureReviewRenderer } from "./ReviewRenderer";
import { ReviewView } from "./ReviewView";

const AssemblyPhotoRenderer = lazy(() => import("./AssemblyPhotoRenderer"));

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
    const lightingSurface = new LightingSurface(reviewView.showsLighting());
    scene.rotation.x = -Math.PI / 2;
    scene.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        surface.applyTo(node);
        lightingSurface.applyTo(node);
      }
    });
    scene.updateMatrixWorld(true);
    const bounds = new Box3().setFromObject(scene);
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    onModelMeasured({
      center: center.toArray(),
      lightingSources: LightingSource.collect(scene),
      modelRoot: scene,
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
      controls.rotationCenter.copy(center);
      controls.update();
    }
  }, [camera, colorMap, controls, normalMap, onModelMeasured, renderer, reviewView, roughnessMap, scene]);

  return <primitive object={scene} />;
}

// A function component keeps the viewer as a self-contained render-only asset.
export function AssemblyReviewViewer() {
  const [modelBounds, setModelBounds] = useState({
    center: [0, 0, 0],
    lightingSources: [],
    modelRoot: null,
    size: [1, 1, 1],
    span: 1,
  });
  const [reviewView] = useState(() => ReviewView.fromSearch(window.location.search));
  const assemblyScene = (
    <>
      {reviewView.showsStudioFloor() && (
        <AssemblyStudioFloor modelBounds={modelBounds} />
      )}
      <Suspense fallback={null}>
        <AssemblyStudioEnvironment />
        <AssemblyStudioLights modelBounds={modelBounds} />
        <AssemblyLighting
          enabled={reviewView.showsLighting()}
          sources={modelBounds.lightingSources}
        />
        <ReviewModel onModelMeasured={setModelBounds} reviewView={reviewView} />
      </Suspense>
    </>
  );

  return (
    <main
      className="review-shell"
      data-light-source-count={modelBounds.lightingSources.length}
    >
      <Canvas
        camera={{ position: [150, 100, 150], fov: 50 }}
        dpr={[1, 2]}
        gl={{ antialias: true, powerPreference: "high-performance" }}
        onCreated={configureReviewRenderer}
      >
        <color attach="background" args={["#d8d5ce"]} />
        <CloseInspectionControls
          modelRoot={modelBounds.modelRoot}
          modelSpan={modelBounds.span}
        />
        {reviewView.usesPhotoRenderer() ? (
          <Suspense fallback={assemblyScene}>
            <AssemblyPhotoRenderer key={`photo-${modelBounds.span}`}>
              {assemblyScene}
            </AssemblyPhotoRenderer>
          </Suspense>
        ) : (
          assemblyScene
        )}
        {!reviewView.usesPhotoRenderer() && <AssemblyContactShading />}
      </Canvas>
      <ReviewGuidanceCard reviewView={reviewView} />
      <ReviewApprovalPanel ready={modelBounds.modelRoot !== null} />
    </main>
  );
}
