/** Scope: Render area lights derived from purchased-light emitter geometry. */

import { useLayoutEffect, useRef } from "react";
import { Vector3 } from "three";

// A component boundary lets each derived strip preserve its own physical orientation.
function RecessedAreaLight({ source }) {
  const light = useRef();

  useLayoutEffect(() => {
    light.current.up.set(...source.up);
    light.current.lookAt(new Vector3(...source.target));
  }, [source]);

  return (
    <rectAreaLight
      ref={light}
      color={source.color}
      height={source.height}
      intensity={source.intensity}
      name={`${source.name}__area_light`}
      position={source.position}
      width={source.width}
    />
  );
}

// A function component is the smallest declarative boundary for the derived lights.
export function AssemblyLighting({ enabled, sources }) {
  if (!enabled) {
    return null;
  }
  return sources.map((source) => (
    <RecessedAreaLight key={source.name} source={source} />
  ));
}
