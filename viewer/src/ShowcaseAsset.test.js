/** Scope: Verify the shipped machined asset and its shared inspection transitions. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { gunzipSync } from "node:zlib";
import { createHash } from "node:crypto";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { AssemblyPresentation } from "./AssemblyPresentation.js";

class ShowcaseAssetVerification {
  async verify() {
    const metadata = JSON.parse(readFileSync(new URL("../showcase/model-info.json", import.meta.url)));
    const compressed = readFileSync(new URL("../showcase/wardrobe.glb.gz", import.meta.url));
    const bytes = gunzipSync(compressed);
    assert.equal(compressed.length, metadata.compressed_bytes);
    assert.equal(bytes.length, metadata.uncompressed_bytes);
    assert.equal(createHash("sha256").update(bytes).digest("hex"), metadata.model_sha256);
    const model = await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), "");
    model.scene.scale.setScalar(0.001);
    model.scene.updateMatrixWorld(true);
    const presentation = new AssemblyPresentation(model.scene, model.parser.associations);
    assert.equal(presentation.records.length, 84);
    assert.ok(presentation.records.every(part => part.kind === "panel"));
    let triangles = 0;
    model.scene.traverse(node => {
      if (node.isMesh) triangles += node.geometry.index.count / 3;
    });
    assert.equal(triangles, 775824);
    assert.equal(presentation.apply("", 0, "panels", true).visibleCount, 80);
    const positions = presentation.records.map(part => part.node.position.clone());
    presentation.apply("", 0.14, "panels", true);
    assert.ok(presentation.records.some((part, i) => !part.node.position.equals(positions[i])));
    const scope = presentation.scopeForPart("cabinet_01__door_panel");
    assert.equal(presentation.apply(scope, 0, "panels", false).visibleCount, 1);
    assert.equal(presentation.apply("", 0, "panels", false).visibleCount, 84);
    assert.ok(presentation.records.every((part, i) => part.node.position.equals(positions[i])));
  }
}

// A callback is the node:test registration contract; the verification belongs to one fixture.
test("public CAD retains all machined panels and restores assembly after inspection", async () => {
  await new ShowcaseAssetVerification().verify();
});
