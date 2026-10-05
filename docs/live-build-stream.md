# Live construction event stream

## Scope

First slice of Patrick's approved live-building experience: genuine placed part
events, atomic draft assets, saved-source rebuilds and a bounded read-only local
transport. The animated viewer and user-facing skill instructions are the next
stacked branch. Existing completed-review behavior remains unchanged.

## Work packages and current state

- [x] Add opt-in observer hooks to the shared panel builder.
- [x] Preserve generated child placement before building child parts.
- [x] Publish immutable, content-addressed GLBs and ordered atomic revisions.
- [x] Reconcile final geometry, removals and check results.
- [x] Watch stable saved inputs with one serial build at a time.
- [x] Retain geometry on failure and expose actionable check problems.
- [x] Serve draft assets on loopback without approval/upload/project-file routes.
- [x] Run targeted CAD, generator, transport and package regression tests.
- [ ] Integrate the animated browser consumer in the dependent viewer branch.

Backend implementation is complete and tested. The new watcher command is an
integration entry point; use it with the dependent viewer branch, not this base
branch's older bundled frontend. Nothing is deployed or manufacturing-approved.

## Verification

36 Python tests and four subtests passed across live publication, failures,
rotated nested frames, stable unchanged hashes, deletion reconciliation, local
transport boundaries, existing geometry/generator behavior and portable packaging.
All changed handwritten backend files are below 150 lines. The observer, CAD
placement, asset publication, transport and watcher have separate responsibilities.

## Audit log

1. Patrick requested real part-level updates and honest building/checking states.
2. Use optional observation hooks, preserving the ordinary build contract. Unknown
   parent frames defer to complete-tree publication rather than guessing position.
3. Preserve the existing formal approval boundary: live output is always a draft.
4. Split the implementation at the stream/viewer seam as required by the branch
   guidelines. The dependent branch adds the full user-facing experience.
