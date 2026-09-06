/** Scope: Load and submit the one decision exposed by the local review server. */

export class ReviewDecisionClient {
  constructor() {
    this.decisionToken = null;
  }

  async load() {
    const response = await fetch("/review-data.json", { cache: "no-store" });
    if (response.status === 404) {
      return null;
    }
    if (!response.ok) {
      throw new Error("The visual review could not be loaded.");
    }
    const payload = await response.json();
    const { decision_token: decisionToken, ...review } = payload;
    if (typeof decisionToken !== "string" || decisionToken.length === 0) {
      throw new Error("The visual review session is invalid.");
    }
    this.decisionToken = decisionToken;
    return review;
  }

  async submit(decision) {
    if (!this.decisionToken) {
      throw new Error("The visual review must be loaded before deciding.");
    }
    const response = await fetch("/api/review-decision", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-AIkea-Review-Token": this.decisionToken,
      },
      body: JSON.stringify({ decision }),
    });
    if (!response.ok) {
      throw new Error("The visual review decision could not be saved.");
    }
    return response.json();
  }
}
