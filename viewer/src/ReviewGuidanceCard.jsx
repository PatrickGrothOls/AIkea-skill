/** Scope: Present the short title and interaction guidance for one visual review. */

// A function component presents the title without adding independent state.
export function ReviewGuidanceCard({ reviewView }) {
  return (
    <section className="review-card review-glass">
      <p className="eyebrow">AIkea visual review</p>
      <h1>{reviewView.title}</h1>
      <p>{reviewView.guidance()}</p>
    </section>
  );
}
