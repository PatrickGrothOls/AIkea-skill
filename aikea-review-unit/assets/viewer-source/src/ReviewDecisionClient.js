/** Scope: Load and submit the one decision exposed by the local review server. */

export class ReviewDecisionClient {
  async load() {
    const response = await fetch("/review-data.json", { cache: "no-store" });
    if (response.status === 404) {
      return null;
    }
    if (!response.ok) {
      throw new Error("The door-opening review could not be loaded.");
    }
    return response.json();
  }

  async submit(decision) {
    const response = await fetch("/api/review-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision }),
    });
    if (!response.ok) {
      throw new Error("The door-opening decision could not be saved.");
    }
    return response.json();
  }
}
