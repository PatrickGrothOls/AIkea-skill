/** Scope: Offer only door visibility and continuous part separation in the viewer toolbar. */

import { ExplodedViewState } from "./ExplodedViewState.js";
import "./AssemblyInspection.css";

// A function component binds the two native viewer controls directly to their existing state.
export function AssemblyInspectionPanel({ inspection, onChange, hasDoors, doorsHidden, onToggleDoors }) {
  return (
    <aside className="assembly-inspection review-glass" aria-label="Assembly inspection">
      {hasDoors && <button type="button" onClick={onToggleDoors} aria-pressed={doorsHidden}>
        {doorsHidden ? "Show doors" : "Hide doors"}
      </button>}
      <input className="inspection-separation" type="range" aria-label="Separate parts"
        title="Separate parts" min="0" max={ExplodedViewState.MAX_AMOUNT * 100} step="1"
        value={Math.round(inspection.amount * 100)}
        onChange={(event) => onChange(inspection.withAmount(Number(event.target.value) / 100))} />
    </aside>
  );
}
