/** Scope: Verify the shipped machined asset and its shared inspection transitions. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { gunzipSync } from "node:zlib";
import { createHash } from "node:crypto";
import { Vector3 } from "three";
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
    assert.equal(presentation.records.length, 612);
    assert.equal(presentation.records.filter(part => part.kind === "panel").length, 84);
    assert.equal(presentation.records.filter(part => part.kind === "hardware").length, 507);
    assert.equal(metadata.vendor_components_excluded, 134);
    assert.equal(metadata.excluded_hardware.product, "Cabineo");
    assert.ok(presentation.records.every(part => !part.name.endsWith("_connector")), "Cabineo bodies must be absent");
    assert.equal(presentation.records.filter(part => part.name.endsWith("_insert")).length, 134);
    assert.equal(presentation.records.filter(part => part.kind === "door_frame").length, 17);
    assert.equal(presentation.records.filter(part => part.kind === "door_handle").length, 4);
    assert.equal(metadata.source_hardware_components, 507);
    let triangles = 0;
    model.scene.traverse(node => {
      if (node.isMesh) triangles += node.geometry.index.count / 3;
    });
    assert.equal(triangles, 1678580);
    assert.equal(presentation.apply("", 0, "panels", false).visibleCount, 612);
    const positions = presentation.records.map(part => part.node.position.clone());
    const originalWorld = new Map(presentation.records.map(part => [part.name, part.node.getWorldPosition(new Vector3())]));
    presentation.apply("", 0.14, "panels", false);
    for (const part of presentation.records.filter(part => ["hardware", "door_frame", "door_handle"].includes(part.kind))) {
      const owner = presentation.records.find(panel => panel.kind === "panel"
        && JSON.stringify(panel.path) === JSON.stringify(part.path.slice(0, -1)));
      assert.ok(owner, `Missing mounting panel for ${part.name}`);
      const movement = part.node.getWorldPosition(new Vector3()).sub(originalWorld.get(part.name));
      const ownerMovement = owner.node.getWorldPosition(new Vector3()).sub(originalWorld.get(owner.name));
      assert.ok(movement.distanceTo(ownerMovement) < 1e-8, `Detached fitting: ${part.name}`);
    }
    assert.ok(presentation.records.some((part, i) => !part.node.position.equals(positions[i])));
    const scope = presentation.scopeForPart("cabinet_01__door_panel");
    assert.ok(presentation.apply(scope, 0, "panels", false).visibleCount > 1);
    assert.equal(presentation.apply("", 0, "panels", false).visibleCount, 612);
    assert.ok(presentation.records.every((part, i) => part.node.position.equals(positions[i])));
  }
}

// A callback is the node:test registration contract; the verification belongs to one fixture.
test("public CAD retains machined panels and hardware with verified explosion attachments", async () => {
  await new ShowcaseAssetVerification().verify();
});
