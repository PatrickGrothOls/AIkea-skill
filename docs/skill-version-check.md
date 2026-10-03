# Skill version check before design intake

## Scope and current state

Implement Patrick's requested startup check: compare the installed skill with
the public release, offer a newer version and ask before downloading it. This
is a local source change, not a publication or an approved installation update.
The checker and entrypoint instructions are implemented. All 21 targeted tests
and the skill validator pass. A live public API check found `v0.1.0-alpha.2` and
correctly retained this development checkout. Independent boundaries and
skill-creator intent/approval review both passed with no blocking findings.

## Work packages

- [x] Add package identity that distinguishes release versions from development.
- [x] Add a read-only release checker, including published alpha releases.
- [x] Define user-facing current/update/unknown/offline behavior and preserve
  existing designs and the previous package when an update is accepted.
- [x] Verify comparison, missing metadata, offline and development cases.
- [x] Validate the skill and independently review the startup policy.

## Audit log

- User requested the version check as the first step before starting a design.
  A new release must be offered, never silently installed. No answer means no
  update; a refusal continues with the current package.
- The public release is currently an alpha, so checking only GitHub's stable
  `/releases/latest` endpoint would miss it. Query published releases and compare
  semantic version tags, requiring the complete ZIP and checksum assets.
- This checkout is unreleased development. Its metadata must say so; assigning
  the old public alpha's version here would misrepresent the installed code.
- Verified real network failure returns `unavailable` and continues with the
  installed package. Live network check returned `development` with the official
  ZIP/checksum links; no package download, install or project mutation occurred.
- This private-history checkout lacks the public packager and START_HERE files.
  The next public packaging step must stamp release.json before checksumming and
  update the starter/chat guide to check before their existing unit-first prompt.
  Public alpha.2 is unchanged and will not gain this behavior retroactively.
- Independent review: CLI 0→19 lines, version value 0→26, release checker 0→65;
  each has one coherent responsibility and none crosses the 150-line threshold.
  Review confirmed the explicit user update choice and preserved project boundary.
