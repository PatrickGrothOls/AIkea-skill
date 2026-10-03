/** Scope: Choose the intact presentation or source inspection model from fixed local routes. */

export class ReviewAssetChoice {
  constructor(manifest) {
    this.assembled = manifest.assembled;
    this.inspection = manifest.inspection;
    if (this.assembled?.baked !== true || this.inspection?.baked !== false) {
      throw new Error("A verified Blender presentation and matching inspection model are required.");
    }
    for (const asset of [this.assembled, this.inspection]) {
      if (!["/model.glb", "/inspection.glb"].includes(asset.url)) {
        throw new Error("The viewer model route is invalid.");
      }
    }
  }

  select(inspection, doorsHidden = false) {
    return !inspection.wholeAssembled || doorsHidden ? this.inspection : this.assembled;
  }
}
