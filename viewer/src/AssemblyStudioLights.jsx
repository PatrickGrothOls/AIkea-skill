/** Scope: Place a key, fill, and backdrop light around the reviewed assembly. */

import { useLayoutEffect, useRef } from "react";
import { Vector3 } from "three";

// A component boundary lets each area light orient itself after React creates it.
function StudioSoftbox({ color, height, intensity, position, target, width }) {
  const light = useRef();

  useLayoutEffect(() => {
    light.current.lookAt(new Vector3(...target));
  }, [target]);

  return (
    <rectAreaLight
      ref={light}
      color={color}
      height={height}
      intensity={intensity}
      position={position}
      width={width}
    />
  );
}

// This component owns the shadow camera for the same light direction as the studio key.
function StudioWindowLight({ modelBounds }) {
  const { center, span } = modelBounds;
  const light = useRef();
  useLayoutEffect(() => {
    light.current.target.position.set(...center);
    light.current.target.updateMatrixWorld();
    light.current.shadow.camera.updateProjectionMatrix();
  }, [center, span]);
  return (
    <directionalLight ref={light} color="#fff8ee" intensity={0.8} castShadow
      position={[center[0] - span * .9, center[1] + span * 1.4, center[2] + span]}
      shadow-mapSize={[2048, 2048]} shadow-bias={-0.00003} shadow-normalBias={0.25}
      shadow-camera-left={-span * 1.1} shadow-camera-right={span * 1.1}
      shadow-camera-top={span * 1.1} shadow-camera-bottom={-span * 1.1}
      shadow-camera-near={span * .01} shadow-camera-far={span * 5}
      shadow-radius={3} />
  );
}

// A function component expresses the studio arrangement without owning scene state.
export function AssemblyStudioLights({ modelBounds }) {
  const { center, span } = modelBounds;
  const target = [center[0], center[1] + span * 0.08, center[2]];

  return (
    <>
      <StudioWindowLight modelBounds={modelBounds} />
      <StudioSoftbox
        color="#fff2dc"
        height={span * 1.1}
        intensity={3.5}
        position={[
          center[0] - span * 0.75,
          center[1] + span * 1.1,
          center[2] + span * 0.9,
        ]}
        target={target}
        width={span * 0.65}
      />
      <StudioSoftbox
        color="#eef3ff"
        height={span * 0.75}
        intensity={0.9}
        position={[
          center[0] + span * 1.1,
          center[1] + span * 0.35,
          center[2] + span * 0.6,
        ]}
        target={target}
        width={span}
      />
      <StudioSoftbox
        color="#fff8ed"
        height={span}
        intensity={3}
        position={[center[0], center[1] + span * 0.5, center[2] - span * 0.6]}
        target={[center[0], center[1] + span * 0.5, center[2] - span * 2.5]}
        width={span * 2}
      />
    </>
  );
}
