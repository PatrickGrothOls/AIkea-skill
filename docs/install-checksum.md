# Published installer checksum

## Scope

Correct the getting-started checksum for the existing public `v0.1.0` ZIP.
Branch `codex/install-checksum` starts at public `origin/main` commit `8920e19`.
No release asset, installation command or dependency is changed.

## Work packages

- [x] Download the published ZIP without running its contents.
- [x] Compare its size and SHA-256 with GitHub release metadata.
- [x] Correct the stale checksum in `START_HERE.md`.
- [x] Verify the published checksum file and review the final diff.
- [x] Prepare the independently releasable correction for its checkpoint commit.

## Current state

The published ZIP is 14,022,803 bytes. Its computed SHA-256 is
`b061e1a27ab555f3e2dc29354009229b2ed77fd1d699543355532877981ce873`, matching
GitHub's asset metadata. The old getting-started value referred to a different
archive and would cause correct integrity checking to stop installation.
The published `SHA256SUMS` file also matches the corrected value.

## Audit log

1. Patrick requested launch readiness while new users are downloading the skill.
   Inspection found a stale download checksum, so correct that setup blocker
   separately from naming and reporting changes.
