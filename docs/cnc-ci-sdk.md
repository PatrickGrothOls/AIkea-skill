# CNC test environment

## Scope
Install the declared AWS SDK in CI so the new offline intake tests collect in a clean environment. The desktop installer requirements remain unchanged.

## Work packages
- [x] Reproduce missing botocore from failed GitHub Actions logs.
- [x] Install the dedicated infrastructure test requirements in CI.
- [ ] Verify the combined feature suite in GitHub Actions.
- [ ] Merge this prerequisite before the CNC feature stack.

## Current state
The workflow now installs the same pinned SDK used locally. Existing failures were test-collection failures in test_cnc_intake.py and test_hosted_quote_session.py. No production dependency or AWS deployment is changed.

## Audit log
- 2026-10-01: Patrick authorized push, merge, a full review/fix loop, then publication. This prerequisite corrects the observed missing test dependency before merging the stack.
