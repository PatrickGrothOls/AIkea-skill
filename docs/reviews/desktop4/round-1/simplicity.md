# Independent simplicity review — round 1

## Verdict and scope

**FAIL**: one introduced responsibility-boundary violation (S1). Boundary phase **FAIL**; structure phase **NOT_RUN** and final simplification verification phase **NOT_RUN**, as the phase skills require the boundary phase to pass first. The offline regression observations below are evidence, not an override of that ordering.

Reviewed contract `/tmp/aikea-review-contract-r1.md` in full and the complete simplify-code, review-code-boundaries, review-code-structure and verify-code-simplicity skills. Reviewed source without sibling reports or commit rationale. No production files, tests, dependencies, virtual environment, or Git state were changed. No live service requests or messages were sent.

Target confirmed before review: `6de7235b087c3a05e8b268484c305fd76c077329`, branch `fix/cnc-release-review`, clean tracked tree. Base: `5db04d7`. Reviewed the complete changed Python/JS/JSX/CSS production path, its relevant tests, the unchanged HTTP superclass, portable package builder/integrity/setup entry points and public installation instructions. Compiled viewer bundles were treated as generated distribution artifacts, not counted as authored source. No exhaustive claim about untouched CAD or actual hosted/browser operation.

Behavior to preserve: retained quote preferences and current preview; explicit host-selected frozen editable sources/docs; protected local submission; identical retries; private invitation-only bounded hosted intake; ready-last publication; notification only after complete delivery; installer dependencies/notices and truthful availability; no trades outreach or manufacturing approval.

## S1 — Extract shared preference validation from the inline-preview payload

- **Requirement/policy:** P3 (strong separation of concerns, avoid unnecessary structure/caller knowledge); preserve R1, R3, R4 and P1 validation behavior.
- **Location:** `infra/cnc-intake/intake_contract.py:27-32`, especially line 31; collaborating `aikea-review-unit/scripts/quote_request_payload.py:7-35`.
- **Reachable path:** every valid invited-customer `POST /requests` enters `IntakeGateway.handle` → `IntakeReservations.reserve` → `IntakeContract.validate`. That API accepts preferences and upload descriptors, with the real PNG uploaded separately.
- **Evidence:** IntakeContract imports base64 and constructs `data:image/png;base64,` plus the eight-byte PNG signature solely to instantiate QuoteRequestPayload and retrieve `.preferences`. The produced `.preview` is immediately discarded. The metadata-only caller must know exactly enough of the other transport's PNG validation to fabricate an accepted payload. An isolated in-memory capture of the constructor observed `preview` absent from incoming preferences but eight fabricated bytes `89504e470d0a1a0a` passed into QuoteRequestPayload; no network, archive source, or real image was executed.
- **Impact:** present structural coupling, not a demonstrated production outage. Shared preference validation has no independent interface: changes to the inline-preview representation or checks also require changes to a metadata-only reservation caller. Hosted validation currently depends on the weak eight-byte local image check succeeding, despite having its own real PNG validation later. Adding a valid-looking fake image makes caller knowledge larger rather than reusing only the invariant actually shared.
- **Introduced/inherited:** introduced; both classes are new relative to the review base.
- **Smallest justified change — EXTRACT:** give shared preference rules/normalization one coherent OOP owner (for example QuotePreferences). QuoteRequestPayload composes it and keeps inline preview decoding; IntakeContract composes it and keeps UUID/digest/upload-descriptor validation. Remove the fake PNG/base64 conversion. Include the new shared module in IntakeDeployment's runtime packaging. Keep real hosted PNG validation in IntakeAcceptance/PreviewValidation.
- **Before/after:** before, preferences and local inline-image transport are inseparable (35-line payload, 42-line intake contract); after, two callers invoke the preference owner directly, with each transport retaining its actual preview boundary. Do not weaken either image check or copy preference rules into intake. No arbitrary file/line target.
- **Needed checks for a fix:** equivalent accepted/rejected preferences and normalization through both entry points; local preview decoding/rejection remains; hosted reservations need no invented image; hosted completion still validates real PNG; packaged Lambda contains the new owner. Existing focused tests below should continue to pass.

## Responsibility and caller-knowledge assessment

| Area | Owner and assessment |
| --- | --- |
| Shared viewer lifecycle | UnitReviewServer adds delivery composition and handler binding only. KEEP; AWS/auth/preference rules did not enter core server lifecycle. |
| Shared viewer scene | AssemblyReviewViewer wires a snapshot object, visibility callback and render pause. KEEP; actual quote form, requests, authentication and retry rules remain outside it. |
| Quote UI | MakeItRealCard owns native dialog lifecycle; QuoteRequestPage composes layout; QuoteRequestForm owns retained preferences and frozen retry request; QuoteRequestClient owns HTTP; QuoteDeliveryStatus and QuoteServiceChoices own presentation. Cohesive scopes. |
| Local submission | QuoteReviewRequestHandler owns host/origin/content boundary. QuoteSubmissionSession owns capability token, request freeze, locking and receipt reuse. Required security/idempotency checks are not bloat. |
| Delivery choices | QuoteDeliverySession owns configured host packaging/factory and trusted object publication; HostedQuoteSession owns hosted network/auth/upload workflow. Core server sees one submit/status boundary. No extra factory or provider framework is justified merely for style. |
| Source snapshot | QuoteSourceRepository owns explicit repo/design snapshot; SourcePackageRules owns shared allowed path policy used by producer and untrusted validator. KEEP; source enumeration and archive security are distinct coherent responsibilities. |
| Shared preferences | FAIL S1: local inline-preview payload currently owns rules that hosted metadata needs independently. |
| Hosted service | IntakeGateway owns HTTP/JWT-directory boundary; reservations own quota and upload grants; acceptance owns validation-before-publication; storage owns bounded and immutable S3 I/O; ZIP and PNG validators own untrusted formats. An intake-specific gateway may know its feature domain; it is not shared cross-feature core infrastructure. |
| Notification | Worker validates the ready manifest/object metadata before SNS, then marks delivered; infrastructure selects narrow object events and preserves other hooks. Its explicit at-least-once crash window is not new speculative complexity. |
| Distribution/deployment | Portable builder remains responsible for tracked skill/runtime packaging; intake deployment explicitly packages its small server/shared modules; resource classes divide identity/API/storage concerns. No arbitrary extraction requested. |

Production code uses classes for new behavior. Module-level Lambda entry points include a framework-entry rationale. The inherited functional AssemblyReviewViewer has a scope and function rationale; converting it solely for style would not reduce caller knowledge. Changed source files carry scope comments. Repeated validation at customer trust boundaries, immutable-object retries, quota races and token reauthentication have concrete security or recovery jobs and were not proposed for removal.

The publication manifest/receipt values appear in trusted-host and server-acceptance paths, but those paths have different trust and identity ownership. No current divergence was established here; a cross-deployment publisher abstraction is optional, not a release violation. Likewise retained React `started` state supports rendering and is not sufficient evidence of harmful duplicate state on its own.

## Size/cohesion review required by P3

**No changed pre-existing source file is over 150 lines.** Pre-existing changed files were reread in full: UnitReviewServer 48→50, AssemblyReviewViewer 124→131, MakeItRealCard 27→44, ReviewActionCards.css 36→29. No mandatory over-threshold refactor report is triggered. The inherited viewer is the largest changed pre-existing source and still coherently composes scene controls and action-card lifecycle; adding feature composition here does not justify splitting its rendering solely to reduce a number. No newly added authored source file exceeds 150 lines either.

Authored changed production source: **235→1,977 physical lines**, 37 files (33 added, 4 modified; no authored-source deletes/renames). New tests/support: **0→812 lines**, 11 files. This is a feature release, so growth is not itself a simplicity defect. Generated minified bundles, infrastructure JSON, prose, and CI YAML are excluded from these code totals; corresponding handwritten Python infrastructure owners are included. Counts include blank lines, comments and imports.

| Production file | Before | After |
| --- | ---: | ---: |
| `aikea-review-unit/scripts/cnc_browser_login.py` | 0 | 69 |
| `aikea-review-unit/scripts/cnc_http_client.py` | 0 | 25 |
| `aikea-review-unit/scripts/hosted_quote_session.py` | 0 | 82 |
| `aikea-review-unit/scripts/quote_delivery_session.py` | 0 | 49 |
| `aikea-review-unit/scripts/quote_object_store.py` | 0 | 46 |
| `aikea-review-unit/scripts/quote_request_payload.py` | 0 | 35 |
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
| `infra/cnc-intake/intake_contract.py` | 0 | 42 |
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
| `viewer/src/ReviewSnapshot.js` | 0 | 13 |

## Offline evidence and limits

**PASS — 60 tests in 1.31s** using:

```text
direnv exec . env PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider tests/test_quote_delivery.py tests/test_hosted_quote_session.py tests/test_cnc_intake.py tests/test_cnc_package_validation.py tests/test_cnc_notification.py tests/test_cnc_intake_infrastructure.py tests/test_quote_source_repository.py tests/test_portable_desktop_package.py
```

Covers frozen/repeated/concurrent submissions, source/docs inclusion and exclusions, hosted mock network through actual gateway logic, exact SDK upload policy construction, quota/auth/expiry/tampering behavior, ready-marker failure retries, notification validation/failure/repeat handling, preserved bucket configuration, reproducible server runtime packaging, and portable archive contracts. The fixture source is only inspected/hashed/archived by these tests; it is not executed as customer code.

**NOT_RUN:** full regression CI (coordinator-owned); live AWS/IAM/Cognito/S3/SNS; actual browser sign-in and interactive quote UX; installation downloads/full CAD/Blender setup; publishing a release. Hosted gateway deployment/live validation remains explicitly deferred by R6 and was not classified as a code defect. Existing public installer release links were inspected as local instructions, not fetched or claimed current for the pending publication. No DB changes or approvals were introduced.

Final state recheck: `6de7235b087c3a05e8b268484c305fd76c077329`; `## fix/cnc-release-review...origin/main`; no changed tracked/untracked worktree files reported.
