# Independent simplicity review — round 2

## Verdict

**PASS** for simplicity of the integrated release at `dec32663814818a134cad6af9357d34c7d698fc5`, compared with `5db04d7`.

- Boundary phase: **PASS**.
- Structure phase: **PASS**.
- Verification phase: **PASS**, within the offline evidence described below.
- Blocking findings: **none**. No refactor is required by this lane.
- Live hosted deployment, Cognito sign-in, S3 upload, SNS delivery and visual browser acceptance: **NOT_RUN**.

This is a feature addition, not a line-reduction refactor. The added production code has identifiable owners; the verdict does not claim that the total codebase shrank, or that offline results prove production availability.

## Contract and independence

Read `/tmp/aikea-review-contract-r2.md` first, then the complete `simplify-code`, `review-code-boundaries`, `review-code-structure` and `verify-code-simplicity` skills. Reviewed the integrated base-to-target unit, direct callers and tests. Did not read sibling reports, previous review verdicts, commit-message rationale or narrative audit logs. No repository edits, dependency changes, external service calls or subagents.

Required preserved behavior: R1 persistent quote preferences/current preview; R2 editable source plus branch docs without generated exports; R3 invited hosted upload with server-owned publication; R4 authorized immutable local submission and unchanged retry; R5 completed-request notifications only; R6 truthful unavailable hosted-service release; R7 runnable licensed distribution; R8 no trade outreach. P1–P4 define validation, review and privacy boundaries.

## Boundary assessment

| Owner | Required responsibility and assessment |
| --- | --- |
| `AssemblyReviewViewer.jsx:25`, `MakeItRealCard.jsx:7` | Viewer owns renderer lifecycle and composition; card owns native dialog visibility. Viewer adds snapshot construction, a capture callback and pause state, not quote fields or network policy. Keeping the card mounted while hidden preserves form state (R1). KEEP. |
| `ReviewSnapshot.js:3` | Renderer-to-PNG conversion and preview size budget have one owner. Core viewer does not know dimension or encoding limits. KEEP. |
| `QuoteRequestPage.jsx:7`, `QuoteRequestForm.jsx:8`, `QuoteServiceChoices.jsx:11`, `QuoteDeliveryStatus.jsx:5` | Layout, state/submission, service fields and delivery copy each have coherent scopes. The form holds the frozen outgoing request; display components neither send nor reconstruct it (R1, R4, R8). KEEP. |
| `QuoteRequestClient.js:3` | Local HTTP serialization and response/error interpretation are isolated from the form. One network client rather than field-by-field request logic in JSX. KEEP. |
| `unit_review_server.py:25` | Adds delivery construction and handler binding only. Existing session and CAD verification still own their own work; server learns no S3, identity, package filtering or retry details. KEEP. |
| `quote_review_request_handler.py:9` | Feature-owned HTTP route checks Host/Origin/content type/length and translates known submission errors. Other paths delegate to existing review handler (R4). KEEP. |
| `quote_submission_session.py:17` | Common token, lock, payload validation, fingerprint and receipt lifecycle centralize identical retry semantics for both transports. `_deliver` is a genuine variation point, not a one-use wrapper (R4). KEEP. |
| `quote_delivery_session.py:13`, `hosted_quote_session.py:15` | Trusted CLI delivery and authenticated intake orchestration keep provider differences outside core server and base session. Environment factory is small composition of these alternatives. KEEP. |
| `quote_object_store.py:14`, `cnc_http_client.py:12`, `cnc_browser_login.py:39` | AWS CLI immutable writes, bounded no-redirect HTTPS, and human PKCE loopback sign-in are separate transport/protocol concerns (R3–R4). KEEP. |
| `quote_source_repository.py:13`, `source_package_rules.py:6` | Repository snapshot selection is separate from portable path policy. Shared path policy is consumed by both trusted packager and untrusted validator, rather than copied (R2, P1). KEEP. |
| `quote_preferences.py:4`, `quote_request_payload.py:9`, `intake_contract.py:9` | Shared preference policy has one implementation. Local preview decoding and hosted request descriptors differ by actual boundary; separate validation owners are justified (P1). KEEP. |
| `gateway.py:14` | Dedicated intake HTTP adapter routes to reservation/acceptance owners and verifies active, email-verified identity. It does not implement ZIP parsing, grants or ready-marker sequencing. This is feature-specific infrastructure, not general application core. KEEP. |
| `intake_reservations.py:11`, `intake_acceptance.py:12`, `intake_storage.py:9` | Reservation/quota/grants, validation/publication, and conditional bounded storage each own independent invariants. Acceptance writes ready only after immutable contents; no uploaded source is executed (R3–R5, P1). KEEP. |
| `package_validation.py:15`, `preview_validation.py:7` | ZIP and PNG boundaries have distinct formats, limits and algorithms. Separate files improve change ownership and do not merely redistribute a single method. KEEP. |
| `notification_worker.py:10` | Completed-package validation, SNS publication and post-publication receipt remain together as the notification consumer; no UI or auth dependency (R5). KEEP. |
| `api_resources.py`, `identity_resources.py`, `storage_resources.py`, `intake_infrastructure.py`, `deployment_permissions.py` | Resource families separate API, identity, storage and role composition. Policy generation is operator tooling, not an untrusted-customer authorization surface. Declarative maps and small shared constructors reduce repeated CloudFormation shapes without inventing a generic framework. KEEP. |
| `infra/cnc-intake/deploy_intake.py`, `infra/cnc-requests/deploy.py`, `infra/cnc-requests/infrastructure.py` | Deployment preparation/apply and stack definitions remain operator concerns; retained notification merge is confined to notification deployment. KEEP. |

## Structure assessment

No unsupported defensive branch or mandatory local simplification found.

- Token/Host/Origin checks, exact descriptor fields, path normalization, archive types/checksums/limits, duplicate detection, quotas, expiry and immutable-write collision checks are real external-boundary invariants; removing them would weaken P1/R3/R4.
- `QuoteSubmissionSession.submit` checks fingerprint before receipt and sets receipt only after delivery returns. Its lock is required by concurrent double clicks; tested concurrent callers receive one submission.
- `HostedQuoteSession.uploaded` captures a real intermediate state: completed uploads without successful completion response. It prevents unnecessary reupload on retry. A 401 reauthentication branch is bounded to one retry.
- The form's immutable `pendingRequest` and render-state `started` serve different mechanics: stable retry content and React rendering. They are set together before transport begins. Replacing them is optional implementation preference, not a justified release-blocking refactor.
- Exception translation is at external boundaries with specified categories. Inner S3 handlers handle actual missing/collision conditions; unrelated AWS errors propagate. HTTP adapters turn known failures into explicit non-success responses. No Python `except Exception` or silent internal-error success path was added. The JSX network catches render an error and retain retry state.
- JSON serialization helpers and `_resource` are reused for transport representation and standard CloudFormation shape. They are not a new abstraction hierarchy.
- Some protocol facts recur across independently shipped client/service/notifier boundaries (file names, receipt shape, byte budgets); shared `SourcePackageRules` and `QuotePreferences` already remove the most policy-sensitive duplication. A cross-deployment schema framework would increase coupling without a demonstrated need.

## Size and cohesion

Handwritten changed production Python/JS/JSX/CSS: **235 → 1993 lines** (+1758 net), across **38 files**, counting imports/comments/blank lines. **34 new files**, no deleted or renamed handwritten production source files.

Changed tests/fixtures: **0 → 900 lines**, across **13 files**. Tests are excluded from production growth.

No changed handwritten production source exceeds 150 lines. Largest are `AssemblyReviewViewer.jsx` (124→131), `QuoteRequestForm.jsx` (0→96), `QuoteRequestPage.css` (0→94), `infra/cnc-requests/infrastructure.py` (0→87). Whole-file review finds their concerns coherent. The viewer is a composition owner; extracting isolated JSX just to lower its line count would not narrow its knowledge further.

Generated deployment-policy JSON is not counted as handwritten source. The combined 229-line generated policy is owned by the 81-line `DeploymentPermissions` generator; core/identity views are generated from the same statements, not independent policy implementations. Compiled viewer artifacts include two JS content-hash renames, CSS replacement and index update. Their minified/bundled contents are distribution output, not appropriate manual-refactor units. Authored viewer sources are assessed above; bundle rebuild equivalence is outside this lane.

### Per-file production counts

| File | Base | Target |
| --- | ---: | ---: |
| `aikea-review-unit/scripts/cnc_browser_login.py` | 0 | 69 |
| `aikea-review-unit/scripts/cnc_http_client.py` | 0 | 25 |
| `aikea-review-unit/scripts/hosted_quote_session.py` | 0 | 82 |
| `aikea-review-unit/scripts/quote_delivery_session.py` | 0 | 49 |
| `aikea-review-unit/scripts/quote_object_store.py` | 0 | 46 |
| `aikea-review-unit/scripts/quote_preferences.py` | 0 | 23 |
| `aikea-review-unit/scripts/quote_request_payload.py` | 0 | 20 |
| `aikea-review-unit/scripts/quote_review_request_handler.py` | 0 | 49 |
| `aikea-review-unit/scripts/quote_source_repository.py` | 0 | 68 |
| `aikea-review-unit/scripts/quote_submission_session.py` | 0 | 54 |
| `aikea-review-unit/scripts/source_package_rules.py` | 0 | 25 |
| `aikea-review-unit/scripts/unit_review_server.py` | 48 | 50 |
| `infra/cnc-intake/api_resources.py` | 0 | 30 |
| `infra/cnc-intake/deploy_intake.py` | 0 | 68 |
| `infra/cnc-intake/deployment_permissions.py` | 0 | 81 |
| `infra/cnc-intake/gateway.py` | 0 | 67 |
| `infra/cnc-intake/identity_resources.py` | 0 | 30 |
| `infra/cnc-intake/intake_acceptance.py` | 0 | 51 |
| `infra/cnc-intake/intake_contract.py` | 0 | 40 |
| `infra/cnc-intake/intake_infrastructure.py` | 0 | 52 |
| `infra/cnc-intake/intake_reservations.py` | 0 | 56 |
| `infra/cnc-intake/intake_storage.py` | 0 | 52 |
| `infra/cnc-intake/package_validation.py` | 0 | 66 |
| `infra/cnc-intake/preview_validation.py` | 0 | 33 |
| `infra/cnc-intake/storage_resources.py` | 0 | 24 |
| `infra/cnc-requests/deploy.py` | 0 | 70 |
| `infra/cnc-requests/infrastructure.py` | 0 | 87 |
| `infra/cnc-requests/notification_worker.py` | 0 | 80 |
| `viewer/src/AssemblyReviewViewer.jsx` | 124 | 131 |
| `viewer/src/MakeItRealCard.jsx` | 27 | 44 |
| `viewer/src/QuoteDeliveryStatus.jsx` | 0 | 22 |
| `viewer/src/QuoteRequestClient.js` | 0 | 25 |
| `viewer/src/QuoteRequestForm.jsx` | 0 | 96 |
| `viewer/src/QuoteRequestPage.css` | 0 | 94 |
| `viewer/src/QuoteRequestPage.jsx` | 0 | 39 |
| `viewer/src/QuoteServiceChoices.jsx` | 0 | 43 |
| `viewer/src/ReviewActionCards.css` | 36 | 29 |
| `viewer/src/ReviewSnapshot.js` | 0 | 23 |

## Verification evidence

1. `direnv exec . python -m pytest -q tests/test_quote_delivery.py tests/test_quote_source_repository.py tests/test_hosted_quote_session.py tests/test_cnc_package_validation.py tests/test_portable_desktop_package.py` — **42 passed**. One harmless cache-write warning: sandbox denied `.pytest_cache` write. No dependency installation or shared-venv modification.
2. `direnv exec . npm --prefix viewer test` — **73 passed**. Includes bounded preview sizing and existing viewer geometry/inspection state tests. These Node tests do not mount the quote form or prove browser dialog behavior.
3. Read direct HTTP, login, notification and intake tests to assess contract coverage; did not repeat full regression CI owned by the coordinator.
4. Invoked unchanged `PortablePackage.members()` offline against target: **614 members**. New quote/client/source-policy modules are included under `skills/aikea-review-unit/scripts`; LICENSE.md, requirements and third-party notices are retained. Hosted client runtime uses the standard library; boto3 service runtime/test needs are separated from portable client installation. No archive extraction or customer source execution.
5. Read README/START_HERE/portable and review-unit release additions plus `references/cnc-quotes.md`. They explicitly state hosted sending is unavailable, invitation is required after deployment, Git/design-repository prerequisites, same-computer callback limitation, no credentials in chat, and no manufacturing approval or trade outreach. Documentation is consistent with the contract's deferred service scope.

## Limits and deferred work

No live AWS, IAM, real uploads, SNS/email, invitation creation, registration, credential reads or browser OAuth were attempted. Full CAD regressions are coordinator-owned. Actual desktop installation, accessibility, rendered layout, browser preference persistence and compiled bundle reproduction were not exercised here. No finding is inferred merely from deferred IAM/service deployment. Any independent correctness/security finding remains relevant even though this simplicity lane passes.

## Revision and source-state verification

Before review: `HEAD=dec32663814818a134cad6af9357d34c7d698fc5`; `git status --short` empty.
After inspection/tests: same HEAD; `git status --short` empty.
The repository stayed unchanged. Only this report was written under `/tmp/aikea-review-r2/`.
