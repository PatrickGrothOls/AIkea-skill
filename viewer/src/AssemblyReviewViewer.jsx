/** Scope: Compose the CAD review stage, inspection controls and assembled-view approval. */

import { lazy, Suspense, useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";

import { AssemblyContactShading } from "./AssemblyContactShading";
import { AssemblyStudioFloor } from "./AssemblyStudioFloor";
import { AssemblyStudioEnvironment } from "./AssemblyStudioEnvironment";
import { AssemblyStudioLights } from "./AssemblyStudioLights";
import { AssemblyLighting } from "./AssemblyLighting";
import { CloseInspectionControls } from "./CloseInspectionControls";
import { AssemblyInspectionPanel } from "./AssemblyInspectionPanel";
import { ExplodedViewState } from "./ExplodedViewState";
import { ReviewAssetChoice } from "./ReviewAssetChoice";
import { ReviewAssetModel } from "./ReviewAssetModel";
import { ReviewGuidanceCard } from "./ReviewGuidanceCard";
import { ReviewGlassFilter } from "./ReviewGlassFilter";
import { ReviewApprovalPanel } from "./ReviewApprovalPanel";
import { MakeItRealCard } from "./MakeItRealCard";
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
  const [doorsHidden, setDoorsHidden] = useState(false);
  const [assets, setAssets] = useState(null);
  const [loadStatus, setLoadStatus] = useState("Loading model…");
  useEffect(() => {
    const controller = new AbortController();
    fetch("/review-models.json", { signal: controller.signal, cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error("The viewer model manifest could not be loaded.");
        return response.json();
      })
      .then((manifest) => setAssets(new ReviewAssetChoice(manifest)))
      .catch((error) => { if (!controller.signal.aborted) setLoadStatus(error.message); });
    return () => controller.abort();
  }, []);
  const asset = assets?.select(inspection, doorsHidden);
  const photo = reviewView.usesPhotoRenderer() && inspection.wholeAssembled && !doorsHidden && asset && !asset.baked;
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
        {asset && <ReviewAssetModel key={asset.url} asset={asset} onStatus={setLoadStatus}
          onModelMeasured={setModelBounds} reviewView={reviewView}
          inspection={inspection} doorsHidden={doorsHidden}
          onSelectPart={(name, scope) => setInspection((current) => current.withSelectedPart(name, scope))} />}
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
      data-model-url={asset?.url}
      data-baked-presentation={asset?.baked || false}
      data-photo-renderer={Boolean(photo)}
      data-doors-hidden={doorsHidden}
    >
      <div className="review-stage">
        <Canvas
          camera={{ position: [150, 100, 150], fov: 42 }}
          dpr={[1, 1.5]}
          gl={{ antialias: true, powerPreference: "high-performance" }}
          onCreated={configureReviewRenderer}
        >
          <color attach="background" args={["#e7dfd3"]} />
          <CloseInspectionControls
            modelRoot={modelBounds.modelRoot}
            modelSpan={modelBounds.span}
          />
          {assemblyScene}
          {photo && modelBounds.modelRoot !== null && (
            <Suspense fallback={null}>
              <AssemblyPhotoRenderer enabled={photo} />
            </Suspense>
          )}
          {!photo && <AssemblyContactShading />}
        </Canvas>
      </div>
      <ReviewGlassFilter />
      <ReviewGuidanceCard reviewView={reviewView} />
      {loadStatus && <div className="review-load-status" role="status">{loadStatus}</div>}
      <div className="review-controls">
        <AssemblyInspectionPanel inspection={inspection} onChange={setInspection}
          hasDoors={modelBounds.hasDoors} doorsHidden={doorsHidden}
          onToggleDoors={() => setDoorsHidden((hidden) => !hidden)}
          />
        {inspection.wholeAssembled && (
          <div className="review-action-cards">
            <ReviewApprovalPanel ready={modelBounds.modelRoot !== null} />
            <MakeItRealCard />
          </div>
        )}
      </div>
    </main>
  );
}
