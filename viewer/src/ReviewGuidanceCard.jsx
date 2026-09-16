/** Scope: Present the viewer header with its title, help and AIkea identity. */

import "./ReviewBrand.css";

// A function component presents the title without adding independent state.
export function ReviewGuidanceCard({ reviewView }) {
  return (
    <section className="review-card">
      <h1>{reviewView.title}</h1>
      <details className="review-help">
        <summary aria-label="Viewer help">?</summary>
        <p className="review-glass">{reviewView.guidance()}</p>
      </details>
      <span className="review-brand" aria-label="AIkea">AIkea</span>
    </section>
  );
}
