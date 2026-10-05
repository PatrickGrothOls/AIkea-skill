/** Scope: Verify retained meshes, failure recovery, cancellation and motion accessibility. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { BoxGeometry, Group, Mesh, MeshStandardMaterial } from "three";
import { LiveBuildScene } from "./LiveBuildScene.js";

class FixtureLoader {
  async load(url) {
    if (url === "fail") throw new Error("missing asset");
    this.scene = new Group();
    this.scene.add(new Mesh(new BoxGeometry(), new MeshStandardMaterial()));
    return { scene: this.scene };
  }
  dispose() { this.disposed = true; }
}

test("only changed parts load; failed revisions retain all existing geometry", async () => {
  const loaders = [];
  const scene = new LiveBuildScene(true, () => { const loader = new FixtureLoader(); loaders.push(loader); return loader; });
  const first = { id: "panel", hash: "one", url: "one", owner: "root/cabinet" };
  await scene.apply({ parts: [first] });
  const mesh = scene.entries.get("panel").scene;
  await scene.apply({ parts: [first] });
  assert.equal(loaders.length, 1);
  await assert.rejects(scene.apply({ parts: [{ ...first, hash: "two", url: "fail" }] }));
  assert.equal(scene.entries.get("panel").scene, mesh);
  assert.equal(loaders[0].disposed, undefined);
  assert.equal(loaders[1].disposed, true);
  scene.active = "root";
  scene.running = true;
  scene.update(0.1, 1);
  assert.equal(scene.entries.get("panel").surface.uniforms.liveStrength.value, 0);
  await scene.apply({ parts: [] });
  assert.equal(loaders[0].disposed, true);
  assert.equal(scene.root.children.length, 0);
  scene.dispose();
});

test("a late asset cannot overwrite a newer scene or reappear after disposal", async () => {
  let release;
  class DelayedLoader extends FixtureLoader {
    async load(url) {
      if (url === "slow") await new Promise((resolve) => { release = resolve; });
      return super.load(url);
    }
  }
  const scene = new LiveBuildScene(true, () => new DelayedLoader());
  const slow = scene.apply({ parts: [{ id: "old", hash: "old", url: "slow" }] });
  await scene.apply({ parts: [{ id: "new", hash: "new", url: "new" }] });
  release();
  assert.equal(await slow, false);
  assert.deepEqual([...scene.entries.keys()], ["new"]);
  const pending = scene.apply({ parts: [{ id: "late", hash: "late", url: "slow" }] });
  scene.dispose();
  release();
  assert.equal(await pending, false);
  assert.equal(scene.root.children.length, 0);
});

test("shimmer stops on failure and does not affect other assemblies", async () => {
  const scene = new LiveBuildScene(false, () => new FixtureLoader());
  await scene.apply({ parts: ["base", "cabinet"].map((id) => ({ id, owner: `root/${id}`, hash: id, url: id })) });
  scene.active = "root/cabinet";
  scene.running = true;
  scene.update(1, 1);
  assert.equal(scene.entries.get("base").surface.uniforms.liveStrength.value, 0);
  assert.equal(scene.entries.get("cabinet").surface.uniforms.liveStrength.value, 0.6);
  scene.running = false;
  scene.update(1, 2);
  assert.equal(scene.entries.get("cabinet").surface.uniforms.liveStrength.value, 0);
  assert.equal(scene.entries.get("cabinet").surface.materials[0].opacity, 1);
  scene.dispose();
});

test("graphics preparation completes before replacement and failures keep the previous model", async () => {
  const scene = new LiveBuildScene(false, () => new FixtureLoader());
  const part = { id: "panel", hash: "one", url: "one" };
  await scene.apply({ parts: [part] });
  const original = scene.entries.get("panel").scene;
  let release;
  const pending = scene.apply({ parts: [{ ...part, hash: "two" }] },
    () => new Promise((resolve) => { release = resolve; }));
  await Promise.resolve();
  assert.equal(scene.entries.get("panel").scene, original);
  release();
  await pending;
  const replacement = scene.entries.get("panel").scene;
  assert.notEqual(replacement, original);
  await assert.rejects(scene.apply({ parts: [{ ...part, hash: "three" }] },
    async () => { throw new Error("graphics preparation failed"); }));
  assert.equal(scene.entries.get("panel").scene, replacement);
  scene.dispose();
});
