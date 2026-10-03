# Independent stability review — round 3

Verdict: **PASS** for the reviewed integrated offline unit. No concrete release-blocking stability finding was identified. This is not a production or exhaustive CAD verdict.

## Target and isolation

- Authoritative requirements: `/tmp/aikea-review-contract-r3.md` only.
- Worktree: `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`.
- Base: `5db04d7`; target: `be17becccad0d0b23ae5c383e535e89e072ab0df`.
- Before and after review: HEAD exactly target; `git status --short` empty.
- No repository edits, dependency installation, venv changes, AWS calls, invitations, uploads, notifications, or customer-source execution. No sibling reports, previous verdicts, narrative audit logs, or commit rationale read.

## Coverage and evidence

**R1 — PASS by code inspection; UI runtime not independently exercised.** Reviewed `AssemblyReviewViewer.jsx`, `MakeItRealCard.jsx`, `QuoteRequestPage.jsx`, `QuoteRequestForm.jsx`, `QuoteDeliveryStatus.jsx`, `ReviewSnapshot.js`, and relevant unchanged approval/state dependencies. The mounted dialog/form preserves choices while returning to the design; explicit `[hidden]` CSS preserves assembled-only action visibility. Preview dimensions/bytes are bounded. Submission freezes the first payload and presents the receipt separately from unsent painting/installation preferences.

**R2/R4 — PASS offline.** Reviewed the full `UnitReviewServer` -> handler -> submission session -> repository packager -> trusted object store path, including unchanged viewer session and request handler dependencies. Explicit repository/project selection occurs before source snapshotting. Package source, model bytes and identity remain bound to the viewer session. Dirty source and untracked branch docs are included, tracked deletions preserved, STEP/generated geometry omitted, other assembly designs filtered, symlinks rejected. Host/origin/token checks and frame restrictions guard local browser submission. Session locking, fixed request ID/timestamp, unchanged-payload fingerprints, conditional object writes, and ready-last publication maintain retry behavior without a premature success receipt.

**R3/P1 — PASS offline; live availability NOT_RUN.** Reviewed client login/HTTP transport, gateway, reservations, storage, acceptance, ZIP/PNG validation, and the actual Lambda packaging/resource definitions. Access-token refresh repeats once, bounded file grants bind key/size/checksum, server-derived accepted IDs separate hosted requests from local UUIDs, and only the service publishes accepted bytes and ready markers. Completion validates the frozen descriptors and writes immutable objects before returning a submitted receipt. Simulated upload/completion failures and reauthentication succeed on unchanged retry. Validation does not execute archive code.

**R5 — PASS offline.** Reviewed notification worker and deployment/configuration integration. Dedicated prefix/suffix routing and worker validation restrict notifications to completed requests. Worker checks all three required object descriptors before publishing; the notification receipt is written after SNS accepts the publish. The possible crash-window duplicate is explicit and does not create a false successful notification after publish failure. Existing shared-bucket notification configuration is merged, with a second read detecting changes during preparation. Trusted-host request and manifest shapes remain compatible with the worker.

**R6/R7/R8 — PASS for source/distribution inspection.** Public README, START_HERE, canonical skill, portable skill/bootstrap, and bundled CNC reference state that customer sending is unavailable until deployment and live verification, invitation-only later, and requires a same-computer browser/runtime callback. Git/source repository requirements for later sending are distinguished from installation. Painter/installer outreach and manufacturing approval are not claimed. Read-only `PortablePackage.members()` inspection found 614 distributable members, every required new quote client module/reference present, plus LICENSE and third-party notices. New desktop quote modules depend on the standard library and their bundled sibling modules; hosted Lambda code packages its shared validation dependencies separately. No installer runtime/dependency mutation was performed.

## Executed checks

1. Focused pytest run of quote delivery, repository packaging, object store, preference boundary, hosted session, package/preview validation, gateway intake, notifier, browser login, and portable packaging: **68 passed; one callback bind blocked by the tool sandbox**. This was an environment restriction, not a code failure.
2. Re-ran `tests/test_cnc_browser_login.py` and `tests/test_quote_http.py` with authorized loopback access and pytest cache disabled: **7 passed**. The previously blocked callback test passed. Across both runs this covers **74 distinct passing tests**.
3. Additional in-memory boundary probe: maximal browser-compatible BMP Unicode title/colour/postcode/notes passed preference validation and hosted reservation (15,085-byte serialized request, HTTP 200), without a network call.
4. Read-only portable-member inspection: **no missing required quote module/reference/license members**.
5. Final revision/status verification: target unchanged, clean tracked/untracked status.

## Findings

None requiring correction under this contract. No optional speculative hardening is promoted to a blocker.

## Limits and deferred work

- AWS intake creation/IAM repair, real Cognito sign-in, actual S3 POST policy enforcement, notification delivery, and production timeout/performance behavior: **NOT_RUN**, explicitly deferred by R6/P2.
- Full regression CI is coordinator-owned and was not duplicated. Untouched CAD behavior is not exhaustively certified.
- No live browser visual/layout review or fresh public installer provisioning. Form lifecycle/preview behavior received source inspection; portable contents and packaging behavior received offline inspection/tests.
- The shared venv was used through `direnv exec .` and not modified. Initial pytest cache writes were denied by the sandbox; the subsequent loopback run disabled the cache.
