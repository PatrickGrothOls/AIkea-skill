/** Scope: Present the design-to-furniture action and its current availability. */

import { useRef } from "react";
import "./ReviewActionCards.css";

// A function component only owns native dialog visibility; it sends no requests.
export function MakeItRealCard() {
  const availabilityDialog = useRef(null);

  return (
    <section className="make-real-card review-glass" aria-label="Make this design real">
      <p>Your design, cut to fit and ready to assemble.</p>
      <button className="make-real-action" type="button"
        onClick={() => availabilityDialog.current.showModal()}>
        Make it real <span aria-hidden="true">↗</span>
      </button>
      <dialog ref={availabilityDialog} className="make-real-dialog review-glass"
        aria-labelledby="make-real-title" aria-describedby="make-real-availability">
        <h2 id="make-real-title">Make it real</h2>
        <p id="make-real-availability">
          Online ordering is not available yet. Your design has not been sent.
        </p>
        <button className="make-real-action" type="button" autoFocus
          onClick={() => availabilityDialog.current.close()}>Back to my design</button>
      </dialog>
    </section>
  );
}
