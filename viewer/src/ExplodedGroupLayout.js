/** Scope: Separate original group bounds for readable inspection, without claiming removal paths. */

import { Box3, Vector3 } from "three";

export class ExplodedGroupLayout {
  offsets(groups, amount) {
    const bounds = new Box3();
    for (const group of groups) bounds.union(group.bounds);
    const size = bounds.getSize(new Vector3());
    const center = bounds.getCenter(new Vector3());
    const span = Math.max(size.x, size.y, size.z);
    const faces = groups.map((group) => ({ group, ...this.nearestFace(group, bounds) }));
    const layers = new Map();
    for (const face of faces) {
      const key = `${face.axis}:${face.sign}`;
      const gaps = layers.get(key) ?? new Set();
      gaps.add(face.gap);
      layers.set(key, gaps);
    }
    return new Map(faces.map(({ group, axis, sign, gap }) => {
      const gaps = [...layers.get(`${axis}:${sign}`)].sort((a, b) => a - b);
      const layer = gaps.length - gaps.indexOf(gap);
      const offset = new Vector3();
      offset[axis] = sign * amount * layer * Math.max(size[axis] * 0.35, span * 0.12);
      // Extra spacing separates stacked groups that share the same outward face.
      offset.add(group.bounds.getCenter(new Vector3()).sub(center).multiplyScalar(Math.max(0, amount - 1)));
      return [group.key, offset];
    }));
  }

  nearestFace(group, bounds) {
    const size = group.bounds.getSize(new Vector3());
    const axes = ["x", "y", "z"];
    const candidates = group.records.length === 1
      ? [axes.reduce((smallest, axis) => size[axis] < size[smallest] ? axis : smallest)]
      : axes;
    const faces = candidates.flatMap((axis) => [
      { axis, sign: -1, gap: group.bounds.min[axis] - bounds.min[axis] },
      { axis, sign: 1, gap: bounds.max[axis] - group.bounds.max[axis] },
    ]);
    const face = faces.reduce((nearest, candidate) => candidate.gap < nearest.gap ? candidate : nearest);
    return { ...face, gap: Math.round(face.gap * 10000) / 10000 };
  }
}
