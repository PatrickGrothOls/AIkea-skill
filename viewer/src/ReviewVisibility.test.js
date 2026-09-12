/** Scope: Verify hidden parts cannot intercept detail zoom when an assembly is isolated. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshBasicMaterial, PerspectiveCamera, Vector2 } from "three";
import { FixedPivotCameraControls } from "./FixedPivotCameraControls.js";

class ZoomScene {
  constructor(withHiddenGroup) {
    const root = new Group();
    root.add(new Mesh(new BoxGeometry(20, 20, 20), new MeshBasicMaterial()));
    if (withHiddenGroup) {
      const hidden = new Group();
      hidden.visible = false;
      hidden.position.z = 70;
      hidden.add(new Mesh(new BoxGeometry(20, 20, 20), new MeshBasicMaterial()));
      root.add(hidden);
    }
    this.camera = new PerspectiveCamera(50, 1, 0.1, 1000);
    this.camera.position.set(0, 0, 100);
    this.camera.lookAt(0, 0, 0);
    this.controls = new FixedPivotCameraControls(this.camera, 100);
    this.controls.setModelRoot(root);
  }
}

test("zoom ignores parts below a hidden assembly ancestor", () => {
  const isolated = new ZoomScene(true);
  const visibleOnly = new ZoomScene(false);
  for (const scene of [isolated, visibleOnly]) {
    assert.equal(scene.controls.zoomTowardPointer(new Vector2(0, 0), -100), true);
  }
  assert.deepEqual(isolated.camera.position.toArray(), visibleOnly.camera.position.toArray());
});
