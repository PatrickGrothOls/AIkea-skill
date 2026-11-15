# Private version receipts through Google Forms

## Scope

Branch `codex/download-receipts` starts from public `origin/main` at
`dd647329c655954d0150a1447d7a5272c0e06dea`. Keep the existing starter prompt,
GitHub release download and installer. Add only a model-submitted version receipt.

## Work packages

- [x] Create a separate Google Form with one required Skill version field.
- [x] Disable email collection, sign-in requirements and public response summaries.
- [x] Link its responses to an owner-only Google Sheet.
- [x] Submit one clearly labelled verification receipt and read back both columns.
- [x] Verify the public prefilled version link without submitting another receipt.
- [x] Add the receipt instructions to the existing getting-started flow.
- [x] Include the same instructions in future portable packages.
- [x] Verify the documentation links, package membership and privacy scan.
- [ ] Publish the instructions and verify the live getting-started page.

## Current state

The submission Form is published and accepts a version number without sign-in.
The linked response Sheet is owner-only. A live test produced exactly two
columns: Google's native timestamp and Skill version. The test version is
`verification-test-0.1.1`, so it can be excluded from actual receipts.

The existing starter prompt still points to this repository. Its getting-started
instructions now direct the assistant to submit the downloaded package's version
once. No release asset, checksum, installer command or dependency has changed.
The instructions also ship in the next portable bundle. The existing v0.1.1
bundle remains unchanged; its users receive the new step from the getting-started
page. Receipt submission is best effort and never gates setup.

Local validation passed: 7 portable-package tests and 4 subtests, a direct package
membership/link check, `git diff --check` and the privacy scan with zero findings.

Bug reporting is separate and remains subject to its existing activation work.
No download proxy, dashboard, database, Apps Script or automated setup-report
upload is part of this change. GitHub's own aggregate release counters remain
separate from this private receipt log.

## Audit log

1. Patrick explicitly chose the simple architecture: the model fills a Google
   Form with only the version number; Google supplies the date-time stamp and
   stores both privately. This supersedes earlier aggregate counters and the
   proposed Apps Script receipt receiver.
2. A dedicated receipt Form keeps downloads separate from bug/improvement reports
   that may be forwarded to GitHub. Download receipts never enter that workflow.
3. Native Form submission was verified end to end. Both Sheet permissions and
   its two-column contents were read back. No private owner URL is published in
   these instructions, and no extra respondent field is collected.
4. Keep the existing download route. Publish the new step in START_HERE.md so it
   applies to the current ZIP without replacing an already released archive.
