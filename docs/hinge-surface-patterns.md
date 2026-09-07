# Surface-based hinge patterns

## Scope

Implement Patrick's instruction that a hinge places a drilling pattern on a
supplied surface. Keep pattern definition and placement independent of door
construction, receiving solids and the cabinet planner. This focused branch is
stacked on `codex/framed-door-design`, commit `59d8b58`, as
`codex/hinge-surface-patterns`.

## Work packages

- [x] Separate generic hole dimensions and surface placement from the NC70 profile.
- [x] Adapt the existing slab workflow to the surface operation without changing cuts.
- [x] Document direct use, receiver ownership and the remaining legacy adapter scope.
- [x] Verify rotated datums, multiple receiving layers and left/right compatibility.
- [x] Finish regression and package checks and review the local commit slice.

## Current state

Nine focused hinge/surface tests pass. The full suite produced 516 passes,
72 passing subtests and five skips, with five localhost server tests blocked
by sandbox socket permissions. Rerunning their two files with localhost access
passed all six tests, clearing every failure. In total, 521 distinct tests pass
and five remain skipped. All 11 skill/link checks and the framed-skill metadata
validator pass; the installed framed-skill reference resolves to this operation.
The pattern can be placed without a receiving solid; physical validation remains
the owning assembly's responsibility. Existing pilot assumptions and cabinet
grid behavior are preserved. The current wardrobe is unchanged.

All new code files are under 150 lines and each owns one concern: generic
drilling geometry, product hole dimensions, or regression checks. The existing
machining adapter is reduced to 67 lines. No new door taxonomy, material
selection or global hardware dependency is introduced.

## Audit log

1. Patrick explicitly rejected a hinge depending on a particular door
   construction. A planar datum and hardware offsets are sufficient to lay out
   the holes; material checks must not become a door-style requirement.
2. Separate `SurfaceHolePattern` from `RiexNc70CupPattern` so other hardware can
   use the operation without importing this hinge profile. The existing slab
   adapter supplies its own datum and preserves its established pilot sizes.
3. Use actual cutter-volume comparisons to prove the left/right adaptation and
   that the same pattern removes the same material from one board or two layers.
   An OCC cylinder's parametric axis may reverse, so the rotated-datum test
   checks occupied volume and endpoints rather than assuming its axis sign.
4. Document the legacy full-door planner and movement limitations explicitly.
   This change makes drilling reusable; it does not claim that every existing
   cabinet template automatically accepts every possible leaf assembly.
5. The full regression's only failures were `socket.bind` permission errors in
   temporary viewer test servers. Re-run just those two files with the required
   access rather than repeat the expensive geometry suite or alter production
   code to accommodate a sandbox limitation. All six tests passed in 3 seconds.
