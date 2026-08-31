/** Scope: Resolve the requested review title, camera direction, and framing axes. */

export class ReviewView {
  static fromSearch(search) {
    const query = new URLSearchParams(search);
    const view = query.get("view") ?? "perspective";
    return new ReviewView(
      view,
      query.get("title") ?? "Your first cabinet",
      query.get("render") ?? (view === "perspective" ? "photo" : "interactive"),
      query.get("lighting") !== "off",
      query.get("framing") === "close" ? 0.72 : 1,
    );
  }

  constructor(view, title, renderMode, lightingEnabled, framingScale) {
    this.view = ["top", "bottom", "structure"].includes(view)
      ? view
      : "perspective";
    this.title = title;
    this.renderMode = renderMode === "photo" ? "photo" : "interactive";
    this.lightingEnabled = lightingEnabled;
    this.framingScale = framingScale;
  }

  cameraDirection() {
    if (this.view === "top") {
      return [0, 1, 0];
    }
    if (this.view === "bottom") {
      return [0, -1, 0];
    }
    if (this.view === "structure") {
      return [1, -0.35, 1];
    }
    return [1, 0.45, 1];
  }

  cameraUp() {
    return ["perspective", "structure"].includes(this.view)
      ? [0, 1, 0]
      : [0, 0, -1];
  }

  showsStudioFloor() {
    return this.view === "perspective";
  }

  usesPhotoRenderer() {
    return this.renderMode === "photo";
  }

  showsLighting() {
    return this.lightingEnabled;
  }

  frameDimensions(size) {
    if (["perspective", "structure"].includes(this.view)) {
      return { horizontal: size.x, vertical: size.y, depth: size.z };
    }
    return { horizontal: size.x, vertical: size.z, depth: size.y };
  }

  cameraDistance(size, verticalFov, horizontalFov) {
    if (this.view === "perspective") {
      const radius = Math.hypot(size.x, size.y, size.z) / 2;
      return radius / Math.sin(Math.min(verticalFov, horizontalFov) / 2)
        * 1.08 * this.framingScale;
    }
    const frame = this.frameDimensions(size);
    return Math.max(
      frame.vertical / (2 * Math.tan(verticalFov / 2)),
      frame.horizontal / (2 * Math.tan(horizontalFov / 2)),
      frame.depth,
    ) * 1.35 * this.framingScale;
  }

  guidance() {
    if (this.usesPhotoRenderer()) {
      return "Drag to rotate, scroll to inspect, or hold Shift while scrolling or dragging to pan. "
        + "Leave it still for a moment while the image sharpens.";
    }
    return {
      top: "Looking down through the deck across both CNC-sized base modules.",
      bottom: "Looking up at the rails, braces, and the join between the modules.",
      structure: "The deck, front and back rails, braces, and both CNC-sized modules.",
    }[this.view]
      ?? "Drag to rotate, scroll to inspect, or hold Shift while scrolling or dragging to pan.";
  }
}
