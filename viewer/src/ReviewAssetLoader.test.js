/** Scope: Verify embedded baked textures load when the host rejects blob fetches. */

import test from "node:test";
import assert from "node:assert/strict";
import { ReviewAssetLoader } from "./ReviewAssetLoader.js";

class DecodedImage {
  constructor() {
    this.listeners = new Map();
    this.width = 1;
    this.height = 1;
  }
  addEventListener(name, callback) { this.listeners.set(name, callback); }
  removeEventListener(name) { this.listeners.delete(name); }
  set src(value) {
    assert.match(value, /^blob:/);
    queueMicrotask(() => this.listeners.get("load")?.call(this));
  }
}

// The test runner requires a callback; this exercises the real GLTF parser.
test("embedded lighting survives a host that rejects blob fetch", async () => {
  const original = {
    fetch: globalThis.fetch, document: globalThis.document,
    self: globalThis.self, createImageBitmap: globalThis.createImageBitmap,
  };
  const data = new Uint8Array(48);
  new Float32Array(data.buffer, 0, 9).set([0, 0, 0, 1, 0, 0, 0, 1, 0]);
  const document = {
    asset: { version: "2.0" }, scene: 0, scenes: [{ nodes: [0] }],
    nodes: [{ mesh: 0 }],
    meshes: [{ primitives: [{ attributes: { POSITION: 0 }, material: 0 }] }],
    accessors: [{ bufferView: 0, componentType: 5126, count: 3,
      type: "VEC3", min: [0, 0, 0], max: [1, 1, 0] }],
    buffers: [{ byteLength: 48 }],
    bufferViews: [{ buffer: 0, byteOffset: 0, byteLength: 36 },
      { buffer: 0, byteOffset: 36, byteLength: 12 }],
    images: [{ bufferView: 1, mimeType: "image/png" }],
    textures: [{ source: 0 }],
    materials: [{ emissiveFactor: [1, 1, 1],
      emissiveTexture: { index: 0, texCoord: 1 } }],
  };
  const json = Buffer.from(JSON.stringify(document).padEnd(
    Math.ceil(JSON.stringify(document).length / 4) * 4, " "));
  const glb = Buffer.alloc(28 + json.length + data.length);
  [0x46546c67, 2, glb.length, json.length, 0x4e4f534a]
    .forEach((value, i) => glb.writeUInt32LE(value, i * 4));
  json.copy(glb, 20);
  glb.writeUInt32LE(data.length, 20 + json.length);
  glb.writeUInt32LE(0x004e4942, 24 + json.length);
  glb.set(data, 28 + json.length);
  const requests = [];
  const loader = new ReviewAssetLoader();
  try {
    globalThis.self = globalThis;
    globalThis.document = { createElementNS: () => new DecodedImage() };
    globalThis.createImageBitmap = async () => { throw new Error("unexpected bitmap path"); };
    globalThis.fetch = async (url) => {
      requests.push(url);
      if (url.startsWith("blob:")) throw new TypeError("Failed to fetch");
      return new Response(glb);
    };
    const result = await loader.load("/model.glb");
    const texture = result.scene.children[0].material.emissiveMap;
    assert.ok(texture, "baked lighting must not silently disappear");
    assert.equal(texture.channel, 1);
    assert.equal(texture.flipY, false);
    assert.deepEqual(requests, ["/model.glb"]);
  } finally {
    loader.dispose();
    Object.assign(globalThis, original);
  }
});
