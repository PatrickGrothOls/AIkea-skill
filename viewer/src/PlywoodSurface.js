/** Scope: Apply the packaged photographed plywood PBR maps to review meshes. */

import {
  Float32BufferAttribute,
  RepeatWrapping,
  SRGBColorSpace,
} from "three";

const TEXTURE_SCALE_MM = 500;
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
    this.#prepareMaps(anisotropy);
  }

  applyTo(mesh) {
    if (
      mesh.name.startsWith(REVIEW_ONLY_PREFIX) ||
      mesh.name.includes(SOURCE_CAD_MARKER) ||
      mesh.name.startsWith(PURCHASED_LIGHT_PREFIX) ||
      mesh.name.startsWith(LIGHT_SOURCE_PREFIX)
    ) {
      return;
    }
    this.#addLocalTextureCoordinates(mesh.geometry);
    const useFaceMaterial = isPlywoodFace(mesh.geometry);
    const replacementMaterials = [mesh.material]
      .flat()
      .map((material) => this.#getMaterial(material, useFaceMaterial));
    mesh.material = Array.isArray(mesh.material)
      ? replacementMaterials
      : replacementMaterials[0];
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
    material.normalScale.set(0.24, 0.24);
    material.roughnessMap = this.roughnessMap;
    material.envMapIntensity = 1;
    material.metalness = 0;
    material.roughness = 0.92;
    material.needsUpdate = true;
    return material;
  }

  #createEdgeMaterial(sourceMaterial) {
    const material = sourceMaterial.clone();
    material.color.set("#cfb27f");
    material.map = this.colorMap;
    material.normalMap = null;
    material.roughnessMap = null;
    material.envMapIntensity = 0.7;
    material.metalness = 0;
    material.roughness = 0.88;
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

  #addLocalTextureCoordinates(geometry) {
    const positions = geometry.getAttribute("position");
    const normals = geometry.getAttribute("normal");
    const coordinates = new Float32Array(positions.count * 2);

    for (let index = 0; index < positions.count; index += 1) {
      const x = positions.getX(index);
      const y = positions.getY(index);
      const z = positions.getZ(index);
      const normalX = Math.abs(normals.getX(index));
      const normalY = Math.abs(normals.getY(index));
      const normalZ = Math.abs(normals.getZ(index));
      const coordinateOffset = index * 2;

      if (normalZ >= normalX && normalZ >= normalY) {
        coordinates[coordinateOffset] = y / TEXTURE_SCALE_MM;
        coordinates[coordinateOffset + 1] = x / TEXTURE_SCALE_MM;
      } else if (normalX >= normalY) {
        coordinates[coordinateOffset] = y / TEXTURE_SCALE_MM;
        coordinates[coordinateOffset + 1] = z / TEXTURE_SCALE_MM;
      } else {
        coordinates[coordinateOffset] = x / TEXTURE_SCALE_MM;
        coordinates[coordinateOffset + 1] = z / TEXTURE_SCALE_MM;
      }
    }

    geometry.setAttribute("uv", new Float32BufferAttribute(coordinates, 2));
  }
}

export function isPlywoodFace(geometry) {
  const normals = geometry.getAttribute("normal");
  let normalZTotal = 0;
  for (let index = 0; index < normals.count; index += 1) {
    normalZTotal += Math.abs(normals.getZ(index));
  }
  return normalZTotal / normals.count >= 0.8;
}
