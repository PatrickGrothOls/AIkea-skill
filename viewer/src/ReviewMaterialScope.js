/** Scope: Preserve source materials on purchased hardware, lighting and review guides. */

export class ReviewMaterialScope {
  static preservesSource(mesh) {
    return mesh.name.startsWith("review_only__")
      || mesh.name.includes("__source_cad")
      || mesh.name.startsWith("purchased_light__")
      || mesh.name.startsWith("light_source__");
  }
}
