/** Scope: Fetch one abortable GLB without a persistent loader cache and own its resources. */

import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { ReviewSceneResources } from "./ReviewSceneResources.js";

export class ReviewAssetLoader {
  constructor() {
    this.controller = new AbortController();
    this.resources = new ReviewSceneResources();
  }

  async load(url) {
    const response = await fetch(url, { signal: this.controller.signal, cache: "no-store" });
    if (!response.ok) throw new Error(`Model could not be loaded (${response.status}).`);
    const gltf = await new GLTFLoader().parseAsync(await response.arrayBuffer(), "/");
    this.resources.track(gltf.scene);
    if (this.controller.signal.aborted) {
      this.resources.dispose();
      return null;
    }
    return gltf;
  }

  dispose() {
    this.controller.abort();
    this.resources.dispose();
  }
}
