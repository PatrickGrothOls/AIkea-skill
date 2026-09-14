/** Scope: Illuminate the reviewed assembly from one packaged photographic studio environment. */

import { Environment } from "@react-three/drei";

const STUDIO_ENVIRONMENT_PATH =
  "/environments/studio-small-08/studio_small_08_1k.hdr";

// A function component declares the shared fill light without owning scene state.
export function AssemblyStudioEnvironment() {
  return (
    <Environment
      environmentIntensity={0.28}
      environmentRotation={[0, -Math.PI / 3, 0]}
      files={STUDIO_ENVIRONMENT_PATH}
    />
  );
}
