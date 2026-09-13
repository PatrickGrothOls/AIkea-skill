/** Scope: Keep all GLTF primitives belonging to one exported part node together. */

export class ReviewPartCatalog {
  constructor(sourceScene, associations) {
    this.scene = sourceScene.clone(true);
    this.parts = [];
    this.names = new Map();
    this.collect(sourceScene, this.scene, associations);
    this.scene.updateMatrixWorld(true);
  }

  collect(source, clone, associations) {
    const association = associations?.get(source);
    const isPart = associations
      ? association?.nodes !== undefined && association?.meshes !== undefined
      : source.isMesh;
    if (isPart) {
      const name = source.name || `Part ${this.parts.length + 1}`;
      const path = source.userData.aikea?.inspection_path;
      const inspectionPath = Array.isArray(path) && path.length > 0
        && path.every((segment) => typeof segment === "string" && segment.length > 0)
        ? path : name.split("__");
      this.parts.push({ node: clone, name, inspectionPath });
      this.names.set(clone, name);
    }
    source.children.forEach((child, index) => this.collect(child, clone.children[index], associations));
  }

  nameFor(object) {
    for (let node = object; node; node = node.parent) {
      if (this.names.has(node)) return this.names.get(node);
    }
    return "";
  }
}
