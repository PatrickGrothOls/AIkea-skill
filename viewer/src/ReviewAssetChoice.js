/** Scope: Choose the intact presentation or source inspection model from fixed local routes. */

export class ReviewAssetChoice {
  constructor(manifest) {
    this.assembled = manifest.assembled;
    this.inspection = manifest.inspection;
    for (const asset of [this.assembled, this.inspection].filter(Boolean)) {
      if (!["/model.glb", "/inspection.glb"].includes(asset.url)) {
        throw new Error("The viewer model route is invalid.");
      }
    }
  }

  select(inspection) {
    return !inspection.wholeAssembled && this.inspection ? this.inspection : this.assembled;
  }
}
