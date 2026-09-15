/** Scope: Present the short title and interaction guidance for one visual review. */

// A function component presents the title without adding independent state.
export function ReviewGuidanceCard({ reviewView }) {
  return (
    <section className="review-card">
      <h1>{reviewView.title}</h1>
      <details className="review-help">
        <summary aria-label="Viewer help">?</summary>
        <p className="review-glass">{reviewView.guidance()}</p>
      </details>
    </section>
  );
}
