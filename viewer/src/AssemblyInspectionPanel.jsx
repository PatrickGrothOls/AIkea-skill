/** Scope: Let the viewer select an assembly, separate its pieces and identify a picked part. */

import { useState } from "react";
import { ExplodedViewState } from "./ExplodedViewState.js";
import { ReviewInspectionPath } from "./ReviewInspectionPath.js";
import "./AssemblyInspection.css";

// A function component keeps native inspection controls bound to React state.
export function AssemblyInspectionPanel({ inspection, onChange, scopes, visibleCount }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <aside className="assembly-inspection review-glass" aria-label="Assembly inspection" data-expanded={expanded}>
      <div className="inspection-heading">
        <h2>Exploded view</h2>
        <button className="inspection-toggle" type="button" aria-expanded={expanded}
          aria-controls="inspection-body" onClick={() => setExpanded(!expanded)}>
          <span>Exploded view</span>
          <span className="inspection-toggle-state">
            <span className="inspection-toggle-amount">{Math.round(inspection.amount * 100)}%</span>
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
              <path d="m2 4 4 4 4-4" stroke="currentColor" strokeWidth="1.5" />
            </svg>
          </span>
        </button>
        <button className="inspection-reset" type="button"
          onClick={() => onChange(new ExplodedViewState())}>Restore assembly</button>
      </div>
      <div className="inspection-body" id="inspection-body">
        <label htmlFor="inspection-detail">Separate</label>
        <select id="inspection-detail" value={inspection.detail}
          onChange={(event) => onChange(inspection.withDetail(event.target.value))}>
          <option value="panels">All panels · keep fittings attached</option>
          <option value="assemblies">Cabinets and subassemblies</option>
        </select>
        <label htmlFor="inspection-assembly">Assembly or part</label>
        <select id="inspection-assembly" value={inspection.scope}
          onChange={(event) => onChange(inspection.withScope(event.target.value))}>
          <option value="">Whole assembly</option>
          {scopes.map((scope) => <option key={scope} value={scope}>{ReviewInspectionPath.label(scope)}</option>)}
        </select>
        <label className="separation-label" htmlFor="inspection-separation">
          Separation <output>{Math.round(inspection.amount * 100)}%</output>
        </label>
        <input id="inspection-separation" type="range" min="0" max={ExplodedViewState.MAX_AMOUNT * 100} step="1"
          value={Math.round(inspection.amount * 100)}
          onChange={(event) => onChange(inspection.withAmount(Number(event.target.value) / 100))} />
        <p className="inspection-part" aria-live="polite">
          {inspection.selectedPart || `Click a piece to see its ID · ${visibleCount} ${visibleCount === 1 ? "piece" : "pieces"} shown`}
        </p>
        {inspection.selectedPart && <button type="button"
          onClick={() => onChange(inspection.withScope(inspection.selectedScope))}>Inspect selected part</button>}
        {!inspection.wholeAssembled && <p className="inspection-note">Inspection pose · assembly order is not verified</p>}
      </div>
    </aside>
  );
}
