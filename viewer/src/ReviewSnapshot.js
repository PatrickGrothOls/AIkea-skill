/** Scope: Capture a bounded quote preview without retaining a WebGL drawing buffer. */

export class ReviewSnapshot {
  constructor(rendererState) {
    this.rendererState = rendererState;
  }

  capture() {
    const { gl, scene, camera } = this.rendererState.get();
    gl.render(scene, camera);
    const source = gl.domElement;
    // Keep high-DPI previews comfortably below intake's dimension and byte limits.
    const scale = Math.min(1, 1600 / Math.max(source.width, source.height),
      Math.sqrt(800000 / (source.width * source.height)));
    const preview = source.ownerDocument.createElement("canvas");
    preview.width = Math.max(1, Math.floor(source.width * scale));
    preview.height = Math.max(1, Math.floor(source.height * scale));
    preview.getContext("2d").drawImage(source, 0, 0, preview.width, preview.height);
    const encoded = preview.toDataURL("image/png");
    // A missing preview disables submission before a request can become frozen.
    return (encoded.length - encoded.indexOf(",") - 1) * 3 / 4 <= 4000000 ? encoded : null;
  }
}
