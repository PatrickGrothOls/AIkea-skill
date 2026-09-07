# Upright assembly review

## Scope

Preserve the orientation already exported in CadQuery GLBs. The viewer currently
adds a second 90-degree rotation, making upright furniture lie on its back.
This branch is stacked on the composable-furniture work; PDF design artifacts
remain in their own evaluation project.

## Current state

The exported root quaternion is `[-0.7071067811865475, 0, 0, 0.7071067811865475]`.
It maps CAD height (Z) to glTF height (Y). The viewer's additional scene rotation
is removed. All 23 viewer tests pass, the portable viewer rebuild succeeds, and
a fresh browser tab shows the identical GLB upright before any orbit gesture.
The default-view screenshot is saved at
`/private/tmp/aikea-composition-forward-test/reviews/screenshots/bench-upright-default.jpg`.

## Work packages

- [x] Reproduce the incorrect default orientation with an unrotated browser view.
- [x] Inspect the actual exported GLB transform and identify the duplicate turn.
- [x] Remove the viewer's additional coordinate conversion.
- [x] Run viewer checks and rebuild the portable viewer assets.
- [x] Verify the same GLB stands upright in a fresh browser view.
- [x] Review and commit this isolated fix.

## Audit log

- 2026-09-07: Patrick reported that the shown model lay on its back. The original
  report had withdrawn an orientation finding because Patrick was manually
  rotating that earlier view. A fresh bench prototype view and its actual GLB
  root transform now independently establish the duplicate conversion. Remove
  only the additional viewer rotation; preserve the exported physical model.
- 2026-09-07: The unrelated open bench brief also omitted the original wardrobe's
  plinth and doors. A separate subagent is rebuilding the actual PDF design.
  Correcting orientation alone does not resolve that scope error.
- 2026-09-07: `npm --prefix viewer test` passed 23 tests, and
  `npm --prefix viewer run build` regenerated the bundled runtime. Direct CUA
  browser capture of the same GLB on port 8773 confirmed the expected upright
  bench and tower without any orbit gesture. No physical geometry was changed.
