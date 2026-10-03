/** Scope: Encode structured inspection paths without confusing IDs with hierarchy separators. */

export class ReviewInspectionPath {
  static key(path) {
    return path.map((segment) => encodeURIComponent(segment).replaceAll("_", "%5F")).join("__");
  }

  static segments(key) {
    return key === "" ? [] : key.split("__").map((segment) => decodeURIComponent(segment));
  }

  static label(key) {
    return this.segments(key).map((segment) => segment.replaceAll("_", " ")).join(" / ");
  }
}
