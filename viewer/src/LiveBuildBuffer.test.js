/** Scope: Verify buffering under slow loads, burst updates, errors and disposal. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { setTimeout as pause } from "node:timers/promises";
import { LiveBuildBuffer } from "./LiveBuildBuffer.js";

test("slow preparation finishes while incoming revisions coalesce to the latest", async () => {
  const received = [];
  let release;
  let applied = 0;
  const model = { async apply(revision) {
    received.push(revision);
    if (revision === 1) await new Promise((resolve) => { release = resolve; });
    return true;
  } };
  const buffer = new LiveBuildBuffer(model, undefined, () => applied++, assert.fail, 0);
  buffer.enqueue(1);
  await pause(10);
  buffer.enqueue(2);
  buffer.enqueue(3);
  await pause(10);
  assert.deepEqual(received, [1]);
  release();
  await pause(10);
  assert.deepEqual(received, [1, 3]);
  assert.equal(applied, 2);
  buffer.dispose();
});

test("errors are reported and a disposed buffer cannot publish late results", async () => {
  const errors = [];
  let release;
  let applied = 0;
  const model = { async apply(revision) {
    if (revision === 1) throw new Error("missing asset");
    return new Promise((resolve) => { release = resolve; });
  } };
  const buffer = new LiveBuildBuffer(model, undefined, () => applied++, (error) => errors.push(error.message), 0);
  buffer.enqueue(1);
  await pause(10);
  assert.deepEqual(errors, ["missing asset"]);
  buffer.enqueue(2);
  await pause(10);
  buffer.dispose();
  release(true);
  await pause(10);
  assert.equal(applied, 0);
});
