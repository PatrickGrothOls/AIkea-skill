/** Scope: Form a seamless photographic floor-to-wall sweep outside the CAD model. */

import { BufferGeometry, Float32BufferAttribute } from "three";

export class StudioBackdropGeometry extends BufferGeometry {
  constructor(span) {
    super();
    const profile = [[0, span * 20], [0, -span * 1.5]];
    for (let step = 1; step <= 48; step += 1) {
      const angle = step / 48 * Math.PI / 2;
      profile.push([span * (1 - Math.cos(angle)), -span * (1.5 + Math.sin(angle))]);
    }
    profile.push([span * 10, -span * 2.5]);
    const positions = profile.flatMap(([height, depth]) => [
      -span * 20, height, depth, span * 20, height, depth,
    ]);
    const triangles = [];
    for (let row = 0; row < profile.length - 1; row += 1) {
      const first = row * 2;
      triangles.push(first, first + 1, first + 2, first + 1, first + 3, first + 2);
    }
    this.setAttribute("position", new Float32BufferAttribute(positions, 3));
    this.setIndex(triangles);
    this.computeVertexNormals();
  }
}
