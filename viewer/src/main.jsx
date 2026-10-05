/** Scope: Mount the standalone AIkea cabinet review experience. */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { AssemblyReviewViewer } from "./AssemblyReviewViewer.jsx";
import { LiveBuildViewer } from "./LiveBuildViewer.jsx";
import "./styles.css";
import "./ReviewGlass.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    {new URLSearchParams(window.location.search).has("live") ? <LiveBuildViewer /> : <AssemblyReviewViewer />}
  </StrictMode>,
);
