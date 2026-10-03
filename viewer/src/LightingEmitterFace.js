/** Scope: Locate the local +Z emitting face in split or consolidated CAD emitter geometry. */
import { Box3, Vector3 } from "three";

export class LightingEmitterFace {
  static bounds(geometry) {
    const positions = geometry.getAttribute("position");
    const normals = geometry.getAttribute("normal");
    const bounds = new Box3();
    const point = new Vector3();
    for (let index = 0; index < positions.count; index += 1) {
      if (normals.getZ(index) > 0.999) {
        bounds.expandByPoint(point.fromBufferAttribute(positions, index));
      }
    }
    return bounds;
  }
}
