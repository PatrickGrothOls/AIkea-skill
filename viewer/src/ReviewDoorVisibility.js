/** Scope: Identify wooden door panels without hiding their attached hardware. */

export class ReviewDoorVisibility {
  static owns(record) {
    return record.kind === "panel"
      && record.path.some((segment) => /^doors?(?:_panel)?(?:_\d+)?$/.test(segment));
  }
}
