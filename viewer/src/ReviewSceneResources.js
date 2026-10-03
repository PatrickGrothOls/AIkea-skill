/** Scope: Release each model's GPU buffers, materials and decoded textures once. */

export class ReviewSceneResources {
  constructor() {
    this.resources = new Set();
    this.images = new Set();
  }

  track(root, sharedTextures = []) {
    root.traverse((node) => {
      if (!node.isMesh) return;
      this.resources.add(node.geometry);
      for (const material of [node.material].flat()) {
        this.resources.add(material);
        for (const value of Object.values(material)) {
          if (!value?.isTexture || sharedTextures.includes(value)) continue;
          this.resources.add(value);
          if (typeof value.image?.close === "function") this.images.add(value.image);
        }
      }
    });
  }

  dispose() {
    for (const resource of this.resources) resource.dispose();
    for (const image of this.images) image.close();
    this.resources.clear();
    this.images.clear();
  }
}
