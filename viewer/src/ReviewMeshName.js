/** Scope: Recognize reserved visual roles after an optional nested assembly path. */

export class ReviewMeshName {
  static hasRole(name, prefix) {
    return name.startsWith(prefix) || name.includes(`__${prefix}`);
  }
}
