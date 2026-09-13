/** Scope: Prevent an exploded view from separating the rendering faces of a physical panel. */

import assert from "node:assert/strict";
import test from "node:test";
import { BoxGeometry, Group, Mesh, MeshBasicMaterial } from "three";
import { AssemblyPresentation } from "./AssemblyPresentation.js";

test("a mesh-bearing GLTF node is one part even when it has multiple primitive meshes", () => {
  const scene = new Group();
  const panel = new Group();
  panel.name = "drawer__side";
  scene.add(panel);
  const associations = new Map([[panel, { nodes: 1, meshes: 0 }]]);
  for (let index = 0; index < 3; index += 1) {
    const face = new Mesh(new BoxGeometry(10, 20, 2), new MeshBasicMaterial());
    face.name = `drawer__side_${index}`;
    face.position.z = index * 2;
    panel.add(face);
    associations.set(face, { meshes: 0, primitives: index });
  }
  const model = new AssemblyPresentation(scene, associations);
  assert.equal(model.apply("drawer", .8).visibleCount, 1);
  assert.equal(model.records.length, 1);
  const copy = model.records[0].node;
  assert.deepEqual(copy.children.map((node) => node.position.z), [0, 2, 4]);
  assert.equal(model.catalog.nameFor(copy.children[1]), "drawer__side");
  assert.deepEqual(model.scopes, ["drawer", "drawer__side"]);
  assert.equal(model.apply(model.scopeForPart("drawer__side"), 3).visibleCount, 1);
  assert.deepEqual(copy.children.map((node) => node.position.z), [0, 2, 4]);
  model.apply("", 0);
  assert.deepEqual(copy.position.toArray(), panel.position.toArray());
});
