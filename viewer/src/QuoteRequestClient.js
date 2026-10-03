/** Scope: Communicate with the local viewer's protected CNC submission boundary. */

export class QuoteRequestClient {
  constructor(fetcher = globalThis.fetch.bind(globalThis)) {
    this.fetcher = fetcher;
  }

  async status() {
    const response = await this.fetcher("/api/cnc-request", { cache: "no-store" });
    if (response.status === 404) return { enabled: false };
    if (!response.ok) throw new Error("CNC delivery is unavailable on this viewer.");
    return response.json();
  }

  async submit(token, request) {
    const response = await this.fetcher("/api/cnc-request", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-AIkea-Quote-Token": token },
      body: JSON.stringify(request),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "The request could not be sent. Retry below.");
    return result;
  }
}
