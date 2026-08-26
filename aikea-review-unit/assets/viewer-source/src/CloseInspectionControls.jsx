/** Scope: Orbit one cabinet and keep pointer-directed wheel zoom useful up close. */

import { useEffect, useRef } from "react";
import { OrbitControls } from "@react-three/drei";
import { useThree } from "@react-three/fiber";
import { Raycaster, Vector2 } from "three";

import { PointerZoomTravel } from "./PointerZoomTravel.js";

// A function component is the smallest React boundary for the control lifecycle hooks.
export function CloseInspectionControls({ modelSpan }) {
  const controlsRef = useRef(null);
  const camera = useThree((state) => state.camera);
  const gl = useThree((state) => state.gl);
  const scene = useThree((state) => state.scene);

  useEffect(() => {
    const controls = controlsRef.current;
    const raycaster = new Raycaster();
    const pointer = new Vector2();
    const zoomTravel = new PointerZoomTravel(modelSpan);
    // One captured wheel boundary avoids target-limited dolly work on every frame.
    const moveTowardPointer = (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();

      const bounds = gl.domElement.getBoundingClientRect();
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, camera);
      const intersections = raycaster.intersectObjects(scene.children, true);
      const surfaceDistance = intersections.length
        ? intersections[0].distance
        : modelSpan;
      const travel = zoomTravel.calculateForWheel(
        event.deltaY,
        surfaceDistance,
        camera.near,
      );
      camera.position.addScaledVector(raycaster.ray.direction, travel);
      controls.target.addScaledVector(raycaster.ray.direction, travel);
      camera.updateMatrixWorld();
      controls.update();
    };

    gl.domElement.addEventListener("wheel", moveTowardPointer, {
      capture: true,
      passive: false,
    });
    return () => {
      gl.domElement.removeEventListener("wheel", moveTowardPointer, true);
    };
  }, [camera, gl, modelSpan, scene]);

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
