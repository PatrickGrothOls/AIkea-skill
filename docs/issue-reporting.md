# Browser issue reporting

## Scope
Let an AIkea user approve a report in chat and have their agent submit a Google
Form. A prefilled form is the fallback. Users need no GitHub credentials or
knowledge. Google hosts the form and a private Apps Script posts the issue.

## Work packages
- [x] Add discoverable reporting instructions and portable entrypoint routing.
- [x] Build an offline report/prefill helper with explicit approval and configuration gates.
- [x] Build the Google Form receiver with fixed repository, bounded intake and no blind retries.
- [x] Test report generation, privacy screening, deduplication and failure behavior.
- [x] Document operator activation and review the final diff.
- [ ] Activate the hosted form and verify one approved synthetic submission.

## Current state
Implemented on codex/issue-reporting. Local checks pass: 24 Python tests plus four
portable-package subtests, six receiver tests, skill discovery and skill validation.
Receiver tests are included in CI. The private Google project has the three source
files and explicit permission manifest saved. Google authorization is waiting at
an unverified-app warning; form creation, credential setup and live delivery remain
pending. Distributed configuration is deliberately `not_configured`.
No public issue has been posted and hosted reporting is not yet available.
The local portable archive built successfully from commit `2a9e6b0`; its reporting
instructions, helper and inactive configuration were verified inside the archive,
with operator infrastructure excluded. Privacy scan reports zero findings.

## Audit log
1. Patrick approved browser-based reporting with a prefilled-form fallback,
   invisible GitHub integration and no dedicated server.
2. Implement that agreed route using Google Forms and Apps Script. Keep the
   GitHub credential in private Script Properties, outside the distributed skill.
3. Activation is separate from local implementation: no public endpoint or new
   credential scope is created without the required account approval.
4. Live Apps Script editing rejected static class fields. Replaced them with
   static getters; Google accepted the saved sources and receiver tests still pass.
5. Automatic approval review blocked saving the explicit Google permission
   manifest. Ask Patrick to approve Forms access, trigger management and external
   requests before continuing setup. No credential or authorization was supplied.
6. Reviewed and committed the implementation, then built and inspected a local
   portable archive. It is a packaging check only, not a published release.
7. On 2026-10-07 Patrick explicitly approved Forms, submission-trigger and external
   request permissions. Saved the matching manifest. The in-app browser did not
   expose the authorization popup; Chrome opened it successfully. Google displayed
   an unverified-app warning for this private script, left for Patrick to handle.
   No Google authorization, form creation or GitHub delivery was confirmed.
