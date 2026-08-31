/** Scope: Mount the standalone AIkea cabinet review experience. */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { AssemblyReviewViewer } from "./AssemblyReviewViewer.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AssemblyReviewViewer />
  </StrictMode>,
);
