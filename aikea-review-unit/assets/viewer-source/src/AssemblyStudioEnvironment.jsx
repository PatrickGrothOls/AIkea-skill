/** Scope: Illuminate the reviewed assembly from one packaged photographic studio environment. */

import { Environment } from "@react-three/drei";

const STUDIO_ENVIRONMENT_PATH =
  "/environments/studio-small-08/studio_small_08_1k.hdr";

export function AssemblyStudioEnvironment() {
  return (
    <Environment
      background
      backgroundBlurriness={0.82}
      backgroundIntensity={0.72}
      environmentIntensity={1.25}
      environmentRotation={[0, -Math.PI / 3, 0]}
      files={STUDIO_ENVIRONMENT_PATH}
    />
  );
}
