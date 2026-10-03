# Resolve missing drawer hardware

## Scope

Branch `codex/resolve-missing-drawer-hardware`, stacked on the existing Vilja
viewer work at `695abc7`. Preserve the six requested drawers and repair the
skill's recovery behavior when a locally registered runner does not fit. Source
the exact 400 mm Hettich candidate and record a repeatable download route.
Do not equate successful source retrieval with installed drawers or CNC approval.

## Current state

The missing STEP is **resolved**. Hettich article 9114274 was generated as STEP
AP214 in the manufacturer's browser portal, downloaded as `HETTICH_9114274.zip`,
stored in the existing Vilja project hardware library, and imported unchanged.
All four source solids are valid. Official installation PDF and alternate DXF/DWG
archive were also retrieved. The source hash and working visual route are in
the sourcing skill's new 400 mm reference.

Six drawers remain requested, zero installed. The next work is the exact 400 mm
installation profile and one complete drawer with compatible spacer/supports,
fixings, captured 6 mm HDF bottom and one CNC face per panel. Then repeat to six
and rebuild the same wardrobe. Existing hinge fit and fabrication gaps remain.
This branch closes sourcing recovery, not the whole furniture build.

## Work packages

### WP1 — Recover the missing source

- [x] Recheck official 400 mm article, minimum depth and installation drawing.
- [x] Inspect the actual browser session rather than assume registration.
- [x] Generate, download and store exact STEP with provenance and vendor notice.
- [x] Import unchanged source and verify native bounds and solid validity.

### WP2 — Make recovery part of the reusable skill

- [x] Route missing/incompatible hardware into active sourcing.
- [x] Preserve requested feature counts and distinguish preview from completion.
- [x] Document tool-aware user handoff and automatic return to the owning builder.
- [x] Save the working exact-product route with real guidance screenshots.
- [x] Validate skill metadata and links; review diff and source-file exclusions.
- [x] Commit this coherent sourcing slice locally.

### WP3 — Continue the original Vilja drawer build

- [ ] Classify exact 400 mm members and reconcile installation datums/fixing axes.
- [ ] Resolve hinge clearances and depth-compatible spacers/supports; the existing
  486 mm article 13952 cannot simply be reused inside a 416 mm opening.
- [ ] Implement one complete installation through shared construction, including
  material-specific fixings, captured HDF bottom and single-face machining.
- [ ] Verify its exact hardware, mounting cuts, closed/open travel and collisions.
- [ ] Repeat to six, reconcile the complete BOM and regenerate the viewer.

## Validation evidence

Local source:
`../vilja-skill-trial/local-evidence/project/hardware/hettich/ka-4532-silent-system/9114274/`

`source-record.json` records the archive and unchanged STEP checksum;
`native-inspection.json` records four valid solids and native bounds. Installation
is explicitly marked unverified. Downloaded CAD remains excluded from Git.
Both changed skills pass `quick_validate.py`; all 26 relative links in the changed
entrypoints/references resolve. This validates packaging, not agent behavior.
The real browser retrieval and exact-CAD import are the execution evidence.

## Audit log

1. 2026-09-15: Patrick explicitly required persistence on missing hardware and
   enabling this recovery in the skill. The change preserves required source/fit
   checks while making resolution an active task rather than dropping drawers.
2. Live official product and portal verify 400/404 mm for article 9114274. The
   portal generated STEP AP214 without registration/agreement prompts in this
   session. The earlier assumed registration blocker is superseded by this test.
3. Direct access to the temporary ZIP returned 403; supported browser download
   succeeded. The stable product page and visible steps are saved, not the
   expiring URL. No access-control bypass or agreement acceptance was performed.
4. The source-store command rejected a project-local `.gitignore` containing only
   `*`. It was normalized to the store's expected blanket-ignore content (plus
   its self-exception); vendor files remain ignored. No public source was added.
5. Native import proves four valid solids, not fitting or machining. Preserve the
   original six-drawer task and carry the exact 400 mm installation work forward.
6. The original Vilja build agent resumed with the stored exact STEP and official
   installation drawing. Its next bounded slice is exact member/datum/fixing
   verification on its own branch before one complete drawer installation.

7. During the subsequent viewer-control work, the resumed drawer agent stopped
   on an account usage limit. Its branch codex/ka4532-400-profile and checked plan
   are saved in vilja-skill-trial; it reported source/provenance verification but
   no production code change yet. Do not describe that agent as still running.
