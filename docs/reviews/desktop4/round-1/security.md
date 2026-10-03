# Independent security review — round 1

**Verdict: PASS for the reviewed offline security boundaries.** No concrete reachable security defect was found. This is not live deployment approval or a claim that untouched CAD behavior is exhaustively verified.

## Snapshot and method

- Contract read in full: `/tmp/aikea-review-contract-r1.md`.
- Worktree: `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`.
- Base: `5db04d7`; reviewed target: `6de7235b087c3a05e8b268484c305fd76c077329`; branch: `fix/cnc-release-review`.
- HEAD and completely clean tracked/untracked source state verified before and after review.
- Reviewed integrated sources, relevant existing server/resolver and installer dependencies, tests, and package member selection. No prior reviewer reports or commit rationale were used. No source edits, AWS calls, credential reads, messages, or execution of uploaded source.

## Security coverage

| Boundary | Result | Evidence and scope |
| --- | --- | --- |
| Local source selection and snapshot, R2/R4 | PASS | `QuoteSourceRepository` requires an explicit repository root and design subdirectory, snapshots current source bytes plus branch docs, filters exports/known secret paths and other `assemblies` designs, and rejects symlinks. Session package/model digest are fixed at viewer construction. Tests cover dirty/new/deleted code, docs preservation, symlinks, secret/export exclusion. |
| Local browser capability, R4/P1 | PASS | Server binds 127.0.0.1. Quote status checks Host; POST checks Host, exact Origin, JSON content type, bounded length, and a random per-viewer token. Resolver confines served static paths. Actual loopback tests reject foreign origin, wrong Host and incorrect token and prove failed delivery is not success. No route exposes the source ZIP. |
| Frozen submission and retries, R4 | PASS | Lock and request fingerprint freeze content after delivery begins; receipt is recorded only after transport returns success. Conditional object creation and checksum/length comparison support identical retries. Hosted completion preserves original uploads. Tests cover changed requests, partial upload/publication failures and retries. |
| Human login and token transport, R3/P1 | PASS | Cognito configuration is invitation-only, public native client, authorization-code flow, scoped JWT routes. Callback validates random state and fixed host/path, uses PKCE, suppresses code logging and retains no refresh token. HTTPS destinations are constrained and redirect forwarding disabled. Actual loopback PKCE/state test and transport tests pass. |
| Customer ownership and upload authorization, R3/P1 | PASS | Customer namespace derives from authenticated sub; account enabled/verified-email state is reread on each API call. Reservation grants bind exact key, checksum, content type and size with at most five-minute expiry and five daily reservation slots. Cross-user completion is rejected. Customer grants cannot write accepted or ready objects. Real SDK presigned-policy generation is tested with fake credentials and no network. |
| Untrusted source and preview processing, P1 | PASS | ZIP is inspected in memory without extraction/import/execution; archive, expanded bytes, individual files and entry counts are bounded. Traversal, backslash/colon/control paths, symlink/nonregular entries, duplicate names, encrypted/unsupported compression, exports/known secret paths and checksum mismatch are rejected. Manifest exact membership and a design source are required. PNG chunk structure/CRC and dimensions are bounded; rendering is not performed in intake. Hostile archive/preview tests pass. |
| Acceptance and publication, R3/R5/P1 | PASS | Re-read uploaded content must match pinned reservation size/hash; server derives accepted ID and builds request/manifest. Immutable accepted objects are written before ready marker. Runtime IAM is confined to quarantine records/uploads, accepted package objects and identity lookup; customer has no accepted-object credentials or grant. Private quarantine blocks public access and denies insecure transport. |
| Notification and shared bucket, R5/P4 | PASS | Notification filter and worker enforce dedicated bucket/prefix/ready key; manifest lists only the three expected files and worker checks stored metadata/lengths before publishing. Existing notification configuration is retained by merge. SNS failure does not mark notification complete. Message explicitly labels source untrusted and quote as not manufacturing approval. All SNS/S3 operations in tests were fakes. |
| Portable distribution, R7 | PASS within inspected membership | Evaluated tracked-only package membership in memory: 612 files, all ten new quote/CNC support modules, root license and viewer third-party licenses/notices included; no known credential/runtime/local-evidence directory members. Bootstrap uses pinned uv archive checksums and package integrity checks. Did not install/download or execute an assembled release. |
| Availability and deferred services, R6/R8 | PASS within inspected implementation/docs | Customer configuration instructions state hosted intake is not live and native callback requires runtime/browser on the same computer. UI only submits machining and explicitly states painting/installation preferences do not contact tradespeople. Publication of a newly versioned release is coordinator work. |

## Executed validation

1. `direnv exec . python -m pytest -q tests/test_cnc_package_validation.py tests/test_cnc_intake.py tests/test_cnc_intake_infrastructure.py tests/test_quote_delivery.py tests/test_quote_source_repository.py tests/test_quote_object_store.py tests/test_cnc_notification.py tests/test_hosted_quote_session.py` — **57 passed**. One cache-write warning because the frozen worktree was outside sandbox write roots; source remained clean.
2. `direnv exec . python -B -m pytest -p no:cacheprovider -q tests/test_quote_http.py tests/test_cnc_browser_login.py` — **6 passed** after authorized loopback sandbox escalation. Initial sandbox-only attempt could not bind sockets; no product failure remained after rerun.
3. Read-only in-memory portable membership inspection — **PASS**, 612 members, license/notices and new runtime modules present; no suspicious directory members from the checked credential/evidence categories.
4. Final `git rev-parse HEAD` and porcelain status — **PASS**, target unchanged and source clean.

## Findings

None. No introduced or inherited defect met the contract's concrete reachable security-finding threshold. No optional hardening items are promoted into release blockers.

## Limits and deferred work

- **NOT_RUN:** live Cognito authorization, real S3 POST/conditional writes, deployed IAM and bucket privacy, SNS/email delivery, stack recovery or invitation. Local templates/fakes and SDK policy generation do not prove deployed configuration.
- **NOT_RUN:** complete portable install/download, browser visual acceptance, full regression CI and untouched CAD behavior; independently coordinated.
- **INCONCLUSIVE:** production readiness of the hosted gateway. IAM recovery and live end-to-end validation are explicitly deferred by R6; this review does not alter that status.
- Accepted customer source remains untrusted even after structural validation. Validation does not establish that source is safe to run, and no uploaded source was executed here.
- Secret-path filtering is not a content-level secret audit of arbitrary customer repositories. This review inspected distribution paths and security code without reading credential stores.
