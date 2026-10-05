/** Scope: Retain unchanged GPU assets and atomically apply the latest complete revision. */

import { Box3, Group } from "three";
import { ReviewAssetLoader } from "./ReviewAssetLoader.js";
import { LiveBuildSurface } from "./LiveBuildSurface.js";

export class LiveBuildScene {
  constructor(reducedMotion, loaderFactory = () => new ReviewAssetLoader()) {
    this.root = new Group();
    this.entries = new Map();
    this.pending = new Set();
    this.generation = 0;
    this.reducedMotion = reducedMotion;
    this.loaderFactory = loaderFactory;
    this.active = "";
    this.running = false;
  }

  async apply(revision) {
    const generation = ++this.generation;
    for (const loader of this.pending) loader.dispose();
    this.pending.clear();
    const additions = [];
    const requested = [];
    try {
      for (const part of revision.parts) {
        if (this.entries.get(part.id)?.hash === part.hash) continue;
        const loader = this.loaderFactory();
        requested.push(loader);
        this.pending.add(loader);
        const gltf = await loader.load(part.url);
        if (!gltf || generation !== this.generation) {
          loader.dispose();
          return false;
        }
        additions.push({ ...part, loader, scene: gltf.scene,
          surface: new LiveBuildSurface(gltf.scene, this.reducedMotion) });
      }
      if (generation !== this.generation) return false;
      const wanted = new Map(revision.parts.map((part) => [part.id, part.hash]));
      for (const [id, entry] of this.entries) {
        if (wanted.get(id) === entry.hash) continue;
        this.root.remove(entry.scene);
        entry.loader.dispose();
        this.entries.delete(id);
      }
      for (const entry of additions) {
        this.entries.set(entry.id, entry);
        this.root.add(entry.scene);
        this.pending.delete(entry.loader);
      }
      for (const part of revision.parts) this.entries.get(part.id).owner = part.owner;
      this.bounds = new Box3().setFromObject(this.root);
      return true;
    } finally {
      const retained = new Set([...this.entries.values()].map((entry) => entry.loader));
      for (const loader of requested) {
        if (!retained.has(loader)) {
          loader.dispose();
          this.pending.delete(loader);
        }
      }
    }
  }

  update(delta, time) {
    const activeBounds = new Box3();
    for (const entry of this.entries.values()) {
      if (this.matches(entry.owner)) activeBounds.union(entry.surface.bounds);
    }
    for (const entry of this.entries.values()) {
      entry.surface.update(delta, time, this.running && this.matches(entry.owner),
        activeBounds.isEmpty() ? entry.surface.bounds : activeBounds);
    }
  }

  matches(owner) {
    return Boolean(this.active) && (owner === this.active || owner.startsWith(`${this.active}/`));
  }

  arriving() {
    return [...this.entries.values()].some((entry) => entry.surface.elapsed < 0.45);
  }

  dispose() {
    ++this.generation;
    for (const loader of this.pending) loader.dispose();
    for (const entry of this.entries.values()) entry.loader.dispose();
    this.pending.clear();
    this.entries.clear();
    this.root.clear();
  }
}
