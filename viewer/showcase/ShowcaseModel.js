/** Scope: Load exact panel meshes and reuse the shared inspection pose engine. */
import { MeshStandardMaterial, Vector3 } from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { AssemblyPresentation } from "../src/AssemblyPresentation.js";
import modelUrl from "./wardrobe.glb.gz?url";

export class ShowcaseModel {
  async load() {
    const response = await fetch(modelUrl);
    if (!response.ok) throw new Error("The model download failed. Please reload to retry.");
    const bytes = await new Response(response.body.pipeThrough(new DecompressionStream("gzip"))).arrayBuffer();
    const gltf = await new GLTFLoader().parseAsync(bytes, "");
    gltf.scene.scale.setScalar(0.001);
    gltf.scene.updateMatrixWorld(true);
    this.presentation = new AssemblyPresentation(gltf.scene, gltf.parser.associations);
    this.scene = this.presentation.scene;
    const white = new MeshStandardMaterial({color: 0xfaf9f6, roughness: 0.7, metalness: 0});
    this.scene.traverse(node => {
      if (node.isMesh) {
        node.material = white;
      }
    });
    return this;
  }

  pose(mode, doorsShown) {
    const state = this.presentation.apply("", mode === "exploded" ? 0.14 : 0, "panels", !doorsShown);
    const center = state.bounds.getCenter(new Vector3());
    return { ...state, center, direction: mode === "exploded" ? new Vector3(0.8, 0.8, 1.8) : new Vector3(0.8, 0.3, 1.8) };
  }
}
