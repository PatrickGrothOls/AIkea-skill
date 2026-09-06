/** Scope: Place two broad photographic softboxes around the reviewed assembly. */

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

// A function component expresses the two-light studio arrangement without owning scene state.
export function AssemblyStudioLights({ modelBounds }) {
  const { center, span } = modelBounds;
  const target = [center[0], center[1] + span * 0.08, center[2]];

  return (
    <>
      <StudioSoftbox
        color="#fff4df"
        height={span * 1.25}
        intensity={5.5}
        position={[
          center[0] + span * 1.15,
          center[1] + span * 0.95,
          center[2] + span * 1.2,
        ]}
        target={target}
        width={span * 1.25}
      />
      <StudioSoftbox
        color="#e8f0ff"
        height={span * 0.9}
        intensity={2.2}
        position={[
          center[0] - span * 1.1,
          center[1] + span * 0.35,
          center[2] + span,
        ]}
        target={target}
        width={span}
      />
    </>
  );
}
