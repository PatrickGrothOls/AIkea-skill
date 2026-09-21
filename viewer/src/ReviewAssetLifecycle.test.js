/** Scope: Verify pose-based asset selection and disposal of shared model resources. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial, Texture } from "three";
import { ExplodedViewState } from "./ExplodedViewState.js";
import { ReviewAssetChoice } from "./ReviewAssetChoice.js";
import { ReviewSceneResources } from "./ReviewSceneResources.js";

// Pure fixtures exercise the policy with real Three.js resources and no WebGL context.
test("assembled restores the bake; separated or isolated panels use the source material asset", () => {
  const manifest = { assembled: { url: "/model.glb", baked: true },
    inspection: { url: "/inspection.glb", baked: false } };
  const assets = new ReviewAssetChoice(manifest);
  for (const state of [new ExplodedViewState(1), new ExplodedViewState(0, "cabinet")]) {
    assert.equal(assets.select(state), manifest.inspection);
  }
  assert.equal(assets.select(new ExplodedViewState()), manifest.assembled);
  assert.throws(() => new ReviewAssetChoice({ ...manifest, inspection: null }), /Blender/);
  assert.throws(() => new ReviewAssetChoice({ ...manifest, assembled: { url: "/model.glb", baked: false } }), /Blender/);
  assert.throws(() => new ReviewAssetChoice({ assembled: { url: "https://untrusted.invalid/model" } }));
});

// Event counts catch double disposal and preserve the explicitly shared fallback maps.
test("release all model buffers and decoded images once while keeping shared studio textures", () => {
  const geometry = new BoxGeometry();
  let closed = 0;
  const texture = new Texture({ close: () => { closed += 1; } });
  const shared = new Texture();
  const material = new MeshStandardMaterial({ map: texture, normalMap: shared });
  const root = new Group();
  root.add(new Mesh(geometry, material), new Mesh(geometry, material));
  const counts = new Map();
  for (const item of [geometry, material, texture, shared]) {
    counts.set(item, 0);
    item.addEventListener("dispose", () => counts.set(item, counts.get(item) + 1));
  }
  const resources = new ReviewSceneResources();
  resources.track(root, [shared]);
  resources.track(root.clone(true), [shared]);
  resources.dispose();
  resources.dispose();
  assert.deepEqual([...counts.values()], [1, 1, 1, 0]);
  assert.equal(closed, 1);
});
