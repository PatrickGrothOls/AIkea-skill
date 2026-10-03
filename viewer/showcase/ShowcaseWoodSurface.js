/** Scope: Share packaged wood textures and real-scale grain across showcase panels. */
import { MeshStandardMaterial, RepeatWrapping, SRGBColorSpace, TextureLoader } from "three";
import { PanelTextureCoordinates } from "../src/PanelTextureCoordinates.js";
import colorUrl from "../public/materials/plywood/plywood_diff_1k.jpg?url";
import normalUrl from "../public/materials/plywood/plywood_nor_gl_1k.jpg?url";
import roughnessUrl from "../public/materials/plywood/plywood_rough_1k.jpg?url";

export class ShowcaseWoodSurface {
  static async load() {
    const loader = new TextureLoader();
    const maps = await Promise.all([colorUrl, normalUrl, roughnessUrl].map(url => loader.loadAsync(url)));
    return new ShowcaseWoodSurface(...maps);
  }

  constructor(map, normalMap, roughnessMap) {
    map.colorSpace = SRGBColorSpace;
    for (const texture of [map, normalMap, roughnessMap]) {
      texture.wrapS = texture.wrapT = RepeatWrapping;
      texture.anisotropy = 4;
    }
    this.material = new MeshStandardMaterial({map, normalMap, roughnessMap, roughness: 0.7, metalness: 0});
    // Lift the wood albedo toward a pale natural finish without changing scene lighting.
    this.material.color.setRGB(2.2, 2.35, 2.5);
    this.material.normalScale.set(0.12, 0.12);
    this.coordinates = new PanelTextureCoordinates();
  }

  applyTo(mesh, identity) {
    this.coordinates.applyTo(mesh.geometry, identity);
    mesh.material = this.material;
  }
}
