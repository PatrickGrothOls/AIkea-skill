/** Scope: Bind the photo renderer's owned lifetime to the existing Three.js scene. */

import { useLayoutEffect, useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { PhotoRenderSession } from "./PhotoRenderSession.js";

// A function component integrates renderer setup, frame callbacks, and teardown.
export default function AssemblyPhotoRenderer({ enabled }) {
  const { gl, scene, camera, controls } = useThree();
  const session = useRef(null);
  useLayoutEffect(() => {
    session.current = new PhotoRenderSession(gl, scene, camera, controls);
    return () => {
      session.current.dispose();
      session.current = null;
    };
  }, [gl, scene, camera, controls]);
  useFrame(() => session.current?.render(enabled, document.hidden), 1);
  return null;
}
