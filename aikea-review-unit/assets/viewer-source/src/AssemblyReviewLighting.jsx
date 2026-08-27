/** Scope: Light the reviewed assembly with neutral studio reflections and soft directional shadows. */

import { useEffect, useLayoutEffect, useRef } from "react";
import { useThree } from "@react-three/fiber";
import { PMREMGenerator } from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

export function AssemblyReviewLighting({ modelBounds }) {
  const keyLight = useRef(null);
  const keyTarget = useRef(null);
  const renderer = useThree((state) => state.gl);
  const scene = useThree((state) => state.scene);
  const { center, span } = modelBounds;

  useEffect(() => {
    const environment = new RoomEnvironment();
    const environmentBuilder = new PMREMGenerator(renderer);
    const environmentMap = environmentBuilder.fromScene(environment, 0.04).texture;
    const previousEnvironment = scene.environment;
    const previousEnvironmentIntensity = scene.environmentIntensity;
    scene.environment = environmentMap;
    scene.environmentIntensity = 0.32;

    return () => {
      scene.environment = previousEnvironment;
      scene.environmentIntensity = previousEnvironmentIntensity;
      environmentMap.dispose();
      environmentBuilder.dispose();
    };
  }, [renderer, scene]);

  useLayoutEffect(() => {
    if (!keyLight.current || !keyTarget.current) {
      return;
    }
    keyLight.current.target = keyTarget.current;
    keyLight.current.shadow.camera.updateProjectionMatrix();
  }, [center, span]);

  return (
    <>
      <hemisphereLight args={["#fff7e9", "#8a7c69", 0.08]} />
      <object3D ref={keyTarget} position={center} />
      <directionalLight
        castShadow
        color="#fff4df"
        intensity={2.35}
        position={[
          center[0] - span * 0.75,
          center[1] + span * 2.1,
          center[2] + span * 0.7,
        ]}
        ref={keyLight}
        shadow-bias={-0.0001}
        shadow-blurSamples={16}
        shadow-camera-bottom={-span}
        shadow-camera-far={span * 5}
        shadow-camera-left={-span}
        shadow-camera-near={span * 0.05}
        shadow-camera-right={span}
        shadow-camera-top={span}
        shadow-mapSize={[2048, 2048]}
        shadow-normalBias={0.6}
        shadow-radius={8}
      />
      <directionalLight
        color="#d8e3f0"
        intensity={0.18}
        position={[
          center[0] + span * 0.8,
          center[1] + span * 0.35,
          center[2] + span * 0.45,
        ]}
      />
    </>
  );
}
