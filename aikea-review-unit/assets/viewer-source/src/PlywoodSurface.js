/** Scope: Apply the packaged photographed plywood PBR maps to review meshes. */

import {
  Float32BufferAttribute,
  RepeatWrapping,
  SRGBColorSpace,
} from "three";

const TEXTURE_SCALE_MM = 500;

export class PlywoodSurface {
  constructor(colorMap, normalMap, roughnessMap) {
    this.colorMap = colorMap;
    this.normalMap = normalMap;
    this.roughnessMap = roughnessMap;
    this.#prepareMaps();
  }

  applyTo(mesh) {
    this.#addLocalTextureCoordinates(mesh.geometry);
    for (const material of [mesh.material].flat()) {
      material.color.set("#ffffff");
      material.map = this.colorMap;
      material.normalMap = this.normalMap;
      material.normalScale.set(0.35, 0.35);
      material.roughnessMap = this.roughnessMap;
      material.metalness = 0;
      material.roughness = 0.96;
      material.needsUpdate = true;
    }
  }

  #prepareMaps() {
    this.colorMap.colorSpace = SRGBColorSpace;
    for (const texture of [
      this.colorMap,
      this.normalMap,
      this.roughnessMap,
    ]) {
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
