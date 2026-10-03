/** Scope: Load and surface the CAD scene, apply inspection state, and frame its visible bounds. */

import { useLayoutEffect, useMemo } from "react";
import { useThree } from "@react-three/fiber";
import { useTexture } from "@react-three/drei";
import { Vector3 } from "three";

import { AssemblyPresentation } from "./AssemblyPresentation.js";
import { LightingSource } from "./LightingSource.js";
import { LightingSurface } from "./LightingSurface.js";
import { PlywoodSurface } from "./PlywoodSurface.js";
import { ReviewCameraFraming } from "./ReviewCameraFraming.js";
import { ReviewVisibility } from "./ReviewVisibility.js";
import { ReviewMaterialSurface } from "./ReviewMaterialSurface.js";

// A function component owns the GLB/texture hooks and their scene lifecycle.
export function ReviewModel({ onModelMeasured, reviewView, inspection, doorsHidden, onSelectPart, gltf, resources, baked }) {
  const { scene, parser } = gltf;
  const presentation = useMemo(() => new AssemblyPresentation(scene, parser.associations), [scene, parser]);
  const framing = useMemo(() => new ReviewCameraFraming(), []);
  const [colorMap, normalMap, roughnessMap] = useTexture([
    "/materials/plywood/plywood_diff_1k.jpg",
    "/materials/plywood/plywood_nor_gl_1k.jpg",
    "/materials/plywood/plywood_rough_1k.jpg",
  ]);
  const camera = useThree((state) => state.camera);
  const controls = useThree((state) => state.controls);
  const renderer = useThree((state) => state.gl);
  const viewportSize = useThree((state) => state.size);

  useLayoutEffect(() => {
    const anisotropy = renderer.capabilities.getMaxAnisotropy();
    const surface = new ReviewMaterialSurface(
      new PlywoodSurface(colorMap, normalMap, roughnessMap, anisotropy), anisotropy);
    const lightingSurface = new LightingSurface(reviewView.showsLighting());
    presentation.scene.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        if (!baked) {
          surface.applyTo(node);
          lightingSurface.applyTo(node);
        }
      }
    });
    resources.track(presentation.scene, [colorMap, normalMap, roughnessMap]);
  }, [baked, colorMap, normalMap, presentation, renderer, resources, reviewView, roughnessMap]);

  useLayoutEffect(() => {
    const { bounds, visibleCount, groupCount } = presentation.apply(inspection.scope, inspection.amount, inspection.detail, doorsHidden);
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    framing.frame(camera, controls, reviewView, center, size);
    onModelMeasured({
      center: center.toArray(), size: size.toArray(),
      lightingSources: baked ? [] : LightingSource.collect(presentation.scene),
      modelRoot: presentation.scene,
      span: Math.max(size.x, size.y, size.z),
      scopes: presentation.scopes, visibleCount, groupCount, hasDoors: presentation.hasDoors,
    });
  }, [baked, camera, controls, framing, inspection.amount, inspection.scope, inspection.detail, doorsHidden,
    onModelMeasured, presentation, reviewView, viewportSize.width, viewportSize.height]);

  // Selection filters hidden meshes because Three.js raycasting includes them.
  const selectPart = (event) => {
    event.stopPropagation();
    const hit = event.intersections.find(({ object }) => object.isMesh && ReviewVisibility.isVisible(object));
    if (hit) {
      const name = presentation.catalog.nameFor(hit.object);
      onSelectPart(name, presentation.scopeForPart(name));
    }
  };

  return <primitive object={presentation.scene} onClick={selectPart} />;
}
