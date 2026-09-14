/** Scope: Preserve authored glTF surfaces and reserve plywood fallback for undeclared parts. */

export class ReviewMaterialSurface {
  constructor(fallback, anisotropy) {
    this.fallback = fallback;
    this.anisotropy = Math.min(anisotropy, 8);
  }

  applyTo(mesh) {
    const materials = [mesh.material].flat();
    const authored = materials.some((material) => material.map || material.userData.aikea?.material_id);
    if (!authored) return this.fallback.applyTo(mesh);
    for (const material of materials) {
      for (const texture of [material.map, material.normalMap, material.roughnessMap].filter(Boolean)) {
        texture.anisotropy = this.anisotropy;
        texture.needsUpdate = true;
      }
    }
  }
}
