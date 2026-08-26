/** Scope: Orbit one cabinet around its center and move straight closer for inspection. */

import { useEffect, useRef } from "react";
import { OrbitControls } from "@react-three/drei";
import { useThree } from "@react-three/fiber";
import { Raycaster, Vector3 } from "three";

import { CabinetSurfaceZoomTravel } from "./CabinetSurfaceZoomTravel.js";

// A function component is the smallest React boundary for the control lifecycle hooks.
export function CloseInspectionControls({ modelSpan }) {
  const controlsRef = useRef(null);
  const camera = useThree((state) => state.camera);
  const gl = useThree((state) => state.gl);
  const scene = useThree((state) => state.scene);

  useEffect(() => {
    const controls = controlsRef.current;
    const raycaster = new Raycaster();
    const zoomDirection = new Vector3();
    const zoomTravel = new CabinetSurfaceZoomTravel(modelSpan);
    // One captured wheel boundary avoids target-limited dolly work on every frame.
    const moveAlongCabinetAxis = (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();

      zoomDirection.copy(controls.target).sub(camera.position).normalize();
      const targetDistance = camera.position.distanceTo(controls.target);
      raycaster.set(camera.position, zoomDirection);
      const intersections = raycaster.intersectObjects(scene.children, true);
      const surfaceDistance = intersections.length
        ? intersections[0].distance
        : targetDistance;
      const travel = zoomTravel.calculateForWheel(
        event.deltaY,
        surfaceDistance,
        targetDistance,
        camera.near,
      );
      camera.position.addScaledVector(zoomDirection, travel);
      camera.updateMatrixWorld();
    };

    gl.domElement.addEventListener("wheel", moveAlongCabinetAxis, {
      capture: true,
      passive: false,
    });
    return () => {
      gl.domElement.removeEventListener("wheel", moveAlongCabinetAxis, true);
    };
  }, [camera, gl, modelSpan, scene]);

  return (
    <OrbitControls
      enableDamping={false}
      enablePan={false}
      makeDefault
      maxPolarAngle={Infinity}
      minPolarAngle={-Infinity}
      ref={controlsRef}
    />
  );
}
