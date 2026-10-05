/** Scope: Verify revision ordering and honest connection loss without dropping the last scene. */
import { test } from "node:test";
import assert from "node:assert/strict";
import { LiveBuildFeed } from "./LiveBuildFeed.js";

test("the default transport preserves the Window receiver required by browsers", async () => {
  const original = globalThis.fetch;
  let called = false;
  // A normal function exposes its receiver, reproducing native Window.fetch's contract.
  globalThis.fetch = async function () {
    assert.equal(this, globalThis);
    called = true;
    return { ok: true, json: async () => ({ session: "native", revision: 1 }) };
  };
  const feed = new LiveBuildFeed(() => {}, () => {});
  try { await feed.poll(); assert.equal(called, true); }
  finally { feed.dispose(); globalThis.fetch = original; }
});

test("feed ignores old revisions, reconnects and accepts a new session", async () => {
  const revisions = [], connection = [];
  let value = { session: "first", revision: 2 };
  const feed = new LiveBuildFeed((r) => revisions.push(r), (c) => connection.push(c), async () => {
    if (value instanceof Error) throw value;
    return { ok: true, json: async () => value };
  });
  await feed.poll();
  value = { session: "first", revision: 1 };
  await feed.poll();
  value = new Error("offline");
  await feed.poll();
  value = { session: "second", revision: 1 };
  await feed.poll();
  assert.deepEqual(revisions.map((r) => r.session), ["first", "second"]);
  assert.deepEqual(connection, [true, true, false, true]);
  feed.dispose();
});
