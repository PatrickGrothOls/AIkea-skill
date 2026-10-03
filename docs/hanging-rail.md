# Hanging rail installation

## Scope
Add a reusable oval hanging rail with two SL 322 supports, six declared fixing
bores, purchases and a cut-length record. Preserve the owning cabinet and its
other features. Replace README development-status copy with the intended output
and the checks each project completes.

## Current state
Official Hettich drawing verified: 30 x 15 mm rail, cut length inside width minus
7 mm; SL 322 article 70664, three 4 mm screws, holes at 0, 9.5 and 32 mm from the
lowest screw. Public DWG/DXF archive downloaded. STEP generation works, but the
browser blocks the generated download; Fusion capture failed. Exact CAD import
remains pending. Drawing dimensions can independently drive drilling.

The module and its cabinet integration are implemented. Seven focused rail tests pass, plus 11 export/hinge/shelf regression checks.
The real saved cabinet exports 35 identified parts with a 556.5 mm rail and
551.3495105 mm³ removed for six pilots. Exact CAD, purchased screw specification
and load confirmation remain explicit construction requirements. The package checker also resolves all 11 skills and links. Nothing has
been published or declared fabrication-ready by this integration test.

## Work packages
- [x] Inspect manufacturer drawing and CAD routes.
- [x] Implement reusable installation and geometry checks.
- [x] Exercise installation, purchases, drilled volumes and existing features.
- [x] Document agent usage and CAD acquisition.
- [x] Update README and review the focused diff.
- [x] Make the proven Hettich download procedure mandatory and reachable for every Hettich item.

## Audit log
- 2026-09-21: User requested the missing rail and two export fixes. Export fixes
  are committed in the parent branch. This branch owns the rail installation.
- 2026-09-21: The manufacturer drawing is the drilling authority. A simplified
  support preview must remain labelled as such until exact CAD is imported;
  no fabricated load rating or screw pull-out proof will be asserted.

- 2026-09-21: Reviewed the module boundaries: product geometry, placement/drilling,
  interference checking and assembly composition are separate classes; all new
  code files remain under 150 lines. The real integration preserves hinges,
  lights and shelves and exports valid identities through the existing viewer.

- 2026-09-21: Collision review caught the need to inspect child assemblies as well
  as direct panels. Reused the shared recursive tree walker and added a nested
  obstruction regression; it now rejects that collision too.

- 2026-09-21: Replaced the README experimental/not-ready paragraph with the
  intended cut-and-assemble output and per-project completion checks, as requested.
  Kept actual product-specific and desktop-delivery limitations visible; no gate
  or validation result was changed to support marketing wording.

- 2026-09-21: User required explicit reuse of prior successful Hettich downloads.
  Added a shared step-by-step guide with existing verified screenshots, exact
  article checks, browser recovery and disk/import finish criteria. Linked it
  from the main sourcing skill and all Hettich product references. Removed the
  older KA 5332 instruction that handed the portal to the user categorically.
  This documentation change does not claim the pending 70664 STEP was obtained.
