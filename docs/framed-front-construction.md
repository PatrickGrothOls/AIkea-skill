# Shared framed-front construction

## Scope and current state

Branch `feat/framed-front-construction`, based on reviewed `3817849`.
Migrate the optional applied-frame helper from `c08f1b0` onto shared panel and
surface-pocket operations. Preserve explicit layer identity and whole-leaf placement.
Implementation, focused tests and independent review are complete. Layered hinge
and parent moving-state integration remain a separate component slice.

## Work package and tasks

- [x] Reuse validated rectangular front parameters and idempotent project setup.
- [x] Emit an editable common recipe with explicit layer materials and pocket cut.
- [x] Declare adhesive and parent mounting as unresolved construction requirements.
- [x] Document optional use, customization, machining and evidence boundaries.
- [x] Verify geometry/contact, editable recipes, common checks and nested ownership.
- [x] Run the review skill and close its findings before committing.

## Audit log

1. Reused the existing optional front recipe rather than introducing a new door
   engine. Its original direct boolean is replaced by the reviewed shared pocket.
2. Represented adhesive as an unresolved attachment requirement. A face-to-face
   relationship removes no material, and claiming a validated machining joint for
   it would misrepresent the shared cut contract. No adhesive rating is introduced.
3. Kept absent material identity explicit and allowed different selected products
   for the two layers. The old dimensions are test examples, not defaults.

## Validation and review

28 focused tests passed across the framed recipe and shared pockets; ten skill
packages and their discovery/document links validate. Common result checks reject
stale cutters; geometry checks cover analytic volume, layer contact, materials,
nested placement and editable recipe output. Initializer conflicts retain authored
project files. The inherited CNC-limit fixture now tests 2497 mm, beyond the current
2496 mm profile limit; the limit itself was not changed.

The review skill's independent testing specialist found no issues. An asymmetric
520×760 mm front with 16+6 mm layers and 33/67/81/42 mm borders matched independent
box/cylinder opening geometry with zero difference, 127690.902664 mm² contact and
no layer overlap. Inventory retained two full-size blanks and distinct materials.
A fresh complete-review CLI exported the nested front as exactly two physical
parts without test runtime imports. Evidence is in
`/private/tmp/framed-front-review-iawj9tjr`. Attachment and parent mounting remain
explicitly unresolved; layered hinges and moving states are the next slice.
