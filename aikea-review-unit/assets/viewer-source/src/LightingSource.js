/** Scope: Derive one Three.js area-light placement from an exported emitter mesh. */

import { Vector3 } from "three";

const LIGHT_SOURCE_PREFIX = "light_source__";
const RECESSED_LIGHT_REVIEW_INTENSITY = 1800;

export class LightingSource {
  static collect(root) {
    const candidates = new Map();
    root.traverse((node) => {
      if (node.isMesh && node.name.startsWith(LIGHT_SOURCE_PREFIX)) {
        const candidate = new LightingSource(node);
        if (!candidate.isEmitterFace()) {
          return;
        }
        const sourceId = candidate.sourceId();
        const current = candidates.get(sourceId);
        if (!current || candidate.faceHeight() > current.faceHeight()) {
          candidates.set(sourceId, candidate);
        }
      }
    });
    return [...candidates.values()].map((candidate) => candidate.describe());
  }

  constructor(mesh) {
    this.mesh = mesh;
  }

  sourceId() {
    return this.mesh.name.replace(/_part_\d+$/, "");
  }

  isEmitterFace() {
    const size = this.#bounds().getSize(new Vector3());
    return size.x > 0.01 && size.y > 0.01 && size.z < 0.01;
  }

  faceHeight() {
    return this.#bounds().getCenter(new Vector3()).z;
  }

  describe() {
    const geometry = this.mesh.geometry;
    const bounds = this.#bounds();
    const center = bounds.getCenter(new Vector3());
    const size = bounds.getSize(new Vector3());
    const outwardDistance = Math.max(size.x, size.y) * 0.1;
    const position = this.mesh.localToWorld(
      new Vector3(center.x, center.y, bounds.max.z + 0.5),
    );
    const target = this.mesh.localToWorld(
      new Vector3(center.x, center.y, bounds.max.z + outwardDistance),
    );
    const upPoint = this.mesh.localToWorld(
      new Vector3(center.x, center.y + 1, bounds.max.z + 0.5),
    );
    const material = [this.mesh.material].flat()[0];
    return {
      color: `#${material.color.getHexString()}`,
      height: size.y,
      intensity: RECESSED_LIGHT_REVIEW_INTENSITY,
      name: this.sourceId(),
      position: position.toArray(),
      target: target.toArray(),
      up: upPoint.sub(position).normalize().toArray(),
      width: size.x,
    };
  }

  #bounds() {
    this.mesh.geometry.computeBoundingBox();
    return this.mesh.geometry.boundingBox;
  }
}

export { LIGHT_SOURCE_PREFIX };
