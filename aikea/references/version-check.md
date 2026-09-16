# Check for an update before starting

At the beginning of a new AIkea design session, before the first intake question
or dependency installation, check the installed package against the official
published release. Check once per session; do not interrupt an active build with
repeated checks. Preserve measurements already supplied by the user.

Run `python <skill-directory>/scripts/check_skill_version.py` with the available
Python runtime. In a direnv-managed checkout use `direnv exec . python ...`.
This uses only Python's standard library: it does not need CadQuery, install
dependencies, download the package, or transmit any project measurements.

## Respond to the result

- `update_available`: briefly name the installed and available versions, link
  the release, then ask: "A newer AIkea version is available. Download it before
  we start? 1. Update, 2. Keep this version." Wait for the answer. No answer is
  not approval. If declined, continue intake without repeatedly asking.
- `current`: silently continue to the unit question or next missing design topic.
- `ahead` or `development`: preserve the installed checkout. A published alpha
  is not automatically newer than unreleased development work; do not downgrade.
- `unknown`: report that the installed version cannot be identified if an update
  decision is needed. Offer the official release as a fresh download, not a
  verified upgrade. Do not infer an installed version from directory names or
  the current public tag.
- `unavailable`: say briefly that the update check could not be completed and
  continue with the installed version. Do not describe it as current. Do not let
  an offline connection or GitHub rate limit prevent furniture intake.

If Python is unavailable but browsing works, read the local `release.json` if
accessible and inspect the official GitHub releases page. Compare numeric
semantic versions, including alpha/beta suffixes; do not use string sorting or
assume `/releases/latest` includes prereleases. If neither comparison is possible,
follow the unknown/unavailable behavior. Use only the official
[AIkea releases](https://github.com/PatrickGrothOls/AIkea-skill/releases).

## After the user accepts

Download the exact offered release ZIP and its SHA256SUMS from the returned
official URLs. Verify the ZIP against the matching checksum. Extract into a new
version-specific directory, reject archive paths escaping that directory, and
preserve the previous installation, client projects, licensed CAD and saved
approvals. Never overwrite or delete those as part of a skill update.

Read the new entrypoint and verify its release identity before switching the
session to it. Keep the entire skill bundle on the same version; do not mix old
builders with new subskills. Continue with the already supplied project facts.
If account-level skill replacement needs a manual action, give the direct link
and concise guidance. Never claim persistent installation when only session
files were downloaded. Existing project migrations require a separate review;
updating the skill is not permission to rebuild an accepted design.

## Release packaging contract

`aikea/release.json` describes the installed bundle. Development source uses
`distribution: "development"` and `version: null`. The release packager must
stamp `distribution: "release"` and the exact semantic tag into the ZIP before
generating checksums. All sibling skills use that one bundle identity.
Older downloads without this metadata are unknown unless an installation
receipt verifies their exact tag and archive checksum; never label them current
by assumption. The public starter prompt and generated chat guide must perform
this check before their unit question when the next release is packaged.

The checker is advisory: it does not prove an installation is unmodified, a
release is fabrication-ready, or that an accepted update has been installed.
