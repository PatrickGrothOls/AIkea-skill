# Current-host drawer proof

## Scope and current state

WP5b proof slice on `feat/drawer-host-proof`, based on reviewed `e72d168`.
Implementation, focused tests and independent review pass. The full Python
regression finished with two stale test-fixture failures; their repair is tracked in
[shared-construction regressions](shared-construction-regressions.md). The generated KA 4532 proof will load the current
host declaration and check actual named support solids, bay limits, and the eight
fixing support points. Exact purchased-source, articulation, motion and collision
checks remain in force. Missing longer screw and pilot authority remains blocked.

Direct legacy checker calls retain their existing canonical-host fallback. The
project proof command always supplies the current saved host; it does not infer
that declaration from stale layout or evidence files.

## Work package and tasks

- [x] Pass the current host through proof orchestration and installed checks.
- [x] Resolve actual participants and the declared front, including inset bays.
- [x] Check actual inside planes, drawer bounds, and material at fixing positions.
- [x] Prove translated/renamed/inset custom hosts, current-source changes, and
  negative shifted support, missing material and stale reservation cases.
- [x] Verify legacy proof regressions and source identity/motion checks.
- [x] Run the review skill and the inherited-file responsibility review.

## Validation

- 64 focused host, source, installed fixing, movement, orchestration and CLI tests
  passed before the end-to-end run exposed the freshness and mesh-bound issues.
- After the fixes, 15 focused regressions passed, including an actual saved custom
  project generating both GLBs and a valid movement proof with supplied test CAD.
  A same-size/same-mtime host edit invalidated the new proof on rerun.
- Independent review reproduced and rechecked the stale-source issue. The old
  bytecode stays unchanged, current source is loaded, and import state is restored
  after invalid source. A final review verified mesh-invariant tangency while a
  genuine 0.001 mm overlap remains detected. No open findings remain.
- Both inherited checkers received [scope review](reviews/drawer-host-proof-scope.md).
  Their new host-agreement helpers remain within those responsibilities.
- All nine skill packages and their links validate.
- [x] Record the full Python run at `87bada6`: 671 passed, 72 subtests passed,
  five skipped, two failed in 1580.31 seconds. The two failures are a missing
  copied requirement template and an obsolete frameless host fixture; see the
  linked follow-up for fixes and rerun evidence.

This is local software evidence with test CAD, not a new physical product trial,
remote CI result or manufacturing approval.

## Audit log

1. Use the saved current `DRAWER_HOST` contract through the existing loader. This
   applies the approved common input boundary to installed-hardware proof.
2. Read the host's front reference independently of a panel's bounding-box front,
   so a declared inset bay can be checked without pretending the panel starts there.
3. Actual support material is checked at the source-derived fixing axes. The
   small interior probe is a numerical geometry check, not screw/pilot authority.

4. Review reproduced stale bytecode after same-size/same-mtime host edits in both
   loading routes. A shared project runtime now reads current assembly source,
   including imported project helpers. It preserves the old review import path,
   restores import state after errors, and leaves existing bytecode files alone.
   This repairs the current-input boundary needed by the proof; it does not make
   project-authored Python a security sandbox.

5. The saved-project run found viewer tessellation inflating fixed-runner bounds
   by about 0.001 mm, creating false swept conflicts at touching board faces.
   The existing sweep checker now obtains CAD-surface bounds with triangulation
   disabled. This retains its collision tolerance and conservative sweep method;
   it does not exclude additional part pairs.
