/** Scope: Compose the CAD review stage, inspection controls and assembled-view approval. */

import { lazy, Suspense, useState } from "react";
import { Canvas } from "@react-three/fiber";

import { AssemblyContactShading } from "./AssemblyContactShading";
import { AssemblyStudioFloor } from "./AssemblyStudioFloor";
import { AssemblyStudioEnvironment } from "./AssemblyStudioEnvironment";
import { AssemblyStudioLights } from "./AssemblyStudioLights";
import { AssemblyLighting } from "./AssemblyLighting";
import { CloseInspectionControls } from "./CloseInspectionControls";
import { AssemblyInspectionPanel } from "./AssemblyInspectionPanel";
import { ExplodedViewState } from "./ExplodedViewState";
import { ReviewModel } from "./ReviewModel";
import { ReviewGuidanceCard } from "./ReviewGuidanceCard";
import { ReviewGlassFilter } from "./ReviewGlassFilter";
import { ReviewApprovalPanel } from "./ReviewApprovalPanel";
import { configureReviewRenderer } from "./ReviewRenderer";
import { ReviewView } from "./ReviewView";

const AssemblyPhotoRenderer = lazy(() => import("./AssemblyPhotoRenderer"));

// A function component keeps the viewer as a self-contained render-only asset.
export function AssemblyReviewViewer() {
  const [modelBounds, setModelBounds] = useState({
    center: [0, 0, 0],
    lightingSources: [],
    modelRoot: null,
    size: [1, 1, 1],
    span: 1,
    scopes: [],
    visibleCount: 0,
  });
  const [reviewView] = useState(() => ReviewView.fromSearch(window.location.search));
  const [inspection, setInspection] = useState(() => ExplodedViewState.fromSearch(window.location.search));
  const photo = reviewView.usesPhotoRenderer() && inspection.wholeAssembled;
  const assemblyScene = (
    <>
      {reviewView.showsStudioFloor() && inspection.wholeAssembled && (
        <AssemblyStudioFloor modelBounds={modelBounds} />
      )}
      <Suspense fallback={null}>
        <AssemblyStudioEnvironment />
        <AssemblyStudioLights modelBounds={modelBounds} />
        <AssemblyLighting
          enabled={reviewView.showsLighting()}
          sources={modelBounds.lightingSources}
        />
        <ReviewModel onModelMeasured={setModelBounds} reviewView={reviewView}
          inspection={inspection}
          onSelectPart={(name, scope) => setInspection((current) => current.withSelectedPart(name, scope))} />
      </Suspense>
    </>
  );

  return (
    <main
      className="review-shell"
      data-light-source-count={modelBounds.lightingSources.length}
      data-inspection-scope={inspection.scope}
      data-explode-amount={inspection.amount}
      data-visible-part-count={modelBounds.visibleCount}
    >
      <div className="review-stage">
        <Canvas
          camera={{ position: [150, 100, 150], fov: 50 }}
          dpr={[1, 2]}
          gl={{ antialias: true, powerPreference: "high-performance" }}
          onCreated={configureReviewRenderer}
        >
          <color attach="background" args={["#d8d5ce"]} />
          <CloseInspectionControls
            modelRoot={modelBounds.modelRoot}
            modelSpan={modelBounds.span}
          />
          {photo ? (
            <Suspense fallback={assemblyScene}>
              <AssemblyPhotoRenderer key={`photo-${modelBounds.span}`}>
                {assemblyScene}
              </AssemblyPhotoRenderer>
            </Suspense>
          ) : (
            assemblyScene
          )}
          {!photo && <AssemblyContactShading />}
        </Canvas>
      </div>
      <ReviewGlassFilter />
      <ReviewGuidanceCard reviewView={reviewView} />
      <div className="review-controls">
        <AssemblyInspectionPanel inspection={inspection} onChange={setInspection}
          scopes={modelBounds.scopes} visibleCount={modelBounds.visibleCount} />
        {inspection.wholeAssembled && <ReviewApprovalPanel ready={modelBounds.modelRoot !== null} />}
      </div>
    </main>
  );
}
