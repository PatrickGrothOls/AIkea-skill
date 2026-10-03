# Desktop 4 release review and publication

Historical record: this presentation was superseded by [AIkea Skill v0.1.0](aikea-public-release.md) at Patrick’s request. The review evidence below is retained unchanged.

## Scope
Publish the merged Make it real/CNC source-request feature as a public desktop
candidate after independent review and correction. AWS IAM recovery and hosted
service activation remain deferred by Patrick's explicit instruction.

## Work packages
- [x] Push branch documentation and merge feature PRs #10–17.
- [x] Freeze shared sourced contracts for independent simplicity/stability/security lanes.
- [x] Resolve round 1 preview-size, shared-preference ownership and packaged availability findings.
- [x] Resolve round 2 missing shared-source and cross-site framing findings.
- [x] Complete fresh round 3 with all three lanes passing.
- [x] Complete exact-revision full CI: all nine jobs pass.
- [x] Merge corrective PRs #18–22.
- [x] Build and verify the 614-file installer manifest.
- [x] Publish desktop 4 and verify its downloaded assets.
- [x] Update public entrypoint links and include this ledger and raw reports in the publication commit.

## Current state
All final review lanes and exact-revision CI pass. Desktop 4 is publicly published;
an anonymous HTTPS download matches the expected checksum and all manifest entries. Hosted customer upload is unavailable:
AWS permissions/deployment recovery and live identity/S3/inbox proof remain
explicitly deferred. No AWS change, customer invitation or real quote was sent.

## Review snapshots and adjudication
Base for all rounds: 5db04d7, the prior public main.

| Round | Target | Simplicity | Stability | Security |
| --- | --- | --- | --- | --- |
| 1 | 6de7235b087c3a05e8b268484c305fd76c077329 | FAIL | FAIL | PASS |
| 2 | dec32663814818a134cad6af9357d34c7d698fc5 | PASS | FAIL | FAIL |
| 3 | be17becccad0d0b23ae5c383e535e89e072ab0df | PASS | PASS | PASS |

All reviewers start fresh from the same frozen requirements/policy packet and
full integrated unit, without earlier verdicts or implementation conversation.
Reports retain their original verdicts; later fixes do not rewrite history.

1. Accepted shared preference/image-parser coupling: common QuotePreferences
   now serves local and hosted boundaries without fabricating preview bytes.
2. Accepted reproducible high-DPI preview rejection: only the PNG thumbnail is
   resized before submission freezes; server limits remain unchanged.
3. Accepted missing installed availability instructions: one canonical packaged
   guide documents unavailable hosted service, invitation/native/Git prerequisites
   and deferred painting/installation outreach.
4. Accepted reproduced missing untracked shared helper: Git working-copy inventory
   includes permitted nonignored new shared files through existing exclusions.
   No customer files are staged and no imports are executed.
5. Accepted missing browser frame protection: all viewer responses carry self-only
   ancestor headers. A real HTTP probe confirmed absence; browser clickjacking was
   not executed, and exploitability is not claimed as browser-verified.

## Verification and limits
- Baseline merged-main CI 36834835897 passed after rerunning one PyPI download timeout.
- Final exact-revision [CI 36839723923](https://github.com/PatrickGrothOls/AIkea-skill/actions/runs/36839723923): 1,140 Python tests passed, six skipped, 20 subtests passed; all 73 viewer tests and reproducible build passed.
- Local viewer: 73 tests pass; production bundle rebuilt and committed.
- Source correction: 31 focused tests pass. Framing correction: 11 real-loopback
  and existing viewer decision/artifact tests pass.
- Package: 11 skills, 614 manifested files; installer PackageIntegrity verifies
  version/source and every included file. License and third-party notices retained.
- Actual Safari UI check uses real quote components with a synthetic preview and
  disabled fake delivery: Make it real opens; painting selection and typed postcode
  survive design/back navigation; sending disabled, no-contact text present.
  This is not a real model-render, OAuth or uploaded-request test.
- Local full suite: 1,130 passed, six skipped, 20 subtests passed. It ran while later source edits occurred. Treat it as
  supplementary evidence, not exact frozen-revision proof; CI supplies that proof.
- Fresh complete CAD/Blender installation and every desktop product are not
  revalidated here. Existing setup acceptance gates remain explicit.
- Uploaded customer source remains untrusted; path filters are not content-wide
  secret detection. Review selected source before sending; never execute customer
  archives with personal credentials/network access.

## Audit log
- 2026-10-01: Patrick authorized push, merge, full review loop and public publication,
  while deferring IAM setup. Public publication is the skill installer; it does
  not open registration or activate the unavailable hosted service.
- 2026-10-01: Corrective changes stay in small stacked PRs with individual branch
  docs. Generated bundles are rebuilt, not hand-edited. No changed handwritten
  production source exceeds the 150-line review threshold.
- 2026-10-01: Reviewer lanes share one source contract and independently inspect
  the entire integrated unit. Reproduced findings are fixed, then a new fresh round
  reviews the new revision. Deferred operational checks remain distinct from tests.

Raw reports and identical per-round contracts are preserved under [reviews/desktop4](reviews/desktop4).

Merged code is `b531dc7cd96f21812a934462e8cc538b6a7d3e36`; its tree is byte-identical to reviewed `be17becccad0d0b23ae5c383e535e89e072ab0df`.

## Published artifact

[Desktop 4 release](https://github.com/PatrickGrothOls/AIkea-skill/releases/tag/v0.1.0-desktop.4)
is public and retains the existing prerelease designation. The tag and package
manifest point to reviewed/tested commit `be17becccad0d0b23ae5c383e535e89e072ab0df`,
which is an ancestor of main. Subsequent publication documentation does not change
installer contents.

SHA-256: `82f5716504f18b0bfa3ae5e950499b73b1cf4aa7ef7a3857e49016c210af6060`.
Anonymous public ZIP and checksum downloads succeeded and all 614 archive members
matched their manifest hashes on 2026-10-01. Source/public branch documentation
and raw review reports are in this repository; repo-wide docs are not duplicated
inside the skill installer. Its canonical CNC availability guide is included.
