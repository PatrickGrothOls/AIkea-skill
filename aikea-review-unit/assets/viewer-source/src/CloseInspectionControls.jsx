/** Scope: Orbit one cabinet and keep pointer-directed wheel zoom useful up close. */

import { useEffect, useRef } from "react";
import { OrbitControls } from "@react-three/drei";
import { useThree } from "@react-three/fiber";

import { CloseInspectionZoomSpeed } from "./CloseInspectionZoomSpeed.js";

// A function component is the smallest React boundary for the control lifecycle hooks.
export function CloseInspectionControls({ modelSpan }) {
  const controlsRef = useRef(null);
  const camera = useThree((state) => state.camera);
  const gl = useThree((state) => state.gl);

  useEffect(() => {
    const controls = controlsRef.current;
    const zoomSpeed = new CloseInspectionZoomSpeed(modelSpan);
    const prepareCloseZoom = (event) => {
      const cameraDistance = camera.position.distanceTo(controls.target);
      controls.zoomSpeed = zoomSpeed.calculateForWheel(
        event.deltaY,
        cameraDistance,
      );
      queueMicrotask(() => {
        controls.zoomSpeed = 1;
      });
    };

    gl.domElement.addEventListener("wheel", prepareCloseZoom, {
      capture: true,
      passive: true,
    });
    return () => {
      gl.domElement.removeEventListener("wheel", prepareCloseZoom, true);
    };
  }, [camera, gl, modelSpan]);

  return (
    <OrbitControls
      enableDamping={false}
      makeDefault
      maxPolarAngle={Infinity}
      minPolarAngle={-Infinity}
      ref={controlsRef}
      zoomToCursor
    />
  );
}
