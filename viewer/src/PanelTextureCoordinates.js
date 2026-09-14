/** Scope: Project wood grain along a panel face's longest local dimension. */

import { Float32BufferAttribute, Vector3 } from "three";

const TEXTURE_SCALE_MM = 500;

export class PanelTextureCoordinates {
  applyTo(geometry, identity) {
    geometry.computeBoundingBox();
    const size = geometry.boundingBox.getSize(new Vector3()).toArray();
    const positions = geometry.getAttribute("position");
    const normals = geometry.getAttribute("normal");
    const coordinates = new Float32Array(positions.count * 2);
    const offset = this.#offset(identity);

    for (let index = 0; index < positions.count; index += 1) {
      const normal = [normals.getX(index), normals.getY(index), normals.getZ(index)].map(Math.abs);
      const perpendicular = normal.indexOf(Math.max(...normal));
      const [along, across] = [0, 1, 2].filter((axis) => axis !== perpendicular)
        .sort((left, right) => size[right] - size[left]);
      const point = [positions.getX(index), positions.getY(index), positions.getZ(index)];
      coordinates[index * 2] = point[along] / TEXTURE_SCALE_MM + offset[0];
      coordinates[index * 2 + 1] = point[across] / TEXTURE_SCALE_MM + offset[1];
    }

    geometry.setAttribute("uv", new Float32BufferAttribute(coordinates, 2));
  }

  #offset(identity) {
    let hash = 0;
    for (const character of identity) hash = (Math.imul(hash, 31) + character.charCodeAt(0)) >>> 0;
    return [(hash % 997) / 997, ((hash >>> 10) % 991) / 991];
  }
}
