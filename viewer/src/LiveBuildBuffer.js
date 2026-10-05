/** Scope: Coalesce live revisions and finish graphics preparation before starting the next. */

export class LiveBuildBuffer {
  constructor(model, prepare, onApplied, onError, delay = 450) {
    Object.assign(this, { model, prepare, onApplied, onError, delay });
    this.busy = false;
    this.disposed = false;
  }

  enqueue(revision) {
    this.latest = revision;
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.flush(), this.delay);
  }

  async flush() {
    if (this.disposed || this.busy || !this.latest) return;
    const revision = this.latest;
    this.latest = null;
    this.busy = true;
    // Asset fetching/GPU preparation is the single external failure boundary.
    try {
      const changed = await this.model.apply(revision, this.prepare);
      if (!this.disposed && changed) this.onApplied();
    } catch (error) {
      if (!this.disposed) this.onError(error);
    } finally {
      this.busy = false;
      if (!this.disposed && this.latest) {
        clearTimeout(this.timer);
        this.timer = setTimeout(() => this.flush(), this.delay);
      }
    }
  }

  dispose() {
    this.disposed = true;
    this.latest = null;
    clearTimeout(this.timer);
  }
}
