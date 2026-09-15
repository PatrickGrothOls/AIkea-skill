/** Scope: Identify door-owned parts from exported inspection paths. */

export class ReviewDoorVisibility {
  static owns(record) {
    return record.path.some((segment) => /^doors?(?:_panel)?(?:_\d+)?$/.test(segment));
  }
}
