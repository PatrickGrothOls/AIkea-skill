/** Scope: Reuse one bounded closed-assembly photo renderer across inspection states. */

import { Vector2 } from "three";
import { WebGLPathTracer } from "three-gpu-pathtracer";

const MAX_PHOTO_PIXELS = 750_000;
const SAMPLE_LIMIT = 512;

export class PhotoRenderSession {
  constructor(renderer, scene, camera, controls, PathTracer = WebGLPathTracer) {
    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    this.controls = controls;
    this.PathTracer = PathTracer;
    this.size = new Vector2();
    this.tracer = null;
    this.active = false;
    // Camera gestures reset accumulation without rebuilding the assembly snapshot.
    this.cameraChanged = () => this.tracer.updateCamera();
  }

  #initialize() {
    this.tracer = new this.PathTracer(this.renderer);
    this.tracer.bounces = 4;
    this.tracer.filterGlossyFactor = 0.5;
    this.tracer.dynamicLowRes = false;
    this.tracer.rasterizeScene = true;
    this.tracer.renderDelay = 350;
    this.tracer.minSamples = 16;
    this.tracer.fadeDuration = 350;
    this.tracer.tiles.set(3, 3);
    this.#limitResolution();
    this.tracer.setScene(this.scene, this.camera);
    this.controls?.addEventListener("change", this.cameraChanged);
  }

  render(enabled, hidden) {
    if (!enabled || hidden) {
      this.active = false;
      return;
    }
    if (this.tracer === null) this.#initialize();
    if (!this.active) this.tracer.updateCamera();
    this.active = true;
    this.#limitResolution();
    // Keep presenting the settled image while stopping expensive sample accumulation.
    this.tracer.pausePathTracing = this.tracer.samples >= SAMPLE_LIMIT;
    this.tracer.renderSample();
    this.renderer.domElement.dataset.photoSamples = String(Math.floor(this.tracer.samples));
  }

  #limitResolution() {
    const { x: previousWidth, y: previousHeight } = this.size;
    this.renderer.getDrawingBufferSize(this.size);
    this.tracer.renderScale = Math.min(1, Math.sqrt(MAX_PHOTO_PIXELS / (this.size.x * this.size.y)));
    if (previousWidth !== this.size.x || previousHeight !== this.size.y) this.tracer.reset();
  }

  dispose() {
    this.controls?.removeEventListener("change", this.cameraChanged);
    this.tracer?.dispose();
    delete this.renderer.domElement.dataset.photoSamples;
  }
}
