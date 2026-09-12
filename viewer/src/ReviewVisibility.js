/** Scope: Exclude meshes hidden directly or through an ancestor from inspection and picking. */

export class ReviewVisibility {
  static isVisible(object) {
    for (let node = object; node; node = node.parent) {
      if (!node.visible) return false;
    }
    return true;
  }
}
