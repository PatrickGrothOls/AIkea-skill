/** Scope: Coalesce input updates into one consistent render per animation frame. */
export class ShowcaseRenderQueue {
  constructor(draw, requestFrame) {
    this.draw = draw;
    this.requestFrame = requestFrame;
    this.pending = false;
  }

  request() {
    if (this.pending) return;
    this.pending = true;
    this.requestFrame(() => {
      this.pending = false;
      this.draw();
    });
  }
}
