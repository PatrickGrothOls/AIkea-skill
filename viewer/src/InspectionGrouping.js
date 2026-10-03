/** Scope: Choose separation groups while preserving hardware mounted beneath panel identities. */

import { ReviewInspectionPath } from "./ReviewInspectionPath.js";

export class InspectionGrouping {
  constructor(records) {
    this.panels = records.filter((record) => record.kind === "panel")
      .sort((first, second) => second.path.length - first.path.length);
  }

  key(record, depth, detail) {
    if (detail === "panels") {
      const owner = this.panels.find((panel) => panel.path.length > depth
        && panel.path.every((segment, index) => record.path[index] === segment));
      if (owner) return ReviewInspectionPath.key(owner.path);
    }
    return ReviewInspectionPath.key(record.path.slice(0, depth + 1));
  }
}
