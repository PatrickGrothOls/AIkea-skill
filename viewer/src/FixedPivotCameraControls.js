/** Scope: Move one camera toward selected cabinet details and orbit it around one fixed model centre. */

import {
  EventDispatcher,
  Quaternion,
  Raycaster,
  Vector3,
} from "three";

import { CabinetSurfaceZoomTravel } from "./CabinetSurfaceZoomTravel.js";

const FULL_TURN_RADIANS = Math.PI * 2;
const DEGREES_TO_HALF_RADIANS = Math.PI / 360;
const MINIMUM_FORWARD_ALIGNMENT = 0.000001;

export class FixedPivotCameraControls extends EventDispatcher {
  constructor(camera, modelSpan) {
    super();
    this.camera = camera;
    this.rotationCenter = new Vector3();
    this.modelRoot = null;
    this.raycaster = new Raycaster();
    this.cameraForward = new Vector3();
    this.cameraRight = new Vector3();
    this.cameraScreenUp = new Vector3();
    this.centerOffset = new Vector3();
    this.orbitAxis = new Vector3();
    this.orbitOffset = new Vector3();
    this.orbitRotation = new Quaternion();
    this.setModelSpan(modelSpan);
  }

  setModelRoot(modelRoot) {
    this.modelRoot = modelRoot;
  }

  setModelSpan(modelSpan) {
    this.zoomTravel = new CabinetSurfaceZoomTravel(modelSpan);
  }

  zoomTowardPointer(pointer, deltaY) {
    if (!this.modelRoot || deltaY === 0) {
      return false;
    }

    this.camera.updateMatrixWorld();
    this.modelRoot.updateMatrixWorld(true);
    this.raycaster.setFromCamera(pointer, this.camera);
    const intersections = this.raycaster.intersectObject(this.modelRoot, true);
    if (intersections.length === 0) {
      return false;
    }

    this.camera.getWorldDirection(this.cameraForward);
    const forwardAlignment = this.cameraForward.dot(this.raycaster.ray.direction);
    if (forwardAlignment <= MINIMUM_FORWARD_ALIGNMENT) {
      return false;
    }

    const nearDistanceAlongRay = this.camera.near / forwardAlignment;
    const rotationCenterDistance = this.camera.position.distanceTo(
      this.rotationCenter,
    );
    const travel = this.zoomTravel.calculateForWheel(
      deltaY,
      intersections[0].distance,
      rotationCenterDistance,
      nearDistanceAlongRay,
    );
    if (travel === 0) {
      return false;
    }

    this.camera.position.addScaledVector(this.raycaster.ray.direction, travel);
    this.update();
    return true;
  }

  orbitByPointerDelta(deltaX, deltaY, viewportHeight) {
    if ((deltaX === 0 && deltaY === 0) || viewportHeight <= 0) {
      return false;
    }

    const radiansPerPixel = FULL_TURN_RADIANS / viewportHeight;
    this.applyWorldRotation(this.camera.up, -deltaX * radiansPerPixel);
    this.orbitAxis.set(1, 0, 0).applyQuaternion(this.camera.quaternion);
    this.applyWorldRotation(this.orbitAxis, -deltaY * radiansPerPixel);
    this.update();
    return true;
  }

  panCameraByPixels(rightPixels, upPixels, viewportHeight) {
    if ((rightPixels === 0 && upPixels === 0) || viewportHeight <= 0) {
      return false;
    }

    this.camera.getWorldDirection(this.cameraForward);
    this.centerOffset.copy(this.rotationCenter).sub(this.camera.position);
    const rotationCenterDepth = this.centerOffset.dot(this.cameraForward);
    if (rotationCenterDepth <= 0) {
      return false;
    }

    const worldUnitsPerPixel = (
      2
      * rotationCenterDepth
      * Math.tan(this.camera.fov * DEGREES_TO_HALF_RADIANS)
      / viewportHeight
    );
    this.cameraRight.set(1, 0, 0).applyQuaternion(this.camera.quaternion);
    this.cameraScreenUp.set(0, 1, 0).applyQuaternion(this.camera.quaternion);
    this.camera.position.addScaledVector(
      this.cameraRight,
      rightPixels * worldUnitsPerPixel,
    );
    this.camera.position.addScaledVector(
      this.cameraScreenUp,
      upPixels * worldUnitsPerPixel,
    );
    this.update();
    return true;
  }

  applyWorldRotation(axis, angle) {
    if (angle === 0) {
      return;
    }

    this.orbitRotation.setFromAxisAngle(axis, angle);
    this.orbitOffset.copy(this.camera.position).sub(this.rotationCenter);
    this.orbitOffset.applyQuaternion(this.orbitRotation);
    this.camera.position.copy(this.rotationCenter).add(this.orbitOffset);
    this.camera.quaternion.premultiply(this.orbitRotation).normalize();
  }

  update() {
    this.camera.updateMatrixWorld();
    this.dispatchEvent({ type: "change" });
  }
}
