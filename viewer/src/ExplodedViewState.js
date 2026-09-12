/** Scope: Represent viewer-only separation, assembly focus and part selection. */

export class ExplodedViewState {
  static fromSearch(search) {
    const value = Number(new URLSearchParams(search).get("explode") ?? 0);
    return new ExplodedViewState(Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0);
  }

  constructor(amount = 0, scope = "", selectedPart = "") {
    this.amount = amount;
    this.scope = scope;
    this.selectedPart = selectedPart;
  }

  get wholeAssembled() {
    return this.amount === 0 && this.scope === "";
  }

  withAmount(amount) {
    return new ExplodedViewState(amount, this.scope, this.selectedPart);
  }

  withScope(scope) {
    return new ExplodedViewState(0.65, scope);
  }

  withSelectedPart(name) {
    return new ExplodedViewState(this.amount, this.scope, name);
  }
}
