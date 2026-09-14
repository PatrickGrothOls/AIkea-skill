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

// A function component expresses the studio arrangement without owning scene state.
export function AssemblyStudioLights({ modelBounds }) {
  const { center, span } = modelBounds;
  const target = [center[0], center[1] + span * 0.08, center[2]];

  return (
    <>
      <StudioSoftbox
        color="#fff2dc"
        height={span * 1.1}
        intensity={11}
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
