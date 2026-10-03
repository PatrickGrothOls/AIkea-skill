# Untrusted CNC package validation

## Scope

First small branch stacked on `codex/cnc-request-notifications`: validate incoming
source archives without executing them and include branch documentation in source
snapshots. The authenticated gateway and client integration follow separately.

## Work packages

- [x] Refresh origin/main and preserve the completed notification branch.
- [x] Share the source-file contract between sender and receiver.
- [x] Include new and edited docs in uploaded source snapshots.
- [x] Reject unsafe archives, inconsistent manifests and oversized previews.
- [x] Run adversarial validation tests and existing source-package tests.
- [x] Review and commit this slice.

## Current state

Implementation complete; 24 focused archive, preview and packaging tests pass. No cloud resources changed. The existing synthetic
request is delivered; external/customer uploads are not enabled yet.

## Audit log

1. Patrick approved building the proposed authenticated upload gateway, temporary
   bounded upload permissions, quarantine and server-controlled acceptance. He
   also requested uploading branch documentation. Including untracked Markdown
   under docs prevents new branch plans from disappearing from source packages.
2. This slice implements only offline package validation. It creates no database
   and never imports or runs uploaded Python, shell scripts or repository hooks.
3. Final integration review additionally rejects ZIP filenames truncated at NUL
   and translates malformed compressed streams into validation failures. This
   protects against disagreement between archive readers; the regression passes.

## Verification and limits

Tests cover traversal, exports, symlinks, duplicate entries, expansion limits,
manifest checksums, preview bounds and new branch docs. File validation cannot establish that source code is safe to run.
Received source must be regenerated in a separate disposable sandbox with no
credentials, personal files or network access. Sandbox execution is not part of
this upload gateway.
