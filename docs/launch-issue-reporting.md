# Launch issue reporting

## Scope

Resume the previously parked issue-reporting tool for the public skill. Patrick
requested download visibility and a way to report problems, with no in-product
milestone tracking. Naming is separate, pending confirmation after the name check.

Branch: `codex/launch-issue-reporting`, based on public `origin/main` at
`8920e19ac0e88eeea698c3b42d846298c4902d6e`. The dirty furniture checkout is preserved.

## Work packages

- [x] Verify the public checkout, update-check instructions and release counts.
- [x] Locate and inspect the parked reporting code and existing Google project.
- [x] Bring the existing reporting implementation onto current public main.
- [x] Verify local reporting behavior, packaging and update-check regression tests.
- [x] Add and verify a maintainer command for existing GitHub download counts.
- [ ] Check the existing hosted form and identify the remaining activation step.
- [ ] Activate and verify delivery only with the required account access.
- [x] Prepare a verified local package and record the activation blocker.

## Current state

The release ZIP has five downloads at inspection time. GitHub already supplies
that counter; it counts downloads rather than distinct users or installations.
The canonical skill checks published releases once per new design session and
asks before downloading an update. The existing Google reporting project is
present. The reporting implementation is carried onto current public main. Local
verification passes: 47 Python tests, four packaging subtests, six receiver tests,
all 12 skill links and the privacy check. The maintainer download-count command
adds no client telemetry and uses only public GitHub release metadata. A real
read-only run returns five ZIP downloads. The published ZIP's SHA-256 matches
GitHub's release metadata, and its installed identity is `release`, version
`0.1.0`, so it can identify newer versions.

Hosted activation is not verified. Automatic approval review rejected running
`exportReportingConfiguration` in the existing Google project because execution
could expose private configuration or credentials. No script was run or property
changed. The distributed reporting configuration remains `not_configured`.

A local-only package candidate built from `cbf27da` passes full package integrity
verification and includes the report helper plus inactive public configuration.
Operator infrastructure is excluded. This is not a published release or a working
hosted reporting endpoint.

## Audit log

1. Patrick requested an urgent rename and usage visibility, then narrowed the
   reporting requirement to download counts and problem reports. Do not add
   milestone telemetry.
2. Preserve the previously agreed Google Form reporting route. Reuse its approved
   report preview, privacy screening and browser fallback rather than requiring
   customers to configure GitHub.
3. Keep the rename separate until Patrick selects a name. No branding change or
   public release has been made by this branch.
4. Patrick selected WardrobeWizard after correcting an accidental selection.
   The initial name check found existing uses; publication awaits his response
   to that finding. No name is represented as legally cleared.
5. Preserve the inactive reporting configuration until the hosted receipt is
   verified. Record the approval-review refusal without bypassing it.
6. Inspection found a stale getting-started checksum. Prepare its correction
   separately from reporting so the existing download can be installed safely.
