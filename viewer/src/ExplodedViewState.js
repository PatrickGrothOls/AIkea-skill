/** Scope: Represent viewer-only separation, assembly focus and part selection. */

export class ExplodedViewState {
  static MAX_AMOUNT = 3;

  static fromSearch(search) {
    const value = Number(new URLSearchParams(search).get("explode") ?? 0);
    return new ExplodedViewState(Number.isFinite(value) ? Math.max(0, Math.min(this.MAX_AMOUNT, value)) : 0);
  }

  constructor(amount = 0, scope = "", selectedPart = "", selectedScope = "") {
    this.amount = amount;
    this.scope = scope;
    this.selectedPart = selectedPart;
    this.selectedScope = selectedScope;
  }

  get wholeAssembled() {
    return this.amount === 0 && this.scope === "";
  }

  withAmount(amount) {
    return new ExplodedViewState(amount, this.scope, this.selectedPart, this.selectedScope);
  }

  withScope(scope) {
    return new ExplodedViewState(0.65, scope);
  }

  withSelectedPart(name, scope = "") {
    return new ExplodedViewState(this.amount, this.scope, name, scope);
  }
}
