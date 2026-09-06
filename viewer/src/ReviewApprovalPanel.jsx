/** Scope: Present and persist the bounded decision attached to one visual review. */

import { useEffect, useState } from "react";

import { ReviewDecisionClient } from "./ReviewDecisionClient";

const COPY = {
  door_openings: {
    eyebrow: "Door opening check",
    approve: "Approve door openings",
    change: "Change a door",
    approved: "Door openings approved.",
    requested: "Change requested—return to the chat and name the door.",
  },
  fabrication_assembly: {
    eyebrow: "Fabrication visual check",
    approve: "Approve this assembly",
    change: "Request a change",
    approved: "This exact assembly is visually approved.",
    requested: "Change requested—return to the chat and describe it.",
  },
};

// A function component is the smallest boundary for the review-decision request state.
export function ReviewApprovalPanel({ ready }) {
  const [client] = useState(() => new ReviewDecisionClient());
  const [review, setReview] = useState(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!ready) {
      return undefined;
    }
    let active = true;
    client.load()
      .then((value) => {
        if (active && COPY[value?.review_type]) {
          setReview(value);
        }
      })
      .catch((reason) => active && setError(reason.message));
    return () => {
      active = false;
    };
  }, [client, ready]);

  if (!review && !error) {
    return null;
  }

  const decide = async (decision) => {
    setSaving(true);
    setError("");
    try {
      setReview(await client.submit(decision));
    } catch (reason) {
      setError(reason.message);
    } finally {
      setSaving(false);
    }
  };
  const copy = review ? COPY[review.review_type] : null;

  return (
    <section className="decision-card" aria-live="polite">
      {review && (
        <>
          <p className="eyebrow">{copy.eyebrow}</p>
          <h2>{review.message}</h2>
          {review.doors && (
            <ul>
              {review.doors.map((door) => (
                <li key={door.assembly_id}>
                  <strong>{door.label ?? door.assembly_id}</strong>: hinges on the {door.hinge_side}
                  {door.note ? ` (${door.note})` : ""}
                </li>
              ))}
            </ul>
          )}
          {review.status === "proposed" ? (
            <div className="decision-actions">
              <button disabled={saving} onClick={() => decide("approved")} type="button">
                {copy.approve}
              </button>
              <button
                className="secondary"
                disabled={saving}
                onClick={() => decide("change_requested")}
                type="button"
              >
                {copy.change}
              </button>
            </div>
          ) : (
            <p className="decision-status">
              {review.status === "approved" ? copy.approved : copy.requested}
            </p>
          )}
        </>
      )}
      {error && <p className="decision-error">{error}</p>}
    </section>
  );
}
