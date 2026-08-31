/** Scope: Present and persist the client's post-visual door-opening decision. */

import { useEffect, useState } from "react";

import { ReviewDecisionClient } from "./ReviewDecisionClient";

export function DoorOpeningApprovalPanel({ ready }) {
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
        if (active && value?.review_type === "door_openings") {
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

  return (
    <section className="decision-card" aria-live="polite">
      {review && (
        <>
          <p className="eyebrow">Door opening check</p>
          <h2>{review.message}</h2>
          <ul>
            {review.doors.map((door) => (
              <li key={door.assembly_id}>
                <strong>{door.label ?? door.assembly_id}</strong>: hinges on the {door.hinge_side}
                {door.note ? ` (${door.note})` : ""}
              </li>
            ))}
          </ul>
          {review.status === "proposed" ? (
            <div className="decision-actions">
              <button disabled={saving} onClick={() => decide("approved")} type="button">
                Approve door openings
              </button>
              <button
                className="secondary"
                disabled={saving}
                onClick={() => decide("change_requested")}
                type="button"
              >
                Change a door
              </button>
            </div>
          ) : (
            <p className="decision-status">
              {review.status === "approved"
                ? "Door openings approved."
                : "Change requested—return to the chat and name the door."}
            </p>
          )}
        </>
      )}
      {error && <p className="decision-error">{error}</p>}
    </section>
  );
}
