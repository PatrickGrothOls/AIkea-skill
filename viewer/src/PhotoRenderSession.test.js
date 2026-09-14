/** Scope: Regress photo/inspection allocation, resumption, render limits, and teardown. */

import assert from "node:assert/strict";
import test from "node:test";
import { EventDispatcher, Vector2 } from "three";
import { PhotoRenderSession } from "./PhotoRenderSession.js";

class TracerProbe {
  constructor(renderer) {
    renderer.allocations.push(this);
    this.samples = 0;
    this.sceneBuilds = 0;
    this.frames = 0;
    this.disposals = 0;
    this.tiles = new Vector2();
  }
  setScene(scene, camera) {
    this.scene = scene;
    this.camera = camera;
    this.sceneBuilds += 1;
  }
  updateCamera() { this.reset(); }
  reset() { this.samples = 0; }
  renderSample() {
    this.frames += 1;
    if (!this.pausePathTracing) this.samples += 1;
  }
  dispose() { this.disposals += 1; }
}

class PhotoHarness {
  constructor() {
    this.allocations = [];
    this.size = new Vector2(800, 600);
    this.domElement = { dataset: {} };
    this.controls = new EventDispatcher();
    this.session = new PhotoRenderSession(this, {}, {}, this.controls, TracerProbe);
  }
  getDrawingBufferSize(target) { return target.copy(this.size); }
  settle() {
    for (let frame = 0; frame < 520; frame += 1) this.session.render(true, false);
  }
}

test("interactive and hidden starts do not allocate a photo renderer", () => {
  const h = new PhotoHarness();
  h.session.render(false, false);
  h.session.render(true, true);
  h.session.dispose();
  assert.equal(h.allocations.length, 0);
});

test("repeated drawer inspection reuses one scene build and resumes the image", () => {
  const h = new PhotoHarness();
  h.settle();
  const tracer = h.allocations[0];
  for (let cycle = 0; cycle < 10; cycle += 1) {
    const frames = tracer.frames;
    h.session.render(false, false);
    assert.equal(tracer.frames, frames);
    h.session.render(true, false);
    assert.equal(tracer.samples, 1);
    h.settle();
  }
  assert.equal(h.allocations.length, 1);
  assert.equal(tracer.sceneBuilds, 1);
});

test("settled photos stop accumulating but redraw after resize and camera movement", () => {
  const h = new PhotoHarness();
  h.settle();
  const tracer = h.allocations[0];
  assert.equal(tracer.samples, 512);
  assert.equal(tracer.frames, 520);
  h.size.set(3840, 2160);
  h.session.render(true, false);
  assert.equal(tracer.samples, 1);
  assert.ok(h.size.x * h.size.y * tracer.renderScale ** 2 <= 750_001);
  h.settle();
  h.controls.dispatchEvent({ type: "change" });
  h.session.render(true, false);
  assert.equal(tracer.samples, 1);
  assert.equal(tracer.sceneBuilds, 1);
});

test("hidden tabs stop photo work and teardown releases the renderer and listener", () => {
  const h = new PhotoHarness();
  h.session.render(true, false);
  const tracer = h.allocations[0];
  h.session.render(true, true);
  assert.equal(tracer.frames, 1);
  h.session.render(true, false);
  assert.equal(tracer.samples, 1);
  h.session.dispose();
  assert.equal(tracer.disposals, 1);
  assert.equal(h.controls.hasEventListener("change", h.session.cameraChanged), false);
  assert.equal(h.domElement.dataset.photoSamples, undefined);
});
