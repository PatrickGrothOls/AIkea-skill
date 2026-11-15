/** Scope: Isolate the Apps Script receiver from real Google services and GitHub writes. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');

class ReceiverFixture {
  constructor() {
    this.values = { ENABLED: 'true', GITHUB_TOKEN: 'test-only', FORM_ID: 'form',
      REPORT_ITEM_ID: 'report', CONSENT_ITEM_ID: 'consent' };
    this.requests = [];
    this.locked = true;
    this.released = false;
    this.code = 201;
    this.body = { number: 42 };
    const props = {
      getProperty: key => this.values[key] || null,
      getProperties: () => ({ ...this.values }),
      setProperty: (key, value) => { this.values[key] = value; },
      setProperties: values => Object.assign(this.values, values),
      deleteProperty: key => { delete this.values[key]; },
    };
    const context = vm.createContext({
      PropertiesService: { getScriptProperties: () => props },
      LockService: { getScriptLock: () => ({ tryLock: () => this.locked,
        releaseLock: () => { this.released = true; } }) },
      Utilities: { DigestAlgorithm: { SHA_256: 'sha256' },
        computeDigest: (_, value) => Array.from(crypto.createHash('sha256').update(value).digest()) },
      UrlFetchApp: { fetch: (url, options) => {
        this.requests.push({ url, options });
        if (this.failure) throw new Error('Transport error containing sensitive diagnostics');
        return { getResponseCode: () => this.code, getContentText: () => JSON.stringify(this.body) };
      } },
    });
    for (const name of ['ReportPolicy.gs', 'IssueReceiver.gs']) {
      vm.runInContext(fs.readFileSync(path.join(__dirname, '../infra/issue-reporting', name), 'utf8'), context);
    }
    this.receiver = vm.runInContext('new IssueReceiver()', context);
    this.consent = vm.runInContext('ReportPolicy.consent', context);
  }

  event(text, consent = [this.consent]) {
    return { source: { getId: () => 'form' }, response: { getItemResponses: () =>
      [['report', text], ['consent', consent]].map(([id, response]) => ({
        getItem: () => ({ getId: () => id }), getResponse: () => response,
      })) } };
  }
}

module.exports = { ReceiverFixture };
