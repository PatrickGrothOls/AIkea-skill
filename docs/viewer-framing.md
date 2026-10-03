# Local viewer framing protection

## Scope
Prevent cross-site embedding of local viewer approval and quote submission controls.

## Work packages
- [x] Confirm real viewer HTML lacked an ancestor policy.
- [x] Add self-only framing headers at the shared HTTP response boundary.
- [x] Add real loopback tests for static HTML and API headers.
- [x] Pass 11 HTTP and existing viewer decision/artifact tests.
- [x] Complete fresh independent reviews: round 3 passes all lanes.
- [x] Publish and merge.

## Current state
Every viewer response now sends CSP frame-ancestors self and X-Frame-Options
SAMEORIGIN. Top-level browsing and same-origin embedding remain supported.
The existing Host/Origin/token checks remain in force.

## Audit log
- 2026-10-01: Accepted the reviewer finding under the authorized review/fix loop.
  A framed genuine form can obtain its own token; response-level ancestor controls
  close that browser interaction path. The missing header was observed; a browser
  clickjacking exploit was not executed and is not claimed as reproduced.

Release evidence and remaining limits: [desktop4-release.md](desktop4-release.md).
