# Owned Korrekt components

## Scope and current state

Branch `feat/korrekt-component-feature`, based on `f04c8b5`. Implementation and review complete. Reuse the sourced mounting operation as an optional feature of any
horizontal panel assembly. Preserve caller-selected stations and unresolved
physical engineering questions.

## Work package and tasks

- [x] Declare exact foot/plate pairs with explicit placements and deck ownership.
- [x] Apply common mounting; retain previous cuts, purchases and children.
- [x] Record operations, installation and unresolved physical-fit requirements.
- [x] Register exact participants with the existing current-evidence mechanism.
- [x] Load source STEP files by registered checksum through generic review.
- [x] Verify feature composition/removal, changed inputs, source identity and ownership.
- [x] Run review skill and resolve findings.

## Evidence boundary

Removing the feature means rebuilding from the base with that feature omitted;
it removes its holes, purchases and requirements. Never fill holes in an already
machined result or remove another feature's material. The feature does not select
stations, redesign the base, adjust static source CAD or approve load capacity.
Its feature manifest scopes qualification; it does not generate a passing report.
Existing fingerprint/artifact checks reject stale evidence. Physical fit, screw
engagement, access, adjustment and deck support stay unresolved until checked.

## Audit log

1. Reuse the existing ordered AssemblyFeature protocol and scoped evidence format;
   no new component framework or parallel ready flag is needed.
2. Source hashes come from the saved wardrobe's verified 61854/70151 downloads.
   Read source files from project-local storage; do not redistribute vendor bytes.

## Validation and review

Five focused component tests pass. The earlier combined component/evidence run
passed 13 tests before the added purchase regression. All nine skill packages
validate. The review skill's independent specialist confirmed preservation of a
prior hole and unrelated hardware; current scoped evidence qualifies only its
participants, layout edits invalidate it, and physical-fit requirements remain
unresolved. The review found missing installed-purchase declarations; fixed by
explicit one-piece identities, preserving valid caller fastener choices.

A fresh saved project at `/private/tmp/aikea-korrekt-component-proof-20260912`
ran the ordinary generated loader, inventory and complete-assembly review. It
exported one deck and four unchanged manufacturer components (two feet, two
plates), counted both articles twice, and measured the expected ten-hole removal
volume. `proof.json` records hashes, inventory and open requirements;
`base-with-korrekt.glb` and its review report record the actual export. This is
local source-CAD integration evidence, not physical-fit or load approval.
