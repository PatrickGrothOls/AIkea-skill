/** Scope: Bind pointer gestures to cabinet-detail zoom, camera panning, and model-centre rotation. */

import { useEffect, useLayoutEffect, useMemo } from "react";
import { useThree } from "@react-three/fiber";
import { Vector2 } from "three";

import { FixedPivotCameraControls } from "./FixedPivotCameraControls.js";

// A function component is the smallest React boundary for the control lifecycle hooks.
export function CloseInspectionControls({ modelRoot, modelSpan }) {
  const camera = useThree((state) => state.camera);
  const gl = useThree((state) => state.gl);
  const get = useThree((state) => state.get);
  const invalidate = useThree((state) => state.invalidate);
  const set = useThree((state) => state.set);
  const controls = useMemo(
    () => new FixedPivotCameraControls(camera, modelSpan),
    [camera],
  );

  useLayoutEffect(() => {
    const previousControls = get().controls;
    set({ controls });
    return () => set({ controls: previousControls });
  }, [controls, get, set]);

  useEffect(() => {
    controls.setModelRoot(modelRoot);
    controls.setModelSpan(modelSpan);
  }, [controls, modelRoot, modelSpan]);

  useEffect(() => {
    controls.addEventListener("change", invalidate);
    return () => controls.removeEventListener("change", invalidate);
  }, [controls, invalidate]);

  useEffect(() => {
    const element = gl.domElement;
    const pointer = new Vector2();
    const drag = { pointerId: null, x: 0, y: 0 };
    const previousTouchAction = element.style.touchAction;
    element.style.touchAction = "none";

    // A local conversion keeps DOM coordinates out of the camera-control class.
    const pointerFromEvent = (event) => {
      const bounds = element.getBoundingClientRect();
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      return pointer;
    };

    const moveCameraWithWheel = (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (event.shiftKey) {
        controls.panCameraByPixels(
          event.deltaX,
          -event.deltaY,
          element.clientHeight,
        );
        return;
      }
      controls.zoomTowardPointer(pointerFromEvent(event), event.deltaY);
    };

    const beginCameraDrag = (event) => {
      if (event.button !== 0 || drag.pointerId !== null) {
        return;
      }
      event.preventDefault();
      drag.pointerId = event.pointerId;
      drag.x = event.clientX;
      drag.y = event.clientY;
      element.setPointerCapture(event.pointerId);
      controls.dispatchEvent({ type: "start" });
    };

    const moveCameraFromDrag = (event) => {
      if (event.pointerId !== drag.pointerId) {
        return;
      }
      event.preventDefault();
      const deltaX = event.clientX - drag.x;
      const deltaY = event.clientY - drag.y;
      drag.x = event.clientX;
      drag.y = event.clientY;
      if (event.shiftKey) {
        controls.panCameraByPixels(-deltaX, deltaY, element.clientHeight);
      } else {
        controls.orbitByPointerDelta(deltaX, deltaY, element.clientHeight);
      }
    };

    const endCameraDrag = (event) => {
      if (event.pointerId !== drag.pointerId) {
        return;
      }
      drag.pointerId = null;
      if (element.hasPointerCapture(event.pointerId)) {
        element.releasePointerCapture(event.pointerId);
      }
      controls.dispatchEvent({ type: "end" });
    };

    element.addEventListener("wheel", moveCameraWithWheel, {
      capture: true,
      passive: false,
    });
    element.addEventListener("pointerdown", beginCameraDrag, true);
    element.addEventListener("pointermove", moveCameraFromDrag, true);
    element.addEventListener("pointerup", endCameraDrag, true);
    element.addEventListener("pointercancel", endCameraDrag, true);
    return () => {
      element.style.touchAction = previousTouchAction;
      element.removeEventListener("wheel", moveCameraWithWheel, true);
      element.removeEventListener("pointerdown", beginCameraDrag, true);
      element.removeEventListener("pointermove", moveCameraFromDrag, true);
      element.removeEventListener("pointerup", endCameraDrag, true);
      element.removeEventListener("pointercancel", endCameraDrag, true);
    };
  }, [controls, gl]);

  return null;
}
