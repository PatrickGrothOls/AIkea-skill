# Drawer visibility fixture and layout policy

## Scope

Restore the existing drawer visibility integration test after the new compact
layout gate. Keep the production gate intact and the fresh Claude download
unchanged. The elevated drawer in this synthetic fixture deliberately tests
placement, rather than prescribing a normal furniture layout.

## Current state

Public CI identified one fixture that lacks the required layout record. Its
actual assembly paths and part bounds now supply a clearly synthetic client
exception for the deliberate elevated placement. Both targeted tests pass: the three-state visibility export and the
missing-policy rejection gate. No production code or installer bytes changed.

## Work packages

### WP1: Repair the fixture
- [x] Identify the failing test and retain the production validation.
- [x] Obtain the required independent scope review for the existing long file.
- [x] Give the elevated test scenario an explicit synthetic request and record.
- [x] Run the visibility test and the missing-policy rejection test.

### WP2: Review and deliver
- [x] Review the diff and record the verification results.
- [x] Commit the isolated test correction.

## Audit log

- 2026-09-21: The public run fails before exporting the visibility fixture because
  its installed drawer has no layout-policy record. Updating this test supports
  the user's requested enforced defaults; weakening the gate would contradict
  them. No furniture layout or Claude acceptance input will be changed.
- 2026-09-21: Independent scope review found the existing integration test coherent
  despite exceeding 150 lines. Its common scenario, placement reports and three
  visual states belong together. Keep this repair limited to fixture validity;
  splitting assertions is optional future cleanup, not needed for this failure.

- 2026-09-21: Both targeted tests passed in 842.46 seconds in the direnv CadQuery
  environment. The valid explicit test exception exports all three states,
  while the separate missing-policy test still blocks export. Diff review
  confirms only fixture setup, fixture data and this plan changed.
