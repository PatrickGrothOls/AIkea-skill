/** Scope: Verify issue delivery boundaries, bounded abuse exposure and uncertain-write handling. */
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { ReceiverFixture } = require('./issue_reporting_fixture.cjs');
const report = 'Report ID: 12345678-1234-4234-8234-123456789abc\n\nTitle:\nViewer stopped\n\n' +
  'Summary:\nSynthetic shelf update.\n\nExpected:\nNew shelf.\n\nActual:\nOld shelf.\n\n' +
  'Steps:\nRebuild synthetic cabinet.\n\nVersion:\n0.1.0\n\nEnvironment:\nTest browser';

test('publishes only to fixed repository and deduplicates ID and content', () => {
  const f = new ReceiverFixture();
  assert.equal(f.receiver.receive(f.event(report)), 'created');
  assert.equal(f.receiver.receive(f.event(report)), 'created');
  const otherId = report.replace('12345678-', '22345678-');
  assert.equal(f.receiver.receive(f.event(otherId)), 'created');
  assert.equal(f.requests.length, 1);
  const request = f.requests[0];
  assert.equal(request.url, 'https://api.github.com/repos/PatrickGrothOls/AIkea-skill/issues');
  assert.equal(request.options.followRedirects, false);
  assert.equal(JSON.parse(request.options.payload).title, 'Viewer stopped');
  assert.equal(f.released, true);
});

test('rejects missing consent, wrong origin, private data, disabled service and missing token', () => {
  const scenarios = [
    f => f.event(report, []),
    f => ({ ...f.event(report), source: { getId: () => 'other' } }),
    f => f.event(report + '\nprivate@example.test'),
    f => { f.values.ENABLED = 'false'; return f.event(report); },
    f => { delete f.values.GITHUB_TOKEN; return f.event(report); },
    f => f.event(report + 'x'.repeat(6000)),
  ];
  for (const scenario of scenarios) {
    const f = new ReceiverFixture();
    assert.throws(() => f.receiver.receive(scenario(f)));
    assert.equal(f.requests.length, 0);
  }
});

test('uncertain delivery never retries automatically or echoes transport details', () => {
  for (const mode of ['network', 'http', 'receipt']) {
    const f = new ReceiverFixture();
    f.failure = mode === 'network';
    f.code = mode === 'http' ? 403 : 201;
    f.body = mode === 'receipt' ? {} : { number: 42 };
    assert.throws(() => f.receiver.receive(f.event(report)), error =>
      !error.message.includes('sensitive diagnostics') && !error.message.includes('test-only'));
    assert.equal(f.receiver.receive(f.event(report)), 'uncertain');
    assert.equal(f.requests.length, 1);
    assert.equal(f.released, true);
  }
});

test('daily cap and busy lock hold reports without posting', () => {
  for (const mode of ['cap', 'lock']) {
    const f = new ReceiverFixture();
    f.locked = mode !== 'lock';
    if (mode === 'cap') f.values.DAILY_COUNT = JSON.stringify({
      day: new Date().toISOString().slice(0, 10), count: 20,
    });
    assert.throws(() => f.receiver.receive(f.event(report)));
    assert.equal(f.requests.length, 0);
  }
});

test('daily count resets; expired receipts are pruned without deleting configuration', () => {
  const f = new ReceiverFixture();
  f.values.DAILY_COUNT = JSON.stringify({ day: '2000-01-01', count: 20 });
  f.values.receipt_old = JSON.stringify({ time: 0, state: 'created' });
  assert.equal(f.receiver.receive(f.event(report)), 'created');
  assert.equal(f.values.receipt_old, undefined);
  assert.equal(f.values.GITHUB_TOKEN, 'test-only');
  assert.equal(JSON.parse(f.values.DAILY_COUNT).count, 1);
});

test('untrusted Markdown stays inside an expanded code fence', () => {
  const f = new ReceiverFixture();
  const text = report + '\n```\n@some-user malicious instruction\n```';
  f.receiver.receive(f.event(text));
  const body = JSON.parse(f.requests[0].options.payload).body;
  assert.ok(body.includes('````text\n'));
  assert.ok(body.endsWith('\n````'));
});
