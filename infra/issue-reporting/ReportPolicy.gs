/** Scope: Validate anonymous report text before any GitHub publication. */
class ReportPolicy {
  static get consent() { return 'I approve publishing this report publicly.'; }

  parse(text, consent) {
    if (typeof text !== 'string' || text.length > 6000 ||
        !Array.isArray(consent) || consent.length !== 1 || consent[0] !== ReportPolicy.consent) {
      throw new Error('Report held: missing consent or invalid report size.');
    }
    const id = text.match(/^Report ID: ([0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})\n\n/);
    const title = text.match(/\n\nTitle:\n([^\n]{1,120})\n\nSummary:\n/);
    const privatePatterns = [
      /[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/,
      /(?:\/Users\/|\/home\/|[A-Za-z]:\\Users\\)/,
      /(?:gh[pousr]_|github_pat_|sk-|AKIA)[A-Za-z0-9_/-]{8,}/,
      /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
      /(?:authorization|password|api[_ -]?key|token|secret)\s*[:=]\s*\S+/i,
      /https?:\/\/\S+/,
    ];
    if (!id || !title || privatePatterns.some(pattern => pattern.test(text))) {
      throw new Error('Report held: invalid structure or potentially private information.');
    }
    return { id: id[1], title: title[1], text };
  }
}
