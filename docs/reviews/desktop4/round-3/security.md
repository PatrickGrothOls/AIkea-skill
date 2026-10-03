# Independent security review — round 3

Verdict: PASS for the reviewed source-release security boundaries. No confirmed security defect requiring a code change was found. This is not deployment approval or live-service verification.

## Identity and scope

- Authoritative requirements: `/tmp/aikea-review-contract-r3.md` (R1–R8, P1–P4).
- Worktree: `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`.
- Base: `5db04d7`; reviewed HEAD: `be17becccad0d0b23ae5c383e535e89e072ab0df`.
- HEAD matched and `git status --short` was empty before and after review. `git diff --check 5db04d7..HEAD` passed.
- Independent source/test inspection; no sibling reports, previous review conclusions, narrative audit logs, or commit rationale were consulted. No repository edits, credential reads, customer source execution, real uploads, AWS mutations, invitations, or messages occurred.

## Actors, capabilities and boundary evidence

| Actor / entry point | Reviewed capability and evidence | Result |
| --- | --- | --- |
| Trusted local operator / launch environment | Explicit source repository plus design subdirectory is required. `quote_delivery_session.py:19-32` selects trusted AWS or hosted transport; browser metadata cannot supply local paths or AWS configuration. `quote_source_repository.py:14-47` validates repository/design selection, snapshots bytes, excludes forbidden files, and rejects symlink traversal. `unit_review_server.py:25-34` binds this snapshot to the model digest and a loopback-only server. | PASS R2/R4 |
| Other website / local HTTP submission | `quote_review_request_handler.py:15-39` validates Host before exposing the token, requires the exact Origin/Host, JSON, bounded body and the session token for submission. `quote_submission_session.py:36-48` validates the token before delivery. No CORS permission is supplied. `review_request_handler.py:79-83` blocks cross-site framing. These are browser-origin protections; an already trusted same-user local process can access loopback, which is outside the hostile-website actor. | PASS R4 |
| Invited customer / authentication | `identity_resources.py:9-27` disables public self-registration, uses a public native client with authorization code flow, and short access-token lifetime. `api_resources.py:9-29` binds issuer, audience and required submit scope on both routes. `gateway.py:20-35,48-53` requires access-token claims and checks current account-enabled/verified-email status. `cnc_browser_login.py:20-37,48-69` checks callback host/state, uses S256 PKCE, suppresses callback logs, retains no refresh token and clears the code. | PASS R3/P1 |
| Invited customer / reservation and object upload | `intake_contract.py:12-40` validates exact descriptor keys, canonical UUID, checksums and size bounds. `intake_reservations.py:15-53` uses owner-derived keys, atomic daily slots, immutable request intent, expiring exact-key/size/checksum POST policies, and never grants accepted-prefix or ready-marker publication. | PASS R3/P1 |
| Customer crossing account or publication boundary | `intake_acceptance.py:16-38` looks up reservations under the authenticated owner, derives a separate accepted ID from owner/request, checks expiry and actual byte digests, then validates source/preview. `intake_storage.py:13-49` bounds reads and uses conditional writes with exact-byte conflict checks. `intake_acceptance.py:39-50` writes server-authored metadata and writes ready.json last. | PASS R3/R4/P1 |
| Untrusted ZIP / validation | `package_validation.py:21-65` checks archive/expanded/member sizes, entry count, duplicate casefolded names, file types, encrypted/unsupported entries, null truncation, exact manifest membership, hashes and editable source. `source_package_rules.py:15-25` rejects traversal/absolute-path shapes, backslashes, drive/stream separators, symlink-relevant directories, known credential paths and generated-export suffixes. Validation reads archive bytes without extracting, importing or executing source. | PASS R2/P1 |
| Untrusted PNG / validation | `preview_validation.py:8-33` bounds bytes, dimensions, permitted chunk types, CRCs and framing without decoding or executing the image. It is structural validation, not exhaustive image-decoder correctness proof. | PASS within stated structural scope P1 |
| Hosted client / network destination | `hosted_quote_session.py:18-26,70-82` constrains public configuration and S3 upload destinations. `cnc_http_client.py:7-25` disables redirects, bounds responses and leaves TLS verification to the standard HTTPS client. Credentials stay in the local runtime and are not returned to the viewer. Operator-provided configuration remains a trusted input. | PASS R3 |
| Service / private storage | `storage_resources.py:7-23` provisions private, owner-enforced, encrypted quarantine storage, requires TLS and expires temporary objects. `intake_infrastructure.py:37-51` confines runtime reads/writes to quarantine namespaces and the four accepted package filenames; it cannot write notified.json, publish SNS, delete objects or change identity configuration. | PASS R3/P1/P4 at template level |
| Completed request / existing notifier | `quote_delivery_session.py:34-49` preserves trusted-host publication and ready-last behavior. `notification_worker.py:23-45` accepts only ObjectCreated events for the expected bucket/CNC ready path and verifies manifest membership, object sizes/hash metadata and request ID. `infrastructure.py:76-84` retains unrelated bucket hooks while adding the prefix/suffix filter. Worker IAM and SQS source conditions are restricted (`infrastructure.py:14-23,42-46`). Arbitrary unrelated shared-bucket objects do not qualify. | PASS R5/P4 |
| Operator / notification contents | `notification_worker.py:46-60` sends an AWS-console link requiring sign-in, identifies uploaded source as untrusted, instructs isolated regeneration without credentials/network, and explicitly denies manufacturing approval. It marks notification after SNS acceptance; crash-window duplicates remain possible and are accurately documented in code. | PASS R2/R5/P4 |
| Public installer / distribution | `build_portable_package.py:19-38` uses tracked skill/portable files plus LICENSE/requirements; the offline member inventory contained 614 files, required new client/source/reference modules, and no tested excluded credential/evidence directory names. `portable/setup.sh` pins and checks the uv archive; `package_integrity.py:9-18` verifies packaged members and rejects escaping paths. Public instructions describe hosted sending as unavailable/invitation-only and explain same-computer callback requirements (`README.md:183-188`, `START_HERE.md:63-68`, `references/cnc-quotes.md:9-44`). No new customer AWS credentials are required. | PASS R6/R7 |
| Painting / installation choices | `QuoteDeliveryStatus.jsx` distinguishes saved preferences from actual CNC delivery. Server receipts name only machining; no painter/installer outreach route was introduced. | PASS R8 |

Paths in the table are relative to their inspected directories: local Python modules under `aikea-review-unit/scripts/`, gateway modules under `infra/cnc-intake/`, notification modules under `infra/cnc-requests/`, UI modules under `viewer/src/`, and quote references under `aikea-review-unit/`.

## Executed verification

1. `direnv exec . python -m pytest -q tests/test_cnc_intake.py tests/test_cnc_package_validation.py tests/test_cnc_intake_infrastructure.py tests/test_cnc_notification.py tests/test_hosted_quote_session.py tests/test_quote_delivery.py tests/test_quote_source_repository.py tests/test_quote_preferences.py tests/test_quote_object_store.py`
   - PASS: 66 tests. Initial pytest cache write was denied by the read-only checkout sandbox; assertions passed. No environment modification was performed.
2. `direnv exec . python -B -m pytest -p no:cacheprovider -q tests/test_quote_http.py tests/test_cnc_browser_login.py`
   - PASS: 7 tests with authorized local-socket escalation. Initial sandbox-only attempt could not bind loopback and therefore did not exercise six socket-dependent checks; this rerun resolved the environmental limitation.
3. Read-only `PortablePackage.members()` inventory: 614 members, required hosted/local source modules and LICENSE/requirements present, no `.aws`, `.ssh`, `.env`, `local-evidence`, `reviews`, or `renders` path components in distribution members. This is a path/membership check, not a claim to detect credentials hidden in arbitrary file content.
4. Revision/status and diff-whitespace checks remained clean.

Total focused passing tests: 73. Synthetic AWS clients use explicit dummy credentials and no live service calls.

## Findings and limits

- Required security fixes: none identified; no introduced or inherited release-blocking finding established in the reviewed paths.
- Optional hardening: none promoted to a requirement. Do not expand this release based on hypothetical hostile operator configuration or a compromised same-user local process.
- INCONCLUSIVE live behavior: actual Cognito issuer/audience/scope enforcement, native browser sign-in, S3 POST policy enforcement, shared accepted-bucket privacy/policies, notification subscription/delivery, IAM permissions, deployed code and end-to-end availability were not checked. R6 explicitly defers IAM/deployment/live proof. Template tests are not proof of deployed state.
- NOT_RUN: full CAD regression, fresh dependency download/installer execution, current external release URL/checksum validation, uploaded source regeneration, and real email delivery. These require their own approved validation and are not implied by this verdict.
- Existing notification deduplication is at-least-once, not exactly-once; this does not weaken the completed-package publication boundary.
- Source packages remain untrusted even after validation; permitted Python/shell/source files must not be executed with operator credentials or network access. Path filters exclude known forbidden paths, not every possible secret embedded in arbitrary source.
