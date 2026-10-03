/** Scope: Render white CAD with consistent lighting and responsive inspection poses. */
import { ACESFilmicToneMapping, AmbientLight, Color, DirectionalLight, HemisphereLight, PerspectiveCamera, Scene, Vector2, Vector3, WebGLRenderer } from "three";
import { ShowcaseRenderQueue } from "./ShowcaseRenderQueue.js";
import { ShowcaseDepthRange } from "./ShowcaseDepthRange.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

export class ShowcaseScene {
  constructor(host) {
    this.host = host;
    this.scene = new Scene();
    this.scene.background = new Color(0xa3afa6);
    this.camera = new PerspectiveCamera(38, 1, 0.001, 25);
    this.renderer = new WebGLRenderer({antialias: true, powerPreference: "low-power"});
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.1;
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    host.append(this.renderer.domElement);
    this.renderer.domElement.setAttribute("aria-label", "Interactive 3D wardrobe. Drag to rotate; pinch or scroll to zoom. Use Reset view to restore the camera.");
    this.renderer.domElement.setAttribute("role", "img");
    this.scene.add(new HemisphereLight(0xffffff, 0x858f7b, 0.8), new AmbientLight(0xffffff, 0.2));
    for (const [position, intensity] of [[[3, 5, 4], 2], [[-3, 2, -4], 2]]) {
      const light = new DirectionalLight(0xffffff, intensity);
      light.position.set(...position);
      this.scene.add(light);
    }
    this.composer = new EffectComposer(this.renderer);
    this.depthRange = new ShowcaseDepthRange(this.camera);
    // Canvas antialiasing does not apply to offscreen postprocessing targets.
    const samples = Math.min(4, this.renderer.capabilities.maxSamples);
    for (const target of [this.composer.renderTarget1, this.composer.renderTarget2]) target.samples = samples;
    this.composer.addPass(new RenderPass(this.scene, this.camera));
    // HDR threshold isolates the emissive strips from white panels and brass.
    const bloom = new UnrealBloomPass(new Vector2(1, 1), 0.35, 0.25, 2);
    // A soft threshold avoids abrupt glow switching as narrow strips cross pixels.
    bloom.highPassUniforms.smoothWidth.value = 1;
    this.composer.addPass(bloom);
    this.composer.addPass(new OutputPass());
    this.renderQueue = new ShowcaseRenderQueue(() => this.draw(), callback => requestAnimationFrame(callback));
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.minDistance = 0.06;
    this.controls.maxDistance = 25;
    this.controls.addEventListener("change", () => this.render());
    this.observer = new ResizeObserver(() => this.resize());
    this.observer.observe(host);
    this.resize();
  }

  resize() {
    const {width, height} = this.host.getBoundingClientRect();
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
    this.composer.setSize(width, height);
    if (this.currentPose) this.frame(this.currentPose);
    else this.render();
  }

  frame(pose) {
    this.currentPose = pose;
    const verticalFov = this.camera.fov * Math.PI / 180;
    const horizontalFov = 2 * Math.atan(Math.tan(verticalFov / 2) * this.camera.aspect);
    let distance = 0;
    const backward = pose.direction.clone().normalize();
    const right = new Vector3().crossVectors(this.camera.up, backward).normalize();
    const up = new Vector3().crossVectors(backward, right);
    for (const x of [pose.bounds.min.x, pose.bounds.max.x]) {
      for (const y of [pose.bounds.min.y, pose.bounds.max.y]) {
        for (const z of [pose.bounds.min.z, pose.bounds.max.z]) {
          const offset = new Vector3(x, y, z).sub(pose.center);
          distance = Math.max(distance, offset.dot(backward) + Math.max(
            Math.abs(offset.dot(right)) / Math.tan(horizontalFov / 2),
            Math.abs(offset.dot(up)) / Math.tan(verticalFov / 2)));
        }
      }
    }
    distance *= 1.12;
    this.controls.target.copy(pose.center);
    this.camera.position.copy(pose.center).addScaledVector(pose.direction.clone().normalize(), distance);
    this.camera.lookAt(pose.center);
    this.controls.update();
    this.render();
  }

  render() {
    this.renderQueue.request();
  }

  draw() {
    // Use the same pipeline at rest and in motion; no shading/glow switch on release.
    if (this.currentPose) this.depthRange.update(this.currentPose.bounds);
    this.composer.render();
  }
}
