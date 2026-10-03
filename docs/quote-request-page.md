# Quote request page

## Scope

Connect Make it real to Patrick's approved quote-page layout. Local page only:
no database, upload, supplier contact, payment, or successful-submission state.

## Work packages

- [x] Create an isolated worktree from refreshed origin/main; install dependencies.
- [x] Implement the responsive page and current-design preview.
- [x] Implement services, paint preferences, postcode, timing and notes.
- [x] Preserve choices on return; support keyboard dismissal.
- [x] Build and run existing checks; verify desktop/mobile keyboard interactions.
- [x] Review responsibility boundaries and the diff.
- [x] Commit the page slice.

## Current state

The page is implemented. Browser checks confirm keyboard opening/dismissal,
field editing, independent choices, conditional painting details and retained
values on return. Requests remain disabled with explicit availability copy.
Build passes; all 68 existing viewer tests pass. The generated viewer bundle is
updated. No new dependency or persistence is introduced. Pointer verification is
limited by the browser tooling issue below; this is not a deployed update to the
existing Claude artifact or installed skill.

## Verification

- Desktop and narrow mobile layout: two columns become one; measured dialog
  scroll width equals client width (no horizontal overflow).
- Enter opens the page with heading focus. Escape, close and Back to design
  return focus to the original button. The viewer remains available.
- Service toggles, conditional colour entry, postcode, timing and notes work.
  Empty service selection exposes a prompt. Values survive reopening, including
  a round trip through separated-model inspection and restored assembled view.
- Request quotes is disabled and the form prevents submission; no send endpoint
  or payment flow exists in this slice. Browser shows no JavaScript errors; an
  existing Three.Clock deprecation warning remains.
- Screenshot: local-evidence/quote-request-page/desktop.png in the main checkout.
  It shows the actual older local wardrobe used for UI testing, not the mockup.
- New classes separate snapshot capture, dialog lifecycle, page composition,
  preference state and service presentation. All maintained changed source files
  are below 150 lines; largest is the 131-line existing viewer coordinator.
- Vite reports the large main bundle warning (1.64 MB); no new runtime libraries.

## Audit log

1. Patrick approved the generated quote layout and requested the page first.
2. Replace the current unavailable dialog with the page, retaining the underlying
   viewer and local form state. Submission infrastructure remains a later slice.
3. Patrick resumed after power loss. Setup survived; no application edits existed.
4. Preview comes from the current rendered design, with the actual viewer title.
   No material or dimension values are invented where the viewer lacks metadata.
5. The full-page native dialog retains form state and returns focus on dismissal.
   Rendering pauses while the page is open. The action stays mounted when hidden
   during detailed inspection so that returning to inspect does not erase inputs.
6. The existing review server rejected an old local model's stale bake evidence.
   UI checks use a temporary static harness with that existing 123-part model;
   this is UI evidence only, not new fabrication/presentation approval. No model
   or acceptance evidence was changed. The production gate remains unchanged.
7. The in-app browser's pointer automation is misaligned: a painting-checkbox
   click toggled machining instead. Keyboard activation, labels and controls work.
   Chrome is unavailable. Pointer verification remains limited by that tool issue.
