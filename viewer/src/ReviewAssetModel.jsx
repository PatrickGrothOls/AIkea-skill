/** Scope: Mount one model load, report progress, and dispose it when the selected asset changes. */

import { useEffect, useState } from "react";
import { ReviewAssetLoader } from "./ReviewAssetLoader.js";
import { ReviewModel } from "./ReviewModel.jsx";

// React owns cancellation and the lifetime of the selected GLB.
export function ReviewAssetModel({ asset, onStatus, onModelMeasured, ...props }) {
  const [loaded, setLoaded] = useState(null);
  useEffect(() => {
    const loader = new ReviewAssetLoader();
    onStatus("Loading model…");
    loader.load(asset.url).then((gltf) => {
      if (!gltf) return;
      setLoaded({ gltf, resources: loader.resources });
      onStatus("");
    }).catch((error) => {
      if (!loader.controller.signal.aborted) onStatus(error.message);
    });
    return () => {
      loader.dispose();
      onModelMeasured((current) => ({ ...current, modelRoot: null, lightingSources: [] }));
    };
  }, [asset.url, onStatus, onModelMeasured]);
  return loaded && <ReviewModel {...props} {...loaded} baked={asset.baked}
    onModelMeasured={onModelMeasured} />;
}
