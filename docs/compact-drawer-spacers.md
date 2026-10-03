# Compact drawer spacers

## Scope
Clarify the existing mandatory spacer requirement: compact bought spacers or
manufactured strips/blocks, with actual attachment and loaded-drawer checks.

## Current state
The drawer skill entrypoint and shared installation contract are updated on this
branch. This does not change the displayed prototype or qualify a replacement
spacer; installed main skills remain unchanged until integration.

## Work packages
### WP1 — Save the corrected default
- [x] Require compact spacers and independently calculated side offsets.
- [x] Require exact runner-to-spacer and spacer-to-cabinet fixing preparation.
- [x] Retain loaded-drawer, full-extension, material and one-face checks.
- [x] Prevent silent full-panel fallback; larger supports need a reasoned design choice.
### WP2 — Verify and hand off
- [x] Validate the skill and review the focused diff.
- [x] Prepare the focused commit and notify the existing drawer agent.

## Audit log
1. Patrick rejected the large inset panels and requested small strips adequate
   for the loaded drawer. The existing skill required spacers but did not bound
   their form; this closes that omission without inventing dimensions or loads.
2. Keep the detailed rule in the existing installation contract and make it
   discoverable from the skill entrypoint. Geometry and load evidence remain
   separate from the policy change.
