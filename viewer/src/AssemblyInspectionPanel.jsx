/** Scope: Let the viewer select an assembly, separate its pieces and identify a picked part. */

import { ExplodedViewState } from "./ExplodedViewState.js";
import "./AssemblyInspection.css";

// A function component keeps native inspection controls bound to React state.
export function AssemblyInspectionPanel({ inspection, onChange, scopes, visibleCount }) {
  return (
    <aside className="assembly-inspection" aria-label="Assembly inspection">
      <div className="inspection-heading">
        <h2>Exploded view</h2>
        <button type="button" onClick={() => onChange(new ExplodedViewState())}>Restore assembly</button>
      </div>
      <label htmlFor="inspection-assembly">Assembly</label>
      <select id="inspection-assembly" value={inspection.scope}
        onChange={(event) => onChange(inspection.withScope(event.target.value))}>
        <option value="">Whole assembly</option>
        {scopes.map((scope) => <option key={scope} value={scope}>{scope.replaceAll("__", " / ").replaceAll("_", " ")}</option>)}
      </select>
      <label className="separation-label" htmlFor="inspection-separation">
        Separation <output>{Math.round(inspection.amount * 100)}%</output>
      </label>
      <input id="inspection-separation" type="range" min="0" max="100" step="1"
        value={Math.round(inspection.amount * 100)}
        onChange={(event) => onChange(inspection.withAmount(Number(event.target.value) / 100))} />
      <p className="inspection-part" aria-live="polite">
        {inspection.selectedPart || `Click a piece to see its ID · ${visibleCount} pieces shown`}
      </p>
      {!inspection.wholeAssembled && <p className="inspection-note">Inspection pose · assembly order is not verified</p>}
    </aside>
  );
}
