/** Scope: Present the short title and interaction guidance for one visual review. */

export function ReviewGuidanceCard({ reviewView }) {
  return (
    <section className="review-card">
      <p className="eyebrow">AIkea visual review</p>
      <h1>{reviewView.title}</h1>
      <p>{reviewView.guidance()}</p>
    </section>
  );
}
