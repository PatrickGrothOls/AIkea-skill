# Independent stability review — round 1

Verdict: **FAIL** — one reproducible hosted-submission correctness defect and one public-release instruction gap. These findings do not require deploying the deferred gateway to fix.

## Snapshot and boundaries

Reviewed `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`, base `5db04d7`, target `6de7235b087c3a05e8b268484c305fd76c077329`. HEAD matched before and after; `git status --porcelain=v1` was empty at both checks. No source, dependency, environment, Git or infrastructure changes. No AWS calls, uploads, messages or customer-source execution. Contract read in full. No other review reports consulted.

## Findings

### STAB-1 — P2: normal large viewer captures cannot complete hosted requests

- Requirements: R1, R3, R4.
- Primary location: `viewer/src/ReviewSnapshot.js:8-11`; integrated constraint: `infra/cnc-intake/preview_validation.py:26-28`; caller config: `viewer/src/AssemblyReviewViewer.jsx:90-97`.
- Reachable path: the full-window Canvas uses DPR up to 1.5 and `capture()` serializes its entire drawing buffer. No resizing or shared dimension limit is applied. A 2560×1400 CSS-pixel viewport at DPR 1.5 creates a 3840×2100 image (8,064,000 pixels). The hosted validator rejects anything above 8,000,000 pixels, even if its compressed byte count is tiny and both dimensions individually fit 4096.
- Reproducer/evidence: created a valid RGB PNG with those dimensions, standard IHDR/IDAT/IEND chunks and valid CRCs (28,564 bytes). Passed it through the existing `TestHostedQuoteSession` fixture's actual `HostedQuoteSession.submit` -> multipart transport -> `IntakeGateway` -> acceptance path. Result was `Preview dimensions exceed limits.`, two uploads already performed, and receipt `None`. Identical retry produced the same error without reupload. This is an offline synthetic integration proof; a real browser on a large monitor was not used.
- Impact: invited customers on sufficiently large displays upload the whole source package but cannot obtain a receipt. Shrinking the browser afterward cannot repair the frozen request; `pendingRequest` and the server fingerprint preserve the original preview. They must restart the viewer and lose their entered state. PNGs exceeding the byte cap also have no client normalization, although the reproduced case specifically stays well below that cap.
- Introduced by this release: the snapshot/hosted submission integration and validator are new relative to base.
- Smallest justified fix: normalize the captured PNG before freezing it, using a maximum width/height/pixel budget compatible with intake and checking the encoded byte limit before starting submission. Keep the gateway limits. Add a focused large-viewport capture/acceptance regression.

### STAB-2 — P2: the distributed entry flow omits the new CNC service's actual availability and prerequisites

- Requirements: R6, R7; supports R2/R3.
- Primary locations: `scripts/build_portable_package.py:19-33`, `portable/SKILL.md:8-20`, `portable/BOOTSTRAP.md:33-50`; default boundary `aikea-review-unit/scripts/quote_delivery_session.py:19-31`.
- Reachable path: a fresh public installer user follows packaged SKILL/BOOTSTRAP and the canonical review skill. The new Make it real page is included, but no source/gateway environment is configured, so delivery stays disabled. The only customer setup and native-host caveat are in repository `docs/cnc-customer-upload.md`; the package whitelist excludes all repository docs. Public README/START_HERE and packaged entry/review instructions contain no CNC service-availability notice or CNC configuration guidance. The UI says only that delivery is not configured for this design, which does not communicate that the new customer service is currently unavailable and invitation-only.
- Evidence: called the real `PortablePackage.members()` read-only. It returned 612 files, including the new hosted client and license. Searching the packaged Markdown yielded zero documents containing `AIKEA_CNC_GATEWAY_CONFIG`. Source inspection confirmed that no packaged setup step enables delivery and no public entry instruction explains the deferred hosted deployment or same-computer callback prerequisite. The documented portable design workflow also keeps customer projects outside the replaceable package and requires no Git for setup, while this new submission implementation requires an explicitly chosen Git repository with HEAD plus a design subdirectory; these need to be explained for eventual invited-customer setup.
- Impact: the released package includes an unavailable feature without the explicit release explanation required by R6. Users/assistants cannot distinguish operator deployment deferral from a per-design setup error, nor discover the supported eventual submission prerequisites from the installed artifact. This is a release documentation/integration gap, not a request to finish IAM work or to open registration.
- Introduced by this release: the whitelist and installer are inherited, but the newly added feature was not integrated into their public instructions.
- Smallest justified fix: add a short public and packaged CNC availability section: preferences can be collected; hosted customer sending is currently unavailable pending operator deployment, will be invitation-only, and requires the runtime/browser on the same computer. Link/package durable future configuration guidance that explains explicit repository/design selection. Do not ship credentials, infer invitations, or claim live validation. No need to change the installer dependency set while sending remains explicitly unavailable.

## Coverage and observed passing behavior

**PASS — 57 focused tests**: `direnv exec . python -m pytest -q tests/test_quote_delivery.py tests/test_quote_object_store.py tests/test_quote_source_repository.py tests/test_hosted_quote_session.py tests/test_cnc_intake.py tests/test_cnc_notification.py tests/test_cnc_package_validation.py tests/test_cnc_intake_infrastructure.py`.

**PASS — 6 real-loopback tests**: `direnv exec . python -m pytest -q -p no:cacheprovider tests/test_quote_http.py tests/test_cnc_browser_login.py`. The initial sandbox attempt could not bind localhost (four setup errors and one test failure); rerunning with authorized loopback escalation passed all six. The first test command emitted a sandbox pytest-cache write warning; assertions all passed and tracked/untracked source status remained clean.

Inspected the integrated form/preview/HTTP client, server factory, frozen submission lock/fingerprint, source snapshot allowlist, trusted-host AWS CLI storage, PKCE callback, hosted request and upload flow, intake reservation/quota/storage/acceptance, cloud resources/deploy packaging, notifier and public distribution member selection. Source reads plus tests support:

- Existing viewer caller signature remains intact; delivery defaults to disabled when no explicit source repository is selected.
- Form choices survive dialog close/reopen because the form remains mounted; the retry object is retained within that mounted form.
- Trusted-host and hosted submission freeze one request, protect same-origin/token submission and do not report partial writes as success.
- Source snapshot preserves untracked branch Markdown and working-copy design Python; tests cover deleted tracked source and symlink refusal.
- Hosted completion retries after connection loss without reupload; access-token 401 triggers one new sign-in.
- Gateway ownership/verification/quota/expiry checks and immutable accepted objects are exercised. Ready marker is last; failed publication can retry with identical bytes.
- Notification validates expected request objects and ignores already-notified requests. The existing publish-then-mark sequence explicitly permits duplicates if execution crashes after SNS accepts; no exactly-once guarantee is claimed here.
- Infrastructure notification configuration preserves unrelated configured entries; worker checks bucket/path/event type. Source remains marked untrusted and requests are not manufacturing approval.
- Portable member selection includes runtime Python modules, prebuilt viewer assets, LICENSE and bundled third-party notices; the new local customer runtime uses the standard library and does not itself require boto3. The deployed Lambda dependency boundary is separate.

## Limits and deferred work

**INCONCLUSIVE**: actual hosted end-to-end service, Cognito account provisioning, real S3 POST enforcement, production notification delivery and exact installer download/reinstall behavior. Those were not exercised; IAM/deployment remains explicitly deferred by the contract.

**NOT_RUN**: full regression suite (coordinator-owned), a fresh dependency installation, real browser visual checks, live AWS, real emails/invitations, and exhaustive untouched CAD validation. No speculative hardening recommendations.
