# AIkea release review contract v3

## Target
Repository/worktree: <user-home>/.codex/worktrees/cnc-release-review/AIkea-skill
Base: 5db04d7 (previous public main)
Target: be17becccad0d0b23ae5c383e535e89e072ab0df
Branch: fix/viewer-framing. Tracked tree is clean and frozen during this round.
Review the integrated AIkea skill release, with primary depth on the entire new Make it real -> quote -> source packaging -> trusted-host or authenticated customer upload -> notification flow. Include portable installer/distribution and existing caller compatibility; inspect unchanged dependencies where needed. Full regression CI is separately coordinated. Do not claim exhaustive proof of untouched CAD behavior.

## Requirements and provenance
- R1 [approved, current conversation]: Make it real opens the agreed quote page with current furniture preview and CNC, painting, installation preferences; choices persist when returning to design.
- R2 [approved, current conversation]: CNC requests go to Patrick's private S3 destination without asking the customer for AWS configuration. Requests carry editable repository code and branch docs; do not upload STEP or other generated geometry. Patrick regenerates locally.
- R3 [approved architecture, user accepted build/deploy after cost discussion]: Customer upload uses separate invitation-only browser login and short-lived bounded upload grants. Never distribute Patrick's credentials. The service, not the customer, controls publication/ready markers.
- R4 [established source-submission contract]: Local host explicitly selects repository/design, freezes source with model, rejects unauthorized local callers, preserves identical retry behavior, and must not report failed or incomplete submission as success.
- R5 [approved original notification request]: Only completed CNC requests trigger existing notification flow; arbitrary shared-bucket uploads do not. A submitted request is not approval to machine. Original trusted-host behavior must remain intact.
- R6 [approved latest user]: Push and merge, full review/fix loop, then publish updated skill. User explicitly deferred IAM setup. New hosted gateway is not operational; release must truthfully explain availability and cannot claim live validation. Source publication/installer release is authorized; opening registration to everyone is NOT assumed.
- R7 [existing public release contract, LICENSE.md / README]: Preserve source-available noncommercial license and third-party notices; installer must include runnable dependencies/code and truthful release instructions. Exclude credentials and local evidence from distribution.
- R8 [deferred work from accepted slice scope docs/cnc-request-delivery.md Scope]: Automated painter/installer discovery and email outreach are not implemented in this release. Do not claim those requests sent or send messages during review.

## Policies
- P1: Untrusted archive/preview/metadata must be bounded and validated without executing uploaded source. Reject traversal, symlinks, forbidden generated exports/secrets paths, malformed metadata. Accepted data is private and server controlled. Trusted config/operator deployment authority differs from customer input authority.
- P2: Review is offline/read-only. No AWS mutations, real uploads, emails, invitations, IAM changes or executing customer source. Local synthetic fixtures and loopback tests permitted. Never read credentials. Do not contact live services except primary public documentation if necessary.
- P3: User AGENTS rules: use direnv exec . for every command/script; existing .venv symlink is shared and MUST NOT be modified. OOP architecture, each source file has scope comment; standalone functions need efficiency rationale. >150 LoC triggers cohesion review, not arbitrary splitting. Simplicity reviewer must report refactor/cohesion assessment for existing over-threshold changed files. Avoid speculative defensive branches and unnecessary bloat. No DB architecture changes without explicit user direction.
- P4: Shared bucket privacy, existing notifier behavior and prior histories must remain intact. Receiving a quote never approves manufacturing. Do not claim live upload verification from offline tests.

## Boundaries and checks
Actors: operator configures trusted host/runtime; local browser sends preferences plus snapshot; invited customer authenticates and submits untrusted bounded packages; service validates and publishes; operator receives source. Other websites must not gain local submission capabilities.
Allowed: direnv exec . python -m pytest <focused tests>; direnv exec . npm --prefix viewer test (if dependencies available). Loopback sockets require tool sandbox escalation, which is allowed for tests. Full suite is coordinator owned; avoid duplicating it. Do not mutate production/test files, dependencies or git. Reports only in /tmp/aikea-review-r3/ assigned path. Do not read sibling reports or prior review verdicts. Do not read commit-message rationale or narrative audit logs as approved product policy. Source files and tests are available without restriction.
Known operational limit: AWS intake creation failed; IAM fix/redeploy/live Cognito/S3 end-to-end proof are explicitly deferred. This is a verification limit, not automatically a code defect. Native PKCE callback requires browser and skill runtime on same computer; remote-cloud model handoff is not implemented. Exact public installer flow must not mislead users about these constraints.

## Reporting
Verify target and source state before/after. Report PASS / FAIL / INCONCLUSIVE / NOT_RUN with coverage and limits. Concrete findings need requirement/policy ID, file/line, reachable path/prerequisites, evidence/reproducer, impact, introduced/inherited distinction and smallest justified fix. Separate optional hardening and deferred work. No-findings is valid. Do not spawn other agents; responsibility reviews are part of the assigned simplicity lane. Never change code.
