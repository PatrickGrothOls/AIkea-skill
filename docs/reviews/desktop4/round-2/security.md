# Independent security review — round 2

## Verdict: FAIL

One medium-severity security finding affects the new trusted-host submission capability. No direct cross-origin API/token bypass, cross-account intake access, customer-controlled ready marker, or uploaded-source execution was found. This is an offline code/security verdict, not an AWS deployment verdict.

Target: `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`, `dec32663814818a134cad6af9357d34c7d698fc5`; base `5db04d7`. Initial HEAD matched and tracked/untracked status was clean. Contract read before source inspection. No earlier reports, narrative audit logs, credentials, or commit rationales were consulted.

## Finding S1 — medium: another website can frame the newly privileged submission UI

**Requirement:** R4 and the explicit boundary that other websites must not gain local submission capabilities.

**Evidence:** `aikea-review-unit/scripts/review_request_handler.py:91-104` returns viewer HTML without either `Content-Security-Policy: frame-ancestors ...` or `X-Frame-Options`. `unit_review_server.py:27-34` now attaches the delivery session to this server. `viewer/src/QuoteRequestForm.jsx:17-20` obtains the capability token within the viewer, and `:34-43` submits with that token on a normal form interaction. `MakeItRealCard.jsx:11-24,34-39` exposes the quote form through an ordinary button and dialog.

**Reachable path/prerequisites:** a trusted operator has explicitly enabled delivery by selecting a repository/project, the viewer is running, and the victim visits an attacker page in a browser configuration that permits a remote page to frame loopback content. The attacker needs the viewer port (known or discovered) and induced user clicks. An attacker can position a transparent/obscured iframe over misleading controls, first opening Make it real and then clicking Send CNC quote request. The iframe itself obtains the token and sends the request from the legitimate loopback origin. Consequently the correct Host, Origin, JSON content type and secret token are present; the existing API protections do not stop this interaction. The trusted-host path needs no additional authentication prompt. The hosted path has an extra human login boundary, so the trusted-host path is the clearest affected case.

**Impact:** source and branch documentation can be submitted and a quote notification initiated without a deliberate quote-submission action by the operator. The destination stays Patrick's fixed private bucket; this does not grant arbitrary destination selection or direct source read access to the attacker.

**Reproducer/evidence obtained:** an offline synthetic loopback server using the real `QuoteReviewRequestHandler`, `ReviewFileResolver` and bundled viewer served `GET /` as status 200, `Content-Type: text/html`, `Content-Security-Policy: None`, `X-Frame-Options: None`. Source search found no frame-ancestor policy, X-Frame-Options, or frontend frame-busting control. Browser clickjacking was not executed, and browser-specific local-network restrictions were not evaluated; these are exploitability limits, not evidence of application-level framing protection.

**Introduced/inherited:** missing framing headers are inherited from the existing viewer. The sensitive source-upload action is introduced by this integrated release, making the old framing behavior relevant to the new R4 boundary.

**Smallest justified fix:** prevent the local viewer document from being framed by another site, for example send `Content-Security-Policy: frame-ancestors 'self'` (or `'none'` when no legitimate embedding is required), with matching X-Frame-Options if desired. Add a focused viewer response-header test. This leaves the existing same-origin token checks in place.

## Boundary coverage and positive evidence

- **Local operator vs browser:** repository/design paths and gateway/AWS selection come only from host environment (`quote_delivery_session.py:19-32`), not browser input. Model and source bytes are frozen before binding the loopback server. API Host/Origin/token checks reject direct foreign submissions (`quote_review_request_handler.py:15-39`, `quote_submission_session.py:36-48`). Immutable fingerprint and receipt state preserve identical retries; failed delivery is not reported as submitted.
- **Source snapshot:** `quote_source_repository.py:20-56` packages the selected working copy plus docs, keeps untracked branch Markdown, rejects symlink traversal and omits other assembly designs. `source_package_rules.py:6-25` excludes known credential/generated-output paths and limits portable source names. The rule is a filename/path exclusion policy, not a general content secret scanner; the documented pre-send source review remains relevant.
- **Invitation and authentication:** Cognito has admin-only creation, a public native client with authorization-code flow and short token lifetime (`identity_resources.py:9-27`). API routes require issuer/audience JWT validation and `aikea/submit` scope (`api_resources.py:9-29`). Gateway additionally requires access-token claims and rechecks enabled/verified-email account state (`gateway.py:20-53`). Client uses random state and S256 PKCE, suppresses OAuth callback logs, stores the token in memory, and refuses HTTP redirects (`cnc_browser_login.py`, `cnc_http_client.py`). No Patrick AWS credentials are distributed by this flow.
- **Customer upload authority:** reservations are keyed under the authenticated subject hash; cross-account completion is rejected. Grants bind exact quarantine key, size, SHA-256 and content type, expire within five minutes, and cannot target accepted objects or ready markers (`intake_reservations.py:15-56`). Per-account daily reservation slots and API/concurrency throttles bound activity.
- **Untrusted content:** archive entry/expanded/file limits, duplicate and traversal checks, mode/symlink rejection, exact manifest membership and content hashes occur without extraction or execution (`package_validation.py:21-65`). PNG structure, CRC, length and dimensions are bounded without decoding (`preview_validation.py:8-33`). Acceptance rechecks exact object length/hash, validates bytes, then publishes immutable server-owned files and ready marker last (`intake_acceptance.py:16-50`). Uploaded source remains labelled untrusted.
- **Storage and notification:** quarantine blocks public access, enforces bucket owner ownership and TLS, encrypts storage, and expires temporary data (`storage_resources.py`). Runtime object and listing permissions are prefix-scoped; accepted writes are limited to four expected filenames (`intake_infrastructure.py:37-51`). Notification filter and worker both require the CNC ready path, validate the three expected objects, and notify only after a completed package; email explicitly says quote-only and source-untrusted (`infra/cnc-requests/infrastructure.py:76-84`, `notification_worker.py:23-60`). Existing unrelated bucket notification configuration is preserved by the merge helper. SNS acceptance followed by marker write permits duplicate notification after a crash; this is disclosed in source and is not a false-success or authorization defect.
- **Distribution and availability:** tracked package selection includes canonical skill scripts and third-party license/notice files, excludes unrelated repository/runtime/evidence directories (`scripts/build_portable_package.py:19-38`). Existing bootstrap verifies pinned uv download before execution and checks package content integrity. Public instructions explicitly say customer delivery is unavailable pending deployed/live verification, invitation-only initially, and browser/runtime must share a computer (`portable/SKILL.md:34-39`, `portable/BOOTSTRAP.md:69-74`, `aikea-review-unit/references/cnc-quotes.md:9-44`). No live readiness or trade outreach is claimed.

## Validation

**PASS:** 52 unique selected tests across `test_cnc_package_validation.py`, `test_cnc_intake.py`, `test_cnc_intake_infrastructure.py`, `test_cnc_browser_login.py`, `test_quote_http.py`, `test_quote_source_repository.py`, `test_quote_object_store.py`, and `test_cnc_notification.py`.

First command: `direnv exec . python -m pytest -q` with those eight files. Result: 47 passed; one failure and four setup errors solely from sandbox denial of loopback binds. Authorized rerun: `direnv exec . python -B -m pytest -q -p no:cacheprovider tests/test_cnc_browser_login.py tests/test_quote_http.py`; result: 6 passed (one overlaps the initial successful tests). No shared environment/dependency modifications occurred. The subsequent read-only loopback header probe produced the S1 evidence above.

**INCONCLUSIVE / explicitly deferred:** live Cognito deployment/claims behavior, real S3 policy enforcement, accepted-bucket effective live privacy/IAM, SNS/email delivery and full customer end-to-end behavior. The gateway is not operational per contract. No AWS/network deployment action, real upload, invitation or message was performed.

**NOT_RUN:** full regression suite (coordinator-owned), exhaustive untouched CAD behavior, desktop installer acceptance/download, actual browser clickjacking demonstration, content-wide credential scan. Distribution and installer review here is source/selection inspection, not a newly built or deployed artifact claim.

## Optional hardening / deferred work

No additional optional hardening is required to resolve this verdict. S1 should be fixed or explicitly adjudicated against the R4 website-isolation requirement. IAM setup and live gateway verification remain deferred under R6 and are not additional defects in this report.

## Final state verification

Final verification after report creation returned HEAD `dec32663814818a134cad6af9357d34c7d698fc5` and an empty `git status --short`. Repository edits were not made; only this report was written under `/tmp/aikea-review-r2/`.
