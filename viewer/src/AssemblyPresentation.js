/** Scope: Keep original mesh transforms and apply hierarchical inspection poses to a cloned GLB scene. */

import { Box3, Vector3 } from "three";
import { ExplodedGroupLayout } from "./ExplodedGroupLayout.js";
import { ReviewVisibility } from "./ReviewVisibility.js";
import { ReviewPartCatalog } from "./ReviewPartCatalog.js";

export class AssemblyPresentation {
  constructor(sourceScene, associations) {
    this.catalog = new ReviewPartCatalog(sourceScene, associations);
    this.scene = this.catalog.scene;
    this.records = [];
    for (const { node, name } of this.catalog.parts) {
      this.records.push({
        node, name, path: name.split("__"),
        position: node.position.clone(),
        worldOrigin: new Vector3().setFromMatrixPosition(node.matrixWorld),
        parentInverse: node.parent.matrixWorld.clone().invert(),
        bounds: new Box3().setFromObject(node),
        visible: ReviewVisibility.isVisible(node), originalVisibility: node.visible,
      });
    }
    this.layout = new ExplodedGroupLayout();
  }

  get scopes() {
    const scopes = new Set();
    for (const record of this.records.filter((part) => part.visible)) {
      for (let depth = 1; depth < record.path.length; depth += 1) {
        scopes.add(record.path.slice(0, depth).join("__"));
      }
    }
    return [...scopes].sort();
  }

  groups(scope) {
    const depth = scope === "" ? 0 : scope.split("__").length;
    const groups = new Map();
    for (const record of this.records) {
      if (!record.visible || (scope !== "" && !record.name.startsWith(`${scope}__`))) continue;
      const key = record.path.slice(0, depth + 1).join("__");
      const group = groups.get(key) ?? { key, records: [], bounds: new Box3() };
      group.records.push(record);
      group.bounds.union(record.bounds);
      groups.set(key, group);
    }
    return [...groups.values()];
  }

  apply(scope, amount) {
    for (const record of this.records) {
      record.node.position.copy(record.position);
      record.node.visible = scope === "" && amount === 0 ? record.originalVisibility : false;
    }
    const groups = this.groups(scope);
    const offsets = this.layout.offsets(groups, amount);
    const bounds = new Box3();
    let visibleCount = 0;
    for (const group of groups) {
      const offset = offsets.get(group.key);
      bounds.union(group.bounds.clone().translate(offset));
      for (const record of group.records) {
        record.node.visible = true;
        if (amount !== 0) {
          record.node.position.copy(record.worldOrigin).add(offset).applyMatrix4(record.parentInverse);
        }
        visibleCount += 1;
      }
    }
    this.scene.updateMatrixWorld(true);
    return { bounds, visibleCount, groupCount: groups.length };
  }
}
