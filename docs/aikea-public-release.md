# AIkea Skill public release

## Scope
Publish AIkea Skill as the main public product release, replacing the mistaken
Desktop 4 presentation. Retain explicit compatibility and hosted-service limits.

## Work packages
- [x] Accept ordinary semantic release versions in the package builder while retaining historical candidate builds.
- [x] Remove candidate branding from the installation entrypoint without claiming unverified app support.
- [x] Pass nine packaging/setup tests and four subtests; validate all 614 manifest files.
- [x] Publish AIkea Skill as the latest normal release and update public links.
- [x] Remove the superseded Desktop 4 release after the new links merged (PR #24).

## Current state
AIkea Skill v0.1.0 is publicly published as the latest normal release, and its
anonymous download matches the expected checksum. Public links and documentation
are merged; the superseded Desktop 4 release is removed. Its Git tag remains
as historical evidence, not a published product release. Furniture, viewer and upload runtime code
remain the reviewed implementation. Hosted uploads stay deferred.

## Audit log
- 2026-10-01: Patrick explicitly rejected Desktop 4 and requested publication of
  AIkea Skill. Use the product name and normal v0.1.0 release, replacing the new
  candidate release. Preserve previous test history and Git tags as audit history.

Package commit: `141b4dcb6592871958ff76a06d77df28a74d2580`.

SHA-256: `e6fd2db936c88c01709ebda14c3e23c1116978d0e8e3ff2df449ab5cf6ac06bf`.

- 2026-10-01: Confirmed GitHub latest release is named AIkea Skill, tag v0.1.0,
  with draft=false and prerelease=false. Corrected public links merged in PR #24.
- A push using the repository's matching setting unintentionally advanced two old
  branches. Both were restored atomically to their exact prior references using
  explicit leases; subsequent pushes name only the intended branch. No main
  history or unrelated files were changed by that restoration.
