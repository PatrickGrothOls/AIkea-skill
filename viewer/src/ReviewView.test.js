/** Scope: Verify URL-selected review views keep their intended camera axes. */

import assert from "node:assert/strict";
import test from "node:test";

import { ReviewView } from "./ReviewView.js";

test("top view looks down and frames width by depth", () => {
  const view = ReviewView.fromSearch("?view=top&title=Base%20top");
  const size = { x: 2978, y: 100, z: 582 };

  assert.deepEqual(view.cameraDirection(), [0, 1, 0]);
  assert.deepEqual(view.frameDimensions(size), {
    horizontal: 2978,
    vertical: 582,
    depth: 100,
  });
  assert.equal(view.title, "Base top");
});

test("bottom view looks upward", () => {
  const view = ReviewView.fromSearch("?view=bottom");

  assert.deepEqual(view.cameraDirection(), [0, -1, 0]);
  assert.deepEqual(view.cameraUp(), [0, 0, -1]);
});

test("structure view looks upward into the base frame", () => {
  const view = ReviewView.fromSearch("?view=structure");

  assert.deepEqual(view.cameraDirection(), [1, -0.35, 1]);
  assert.deepEqual(view.cameraUp(), [0, 1, 0]);
});

test("perspective distance contains the complete three-dimensional bounds", () => {
  const view = ReviewView.fromSearch("");
  const size = { x: 2978, y: 2384, z: 1571 };
  const fieldOfView = 50 * Math.PI / 180;

  assert.ok(view.cameraDistance(size, fieldOfView, fieldOfView) > 5000);
});

test("close framing opens nearer without changing the model", () => {
  const ordinary = ReviewView.fromSearch("");
  const close = ReviewView.fromSearch("?framing=close");
  const size = { x: 743, y: 2288, z: 582 };
  const fieldOfView = 50 * Math.PI / 180;

  assert.ok(
    close.cameraDistance(size, fieldOfView, fieldOfView)
      < ordinary.cameraDistance(size, fieldOfView, fieldOfView),
  );
});

test("only a perspective review shows the studio floor", () => {
  assert.equal(ReviewView.fromSearch("").showsStudioFloor(), true);
  assert.equal(ReviewView.fromSearch("?view=top").showsStudioFloor(), false);
  assert.equal(ReviewView.fromSearch("?view=bottom").showsStudioFloor(), false);
  assert.equal(ReviewView.fromSearch("?view=structure").showsStudioFloor(), false);
});

test("perspective reviews default to photo rendering", () => {
  assert.equal(ReviewView.fromSearch("").usesPhotoRenderer(), true);
  assert.equal(
    ReviewView.fromSearch("?render=interactive").usesPhotoRenderer(),
    false,
  );
});

test("fixed construction views stay interactive unless photo rendering is requested", () => {
  assert.equal(ReviewView.fromSearch("?view=top").usesPhotoRenderer(), false);
  assert.equal(
    ReviewView.fromSearch("?view=top&render=photo").usesPhotoRenderer(),
    true,
  );
});
