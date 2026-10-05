/** Scope: Poll ordered live revisions without overlapping requests or hiding disconnects. */

export class LiveBuildFeed {
  // Bind the browser receiver; injected transports keep this class testable.
  constructor(onRevision, onConnection, fetcher = globalThis.fetch.bind(globalThis)) {
    this.onRevision = onRevision;
    this.onConnection = onConnection;
    this.fetcher = fetcher;
    this.controller = new AbortController();
    this.session = null;
    this.revision = -1;
  }

  async poll() {
    try {
      const response = await this.fetcher("/live-build.json", {
        cache: "no-store", signal: AbortSignal.any([
          this.controller.signal, AbortSignal.timeout(5000),
        ]),
      });
      if (!response.ok) throw new Error("Live build connection unavailable");
      const revision = await response.json();
      if (revision.session !== this.session || revision.revision > this.revision) {
        this.session = revision.session;
        this.revision = revision.revision;
        this.onRevision(revision);
      }
      this.onConnection(true);
    } catch (error) {
      if (!this.controller.signal.aborted) this.onConnection(false, error.message);
    }
  }

  async start() {
    await this.poll();
    if (!this.controller.signal.aborted) this.timer = setTimeout(() => this.start(), 700);
  }

  dispose() {
    this.controller.abort();
    clearTimeout(this.timer);
  }
}
