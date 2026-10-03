/** Scope: Verify CAD depth precision, clipping safety and SSAO projection synchronization. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { Box3, Matrix4, PerspectiveCamera, Vector3 } from "three";
import { ShowcaseDepthRange } from "../showcase/ShowcaseDepthRange.js";

class DepthRangeVerification {
  constructor() {
    this.camera = new PerspectiveCamera(38, 1, 0.001, 25);
    this.occlusion = {
      ssaoMaterial: {uniforms: {cameraNear: {}, cameraFar: {},
        cameraProjectionMatrix: {value: new Matrix4()}, cameraInverseProjectionMatrix: {value: new Matrix4()}}},
      depthRenderMaterial: {uniforms: {cameraNear: {}, cameraFar: {}}},
    };
    this.range = new ShowcaseDepthRange(this.camera, this.occlusion);
    this.bounds = new Box3(new Vector3(-1.3, -1.3, -0.3), new Vector3(1.3, 1.3, 0.3));
  }

  verify() {
    for (const position of [[0, 0, 8], [8, 2, 0], [0, 0, 0.06], [0, 0, 25]]) {
      this.camera.position.set(...position);
      this.camera.lookAt(0, 0, 0);
      this.camera.updateMatrixWorld(true);
      this.range.update(this.bounds);
      assert.ok(this.camera.near >= 0.005);
      for (const x of [-1.3, 1.3]) for (const y of [-1.3, 1.3]) for (const z of [-0.3, 0.3]) {
        const depth = -new Vector3(x, y, z).applyMatrix4(this.camera.matrixWorldInverse).z;
        // Points behind the camera cannot be preserved by any positive near plane.
        if (depth > 0.005) assert.ok(depth > this.camera.near && depth < this.camera.far);
      }
      for (const material of [this.occlusion.ssaoMaterial, this.occlusion.depthRenderMaterial]) {
        assert.equal(material.uniforms.cameraNear.value, this.camera.near);
        assert.equal(material.uniforms.cameraFar.value, this.camera.far);
      }
      assert.deepEqual(this.occlusion.ssaoMaterial.uniforms.cameraProjectionMatrix.value, this.camera.projectionMatrix);
      assert.deepEqual(this.occlusion.ssaoMaterial.uniforms.cameraInverseProjectionMatrix.value, this.camera.projectionMatrixInverse);
      assert.ok(Math.abs(this.occlusion.minDistance * (this.camera.far - this.camera.near) - 0.00005) < 1e-12);
    }
    this.camera.position.set(0, 0, 8);
    this.camera.lookAt(0, 0, 0);
    this.camera.updateMatrixWorld(true);
    this.range.update(this.bounds);
    const front = new Vector3(0, 0, 0).project(this.camera).z;
    const adjacent = new Vector3(0, 0, 0.0001).project(this.camera).z;
    assert.ok(Math.abs(front - adjacent) / 2 * (2 ** 24 - 1) > 10,
      "Surfaces 0.1 mm apart must occupy distinct depth values at overview distance");
  }
}

// node:test requires a callback; one fixture owns all camera and shader-state checks.
test("showcase keeps fine CAD depth distinct without clipping overview or close-up views", () => {
  new DepthRangeVerification().verify();
});
