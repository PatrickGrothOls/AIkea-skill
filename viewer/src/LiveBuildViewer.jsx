/** Scope: Present an early, orbitable construction preview with honest build status. */

import { useEffect, useMemo, useRef, useState } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { LiveBuildFeed } from "./LiveBuildFeed.js";
import { LiveBuildScene } from "./LiveBuildScene.js";
import { LiveBuildCamera } from "./LiveBuildCamera.js";
import { LiveBuildBuffer } from "./LiveBuildBuffer.js";
import "./LiveBuildViewer.css";

// React coordinates one persistent feed and DOM status while the scene stays mounted.
export function LiveBuildViewer() {
  const [revision, setRevision] = useState(null);
  const [connected, setConnected] = useState(true);
  const [connectionError, setConnectionError] = useState("");
  const [problem, setProblem] = useState("");
  const [fit, setFit] = useState(0);
  useEffect(() => {
    const feed = new LiveBuildFeed(setRevision, (available, error = "") => {
      setConnected(available);
      setConnectionError(error);
    });
    feed.start();
    return () => feed.dispose();
  }, []);
  const state = problem ? "preview-error" : connected ? (revision?.state || "waiting") : "disconnected";
  const labels = { waiting: "Waiting for your design", building: "Building your furniture",
    checking: "Checking the assembly", checked: "Ready for design review",
    failed: "The build needs attention", "preview-error": "Preview update failed",
    paused: "Build paused", disconnected: "Live build disconnected" };
  return <main className="live-build-shell">
    <Canvas camera={{ position: [4, 3, 5], fov: 40 }} dpr={[1, 2]} frameloop="demand">
      <color attach="background" args={["#f4f0e8"]} />
      <ambientLight intensity={1.1} />
      <directionalLight position={[4, 6, 3]} intensity={2.2} />
      <directionalLight position={[-3, 2, -2]} intensity={0.6} />
      <LiveBuildLayer revision={revision} connected={connected && !problem} fit={fit} onProblem={setProblem} />
    </Canvas>
    <header className="live-build-heading"><strong>AIkea</strong><span>Live construction preview</span></header>
    {!revision?.parts.length && <div className="live-build-empty">Your furniture will appear here as its parts are built.</div>}
    <section className="live-build-status" aria-live="polite" data-state={state}>
      <span className="live-build-eyebrow">WORK IN PROGRESS</span>
      <h1>{labels[state] || "Build status unavailable"}</h1>
      <p>{problem || (connected ? revision?.message : `Showing the last geometry. ${connectionError}`)}</p>
      {revision?.problems?.length > 0 && <details><summary>What needs attention</summary>
        <ul>{revision.problems.map((item, index) => <li key={index}>{item}</li>)}</ul>
      </details>}
      <small>{revision?.parts.length || 0} parts · Preview only, not fabrication approval</small>
      <button type="button" onClick={() => setFit((value) => value + 1)}>Fit furniture</button>
    </section>
    <p className="live-build-hint">Drag to orbit · Scroll to zoom</p>
  </main>;
}

// R3F hooks bind the imperative CAD scene lifetime to the persistent canvas.
function LiveBuildLayer({ revision, connected, fit, onProblem }) {
  const reduced = useMemo(() => matchMedia("(prefers-reduced-motion: reduce)").matches, []);
  const model = useMemo(() => new LiveBuildScene(reduced), [reduced]);
  const framing = useMemo(() => new LiveBuildCamera(), []);
  const controls = useRef();
  const touched = useRef(false);
  const { camera, gl, scene, invalidate } = useThree();
  const [applied, setApplied] = useState(0);
  const buffer = useRef();
  useEffect(() => {
    buffer.current = new LiveBuildBuffer(model, async (asset, surface) => {
      await gl.compileAsync(asset, camera, scene);
      if (reduced) return;
      for (const material of surface.materials) material.transparent = false;
      await gl.compileAsync(asset, camera, scene);
      for (const material of surface.materials) { material.transparent = true; material.needsUpdate = true; }
    }, () => { setApplied((value) => value + 1); onProblem(""); invalidate(); },
    (error) => onProblem(`Preview update failed: ${error.message}. Previous geometry retained.`));
    return () => { buffer.current.dispose(); model.dispose(); };
  }, [model, onProblem, invalidate, gl, camera, scene, reduced]);
  useEffect(() => { if (revision) buffer.current.enqueue(revision); }, [revision]);
  useEffect(() => { touched.current = false; }, [fit]);
  useEffect(() => {
    if (touched.current) return;
    framing.fit(model.bounds, camera, controls.current, reduced);
    invalidate();
  }, [model, applied, fit, camera, framing, reduced, invalidate]);
  useFrame((state, delta) => {
    model.active = revision?.active || "";
    model.running = connected && ["building", "checking"].includes(revision?.state);
    model.update(Math.min(delta, 0.05), state.clock.elapsedTime);
    framing.update(Math.min(delta, 0.05), camera, controls.current);
    if (framing.moving || (!reduced && (model.running || model.arriving()))) invalidate();
  });
  return <><primitive object={model.root} />
    <OrbitControls ref={controls} makeDefault onStart={() => { touched.current = true; framing.stop(); }} />
  </>;
}
