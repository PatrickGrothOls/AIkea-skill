/** Scope: Load exact panel meshes and reuse the shared inspection pose engine. */
import { EdgesGeometry, LineBasicMaterial, LineSegments, MeshStandardMaterial, Vector3 } from "three";
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
    const metal = new MeshStandardMaterial({color: 0x879399, roughness: 0.38, metalness: 0.4});
    const brass = new MeshStandardMaterial({color: 0xc79b4e, roughness: 0.38, metalness: 0.6});
    const materials = {hardware: metal, door_handle: brass};
    const frameEdges = new LineBasicMaterial({color: 0x737970, transparent: true, opacity: 0.25});
    for (const part of this.presentation.records) {
      part.node.traverse(node => {
        if (!node.isMesh) return;
        node.material = materials[part.kind] ?? white;
        if (part.kind === "door_frame") node.add(new LineSegments(new EdgesGeometry(node.geometry), frameEdges));
      });
    }
    return this;
  }

  pose(mode, doorsShown) {
    const state = this.presentation.apply("", mode === "exploded" ? 0.14 : 0, "panels", false);
    // Hide the entire wooden front, including frames and handles; keep hinges inspectable.
    for (const part of this.presentation.records) {
      if (part.kind !== "hardware" && part.path.includes("door_panel")) part.node.visible = doorsShown;
    }
    const center = state.bounds.getCenter(new Vector3());
    return { ...state, center, direction: mode === "exploded" ? new Vector3(0.8, 0.8, 1.8) : new Vector3(0.8, 0.3, 1.8) };
  }
}
