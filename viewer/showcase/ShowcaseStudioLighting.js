/** Scope: Light the CAD with a fixed studio key and cached, pose-fitted shadows. */
import { AmbientLight, DirectionalLight, HemisphereLight, PCFShadowMap, Sphere, Vector3 } from "three";

export class ShowcaseStudioLighting {
  constructor(scene, renderer) {
    this.renderer = renderer;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = PCFShadowMap;
    // Camera orbit does not change the furniture or light; rebuild only for a new pose.
    renderer.shadowMap.autoUpdate = false;
    scene.add(new HemisphereLight(0xffffff, 0x858f7b, 0.8), new AmbientLight(0xffffff, 0.2));
    this.key = new DirectionalLight(0xffffff, 2);
    this.key.castShadow = true;
    this.key.shadow.mapSize.set(2048, 2048);
    this.key.shadow.normalBias = 0.001;
    this.key.shadow.bias = -0.00005;
    this.direction = new Vector3(-3, 4, 3).normalize();
    const fill = new DirectionalLight(0xffffff, 2);
    fill.position.set(-3, 2, -4);
    scene.add(this.key, this.key.target, fill);
    this.sphere = new Sphere();
  }

  fit(bounds) {
    bounds.getBoundingSphere(this.sphere);
    const { center } = this.sphere;
    const radius = this.sphere.radius * 1.05;
    this.key.target.position.copy(center);
    this.key.position.copy(center).addScaledVector(this.direction, radius * 2);
    const camera = this.key.shadow.camera;
    camera.left = camera.bottom = -radius;
    camera.right = camera.top = radius;
    camera.near = radius * 0.5;
    camera.far = radius * 3.5;
    camera.updateProjectionMatrix();
    this.renderer.shadowMap.needsUpdate = true;
  }
}
