/** Scope: Illuminate the existing recessed LED faces without changing CAD geometry. */
import { MeshStandardMaterial, RectAreaLight, Vector3 } from "three";
import { RectAreaLightUniformsLib } from "three/addons/lights/RectAreaLightUniformsLib.js";

export class ShowcaseLighting {
  constructor(records) {
    RectAreaLightUniformsLib.init();
    this.lights = [];
    this.emitter = new MeshStandardMaterial({color: 0xfff9ed, emissive: 0xfff5df, emissiveIntensity: 6});
    for (const part of records.filter(record => record.name.endsWith("_light"))) {
      part.node.traverse(node => { if (node.isMesh) this.attach(node); });
    }
  }

  attach(mesh) {
    // Source strips run along local X; only their exposed +Z diffuser face emits.
    const geometry = mesh.geometry.clone();
    const normals = geometry.attributes.normal;
    geometry.clearGroups();
    for (let offset = 0; offset < geometry.index.count; offset += 3) {
      const facing = [0, 1, 2].every(i => normals.getZ(geometry.index.getX(offset + i)) > 0.99);
      geometry.addGroup(offset, 3, facing ? 1 : 0);
    }
    mesh.geometry = geometry;
    mesh.material = [mesh.material, this.emitter];
    geometry.computeBoundingBox();
    const {min, max} = geometry.boundingBox;
    // Three.js area-light dimensions ignore parent scale; convert CAD mm to world metres.
    const scale = mesh.getWorldScale(new Vector3());
    const light = new RectAreaLight(0xfff5df, 18, (max.x - min.x) * scale.x, (max.y - min.y) * scale.y);
    light.position.set((min.x + max.x) / 2, (min.y + max.y) / 2, max.z + 0.5);
    light.rotation.y = Math.PI;
    mesh.add(light);
    this.lights.push(light);
  }

  setPose(mode, doorsShown) {
    // Area lights have no occlusion: restrict spill to the assembled interior view.
    for (const light of this.lights) light.visible = mode === "assembled" && !doorsShown;
  }
}
