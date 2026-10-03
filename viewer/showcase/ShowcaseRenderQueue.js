/** Scope: Coalesce pointer updates and restore full rendering after interaction. */
export class ShowcaseRenderQueue {
  constructor(draw, requestFrame) {
    this.draw = draw;
    this.requestFrame = requestFrame;
    this.pending = false;
    this.interacting = false;
  }

  setInteracting(value) {
    this.interacting = value;
    this.request();
  }

  request() {
    if (this.pending) return;
    this.pending = true;
    this.requestFrame(() => {
      this.pending = false;
      this.draw(this.interacting);
    });
  }
}
