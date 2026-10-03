/** Scope: Apply the packaged photographed plywood PBR maps to review meshes. */

import { ReviewMeshName } from "./ReviewMeshName.js";
import { PanelTextureCoordinates } from "./PanelTextureCoordinates.js";

import {
  RepeatWrapping,
  SRGBColorSpace,
} from "three";

const REVIEW_ONLY_PREFIX = "review_only__";
const SOURCE_CAD_MARKER = "__source_cad";
const PURCHASED_LIGHT_PREFIX = "purchased_light__";
const LIGHT_SOURCE_PREFIX = "light_source__";

export class PlywoodSurface {
  constructor(colorMap, normalMap, roughnessMap, anisotropy) {
    this.colorMap = colorMap;
    this.normalMap = normalMap;
    this.roughnessMap = roughnessMap;
    this.materialsBySource = new WeakMap();
    this.coordinates = new PanelTextureCoordinates();
    this.#prepareMaps(anisotropy);
  }

  applyTo(mesh) {
    if (
      this.#isPurchasedHardware(mesh) ||
      ReviewMeshName.hasRole(mesh.name, REVIEW_ONLY_PREFIX) ||
      mesh.name.includes(SOURCE_CAD_MARKER) ||
      ReviewMeshName.hasRole(mesh.name, PURCHASED_LIGHT_PREFIX) ||
      ReviewMeshName.hasRole(mesh.name, LIGHT_SOURCE_PREFIX)
    ) {
      return;
    }
    this.coordinates.applyTo(mesh.geometry, mesh.parent?.name || mesh.name);
    const useFaceMaterial = isPlywoodFace(mesh.geometry);
    const replacementMaterials = [mesh.material]
      .flat()
      .map((material) => this.#getMaterial(material, useFaceMaterial));
    mesh.material = Array.isArray(mesh.material)
      ? replacementMaterials
      : replacementMaterials[0];
  }

  #isPurchasedHardware(mesh) {
    for (let node = mesh; node; node = node.parent) {
      if (node.userData.aikea?.kind === "hardware") return true;
    }
    return false;
  }

  #getMaterial(sourceMaterial, useFaceMaterial) {
    if (!this.materialsBySource.has(sourceMaterial)) {
      this.materialsBySource.set(sourceMaterial, {
        edge: this.#createEdgeMaterial(sourceMaterial),
        face: this.#createFaceMaterial(sourceMaterial),
      });
    }
    const materials = this.materialsBySource.get(sourceMaterial);
    return useFaceMaterial ? materials.face : materials.edge;
  }

  #createFaceMaterial(sourceMaterial) {
    const material = sourceMaterial.clone();
    material.color.set("#ffffff");
    material.map = this.colorMap;
    material.normalMap = this.normalMap;
    material.normalScale.set(0.12, 0.12);
    material.roughnessMap = this.roughnessMap;
    material.envMapIntensity = 1;
    material.metalness = 0;
    material.roughness = 0.48;
    material.needsUpdate = true;
    return material;
  }

  #createEdgeMaterial(sourceMaterial) {
    const material = sourceMaterial.clone();
    material.color.set("#e4ceb0");
    material.map = this.colorMap;
    material.normalMap = null;
    material.roughnessMap = null;
    material.envMapIntensity = 1;
    material.metalness = 0;
    material.roughness = 0.62;
    material.needsUpdate = true;
    return material;
  }

  #prepareMaps(anisotropy) {
    this.colorMap.colorSpace = SRGBColorSpace;
    for (const texture of [
      this.colorMap,
      this.normalMap,
      this.roughnessMap,
    ]) {
      texture.anisotropy = anisotropy;
      texture.wrapS = RepeatWrapping;
      texture.wrapT = RepeatWrapping;
      texture.needsUpdate = true;
    }
  }
}

// A pure predicate classifies only this normal buffer; it needs no material state.
export function isPlywoodFace(geometry) {
  const normals = geometry.getAttribute("normal");
  let normalZTotal = 0;
  for (let index = 0; index < normals.count; index += 1) {
    normalZTotal += Math.abs(normals.getZ(index));
  }
  return normalZTotal / normals.count >= 0.8;
}
