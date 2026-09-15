# Vilja fresh build

## Scope and current state

Restart the four-bay Vilja wardrobe using the updated local skills. The previous agent stopped after an incomplete drawer prototype. Its project remains evidence only, not a design implementation to copy. Fresh worktree starts at 60f32aa plus reusable exact runner profile 3d18301. Environment reuses the existing CadQuery venv.

## User brief

Use this worktree's `aikea/SKILL.md` and routed local skills, not the older globally installed bundle. Read the actual skill instructions before designing. Make a complete assembly with shelves, drawers, hinged doors, adjustable-foot base and lighting. Resolve routine arrangement choices yourself and record assumptions.

Original room authority: `/Users/patrickolsen/Desktop/Projects/Vilja værelse/wardrobe/core/global_spec.py` and `wardrobe/core/specs.py`. Read these measurement/specification files only; do not reuse the original builders or the unrelated untracked aikea.yaml. Known outside envelope: width 2475 mm, depth 450 mm, left height 2374 mm; flat top to X=990 mm, then straight slope to right height 724 mm at X=2475 mm. Base total height 95 mm. Verify coordinate conventions against source.

Preserve four bays, six drawers of varied heights and thirteen adjustable shelves as the review scope. The old distributions (drawers 2/2/1/1 and shelves 5/4/3/1) were proposals: arrange anew if needed for fit. Carcass 16 mm, doors 18 mm, backs 16 mm; 6 mm HDF drawer bottoms captured in four grooves. Base deck 15 mm was the previous deliberate proposal to accommodate an 80 mm foot below a 95 mm base: verify the actual hardware stack before adopting it.

Mandatory requirements:

- Adjustable Korrekt feet and mounting plates, deck and front kickboard. Never substitute the retired timber brace/rail plinth. Verify exact source article pairing and drilling.
- Default full usable-height System 32 rows: 5 mm diameter, 32 mm pitch, 13 mm blind depth, 37 mm front/rear setback, 100 mm end offsets as defined by the current shared profile. Original 64 mm spacing is superseded by the user's 32 mm choice. Preserve remaining exterior skin.
- Adjustable shelves rest on four selected pins on matching rows. Move shelves to another 32 mm row to avoid hinges. Near-full usable depth still requires front AND rear fitting clearance; the retired 414 mm proposal had zero rear clearance and must not be reused blindly. Keep width, coating, actual stock and room tolerances explicit. Shelves may visually overlap the light line, but must not collide with physical profiles or hardware.
- Selected pins: Røverkøb Hyldebærer 5mm, 24 stk., article 16415, LN 206.129.2, https://www.roverkob.dk/hyldebaerer-5mm-24-stk . Only diameter is confirmed; 13 mm hole depth is not pin insertion length. Do not substitute another product's dimensions. Source missing dimensions or label visual approximation explicitly.
- Regenerate panels from current operations; remove retired shelf-relative drilling. Do not remove valid shared grid or current hardware holes.
- Shelves are not Cabineo-fixed by default. A deliberate fixed shelf exception uses concealed underside pockets. Cabineos must be flush to the joining edge, correctly seated, with brass receiver inserts counted one per connector.
- Every drawer includes actual fixed and moving runners, screw holes and necessary hinge-clearance spacers. Use depth-compatible exact Hettich KA 4532 9114274 (400 mm nominal, 404 mm minimum cabinet depth) through the local verified profile. Preserve source geometry; nominal/source dimensional differences require explicit treatment.
- Use compact strips/blocks or appropriate purchased spacers. No full extra inset side-panel assembly just to mount runners. Check runner-to-spacer and spacer-to-cabinet fasteners, engagement, material and drawer travel.
- One broad machining face per part wherever viable. Qualified through pilot holes are allowed; neat 3 mm exits inside drawers can remain open. Plugs on visible surfaces are optional finishing operations and do not restore screw grip. Only when no viable one-face option exists consider a guided drill template or registered CNC flip fixture. Do not convert precision connector pockets to through holes to evade checks.
- Recessed lighting on cabinet right sides, continuing along sloped top panels. Include modular lighting components and actual channels/cuts.
- Hinges and other purchased hardware must be present, with actual fixing holes and required clearances. Do not reuse an out-of-limit hinge profile silently. Check shelf/door/runner motion and all attachment relationships.
- Finished viewer uses the bundled headless Blender workflow and genuine CAD geometry; no render-only edge details. Explosion can use inexpensive materials, but all parts and lights must remain inspectable. Hardware stays on its parent unless that parent subassembly is being exploded. Door visibility toggle and compact explosion slider.

## Reusable source assets

Untouched vendor CAD and source records may be read from the hardware cache only:
`/Users/patrickolsen/Desktop/Projects/AIkea-skill/.worktrees/vilja-skill-trial/local-evidence/project/hardware/`.
Copy necessary vendor inputs into this run with provenance. Do not read/copy the old project's builder code, derived assembly geometry, review models, placements or outputs as implementation input. The KA4532 400 mm profile is already in this local skill bundle. Candidate purchased 350 mm spacer: Hettich 9135703; source authority and assembly suitability must be verified. A compact manufactured spacer is allowed.

## Work packages

- [x] WP1: Read local skills; verify envelope, dependencies and source hardware; establish a fresh project and arrangement.
- [ ] WP2: Generate all carcasses, foot base, doors, shelves, lighting and six complete drawer assemblies with compact supports.
- [ ] WP3: Validate actual subtractive geometry/material removal, one-face policy, obsolete-hole absence, fixing alignment/engagement, fit tolerances and motion. Distinguish provisional source or load assumptions from proven geometry.
- [ ] WP4: Export full assembly STEP/GLB and part/BOM data; confirm all six drawers and hardware exist in exports. Run appropriate tests and skill-based review after each work package.
- [ ] WP5: Produce final viewer assets and a concise evidence report; parent reviews before replacing the single browser viewer.

## Execution rules

Use `direnv exec .` for commands/scripts and the existing venv. Limit numerical threads to one. One heavy CAD/render operation at a time on this 8 GiB Mac. Do not open browser tabs or run a persistent viewer; parent owns delivery. No push, merge, deployment or global skill installation. Follow project OOP/separation-of-concerns conventions and create coherent commits. Update these task checks and audit entries with actual evidence, not intended progress.

## Audit log

- User requested a new agent from the beginning after the crash, using all updated skills. Preserve old files; no live previous agent remained to delete.
- Created isolated fresh worktree from the latest local policy branch and added only the reusable exact runner-profile commit. No old assembly code or geometry imported.
- Six drawers/thirteen shelves retain the previous review scope; layout may change to satisfy the supplied envelope and current policies. Fitting and sourcing gaps must be addressed explicitly, never hidden behind a successful render.
- Fresh worker loaded local aikea, design-furniture, drawers, doors, lighting, hardware sourcing, review and materials instructions. Supplied measurement modules confirm 2475 x 450 mm, 432 mm carcass/416 mm interior and 95 mm base; original 64 mm drilling is intentionally superseded.
- WP1 source check: unchanged exact 9114274 source passes all twelve fixed/moving opening checks. Report: `local-evidence/fresh-project/reviews/ka4532-400-source-check.json`. Parent separately confirmed eight profile tests and four grid tests.
- Arrangement proposal within the authorized routine design discretion: four 598 mm carcasses on 602 mm pitch, starting at X35.5 mm. Four 600 mm left-hinged leaves use the exact 17 mm K6/H0 overlay, with 2 mm between leaves. Side fitting strips occupy remaining width; top fitting allowance is 5 mm. Six drawers remain 2/2/1/1, shelves 5/4/3/1. These are authored assumptions, not new site measurements or material approval.
- Compared sourced Hettich 9135703 compact 350 x 67 x 25 mm spacer: published 20 kg limit, native DXF/ACIS only. Selected an explicit 400 x 80 x 25 mm birch strip proposal instead, with real runner and cabinet fasteners/pilots; physical load and stock qualification remain open.
- WP1 skill review: current local shared contracts installed into a blank project; only permitted vendor source inputs copied. No prior builder, placement, derived geometry or old review was used. Every drawer remains in scope while its complete source and mounting construction are checked.

## Current checkpoint

- Current inspection export contains four bays, six complete drawers, thirteen shelves, two base deck sections, sixteen exact Korrekt plate/foot pairs and nine emitters. Parent verified compact stacks and the neutral-white interior illumination in the single viewer.
- The current preview still contains the rejected NC70-driven narrow cabinets and two side fitting panels. It is preserved for inspection while exact replacement Blum hardware is integrated; it is not the final intended full-width design.
- All 86 manufactured parts have individual STEP/DXF exports. Full assembly STEP and GLB exist. DXF is perimeter-only; manufacturing release, full closed collision audit and Blender presentation remain unfinished.
- Actual wide-front sweep fails against the old NC70 door. This is an active design failure, not a passed motion check. Exact Blum71B7550/173H7100 ACIS sources and official installation authority are saved; native STEP conversion and replacement mounting/pose verification remain open.
- Shared review/completion routes now enforce complete drawer-layout evidence. Project source declares the six structural fronts and their measured floor/stack/cap relationships; next regeneration must pass that gate.
- Disk free space is approximately1.76 GB. No large isolated FreeCAD runtime was installed. Existing Fusion access was denied by Computer Use and the live Blum CAD portal requires login; direct STEP download or an approved existing converter is the immediate source-format dependency.
- Materials remain proposals: painted MDF, birch plywood supports/decks and HDF bottoms. No supplier finish or load approval is implied.
- Exact runner source axes are checked at all twelve openings. Installation uses the complete native pair at a common 2 mm inset; fixed axes are 39/167/231 mm from cabinet front and moving axes 37/165/291 mm from drawer front. The 0.2 mm native/nominal side spacing difference is explicit.
- Shelf pins, connector bodies and screw visuals are dimensional illustrations. Purchased hinge, runner and leg bodies use unchanged source CAD. A 13 mm blind grid is not claimed to establish pin insertion length.
- Physical qualification still requires stock/load, pilot and screw compatibility, base/cabinet and wall anchoring, fitting-panel/kickboard fixings and lighting electrical routing. Full assembly exports do not establish fabrication readiness.
- Shared lighting review uncovered missing hardware ownership. The feature now consistently declares its mounting panel and review validates it, so light bodies follow their parent during inspection explosion. Focused regression checks are pending the serial CAD run.

### User correction: compact drawer stacks

- [x] Stop the superseded tall/gappy layout before further export/bake.
- [x] Derive shallow drawer heights from 3 mm floor, inter-drawer and cap-shelf gaps.
- [x] Keep cap shelves on System32 rows324/164; move runner axes independently to54/207.75 or54 mm.
- [ ] Regenerate and audit all six revised drawers and thirteen shelves.
- [ ] Replace the parent's existing inspection asset and complete its final presentation.

The user explicitly rejected tall drawers and exposed vertical gaps. Two-drawer bays now use150.75 mm boxes; single-drawer bays144.5 mm. Floor top isZ16, first box bottomZ19. Cap undersides areZ326.5 andZ166.5, each3 mm above the drawer stack. Compact strips move upward5 mm to start atZ19 and clear the floor. The entire recipe regenerates its mounting holes; old row164/452 runner holes are not retained. The drawer skill now records this client default. Other shelves remain adjustable on the shared32 mm grid.

- Reusable drawer policy checkpoint: compact floor-adjacent stacks and one full-width structural front are now AIkea defaults, with one authoritative installation section. Applied/doubled fronts require an explicit design choice. Shared height-planner default changed from22 mm to3 mm; six planner tests pass, including the actual corrected two-drawer stack. This user correction supersedes the earlier parent suggestion of a separate front.

- User correction: deck now has two1236.5 x432 x15 mm sections with a2 mm seam centered atX1237.5, spanning the full2475 mm base. Shared BaseModulePlanner resolves the middle cabinet gap from1220 x2440 sheet constraints; each deck orients its long axis along2440 mm and both432 mm strips fit the sheet width. Sixteen exact foot/plate pairs retain their previous cabinet-floor access axes; each deck owns eight pairs. No brace plinth introduced. Base recipe now explicitly separates deck segmentation from cabinet count.
- User correction: each drawer has one562 mm wide structural front with2 mm side reveals within the566 mm opening, independent of490.6 mm runner-box width. Its side walls terminate against the front’s rear face; paired Cabineos and bounded captured-bottom groove replace the old between-side front. No second front is added. Full travel against exact open hinges remains a required geometric check.
- Shared lighting ownership regression: five focused tests pass, including rejecting a mismatched mounting panel and preserving nested visibility/ownership.

- Strong-default enforcement: added actual-solid drawer layout evidence checker to shared complete-review export and fabrication gate. Missing evidence, noncompact measured gaps, missing cap references, narrow frontage and doubled fronts fail absent user-request provenance. Geometry helper and evidence/gate orchestration remain separate, each under150 lines. Existing202-line review-generator test file received the AGENTS-required independent read-only separation review: keep coherent generator probes, isolate layout rule tests, and move CLI parser coverage if expanding that concern. No blanket size-driven refactor is needed.
- Runtime audit found OCCT booleans using328% CPU despite OMP/BLAS limits. Stopped only worker PID41908; exported files remain. Next heavy launch must explicitly initialize the OCCT thread pool to one. Full closed geometry remains unfinished and unapproved.
- Wider-front full travel check failed at the exact open NC70 door: door reachesX25.43 mm inside the cabinet-local frame, while the front startsX18 mm. All-open adjacent leaves also obstruct neighboring bays. This is a real unresolved mechanical limitation, not hidden behind the valid render.
- Side fitting strips are an authored hinge/width arrangement workaround, not a supplied measurement requirement. Parent is clarifying the user’s desired treatment; no resizing/removal has been made pending that direction.

- Enforcement validation checkpoint:23 focused tests passed across measured layout rules, complete-review gating, fabrication gate and input fingerprint/approval regression. The policy-edit fingerprint invalidation test also passes. Existing project code now declares drawer_front roles and full stack references; regenerated proof is still required after pending design/motion decisions.

- User explicitly rejected filler/narrowing compromises and authorized sourcing better hinges. Preserve the full2475 mm four-bay design and single full-width structural fronts; remove the NC70-driven fitting workaround only with the verified replacement integration. Door entrypoint now routes an unsuitable/missing registered profile through sourcing and integration, not only missing CAD. Hardware skill prohibits silent dimensional/filler compromises.
- First manufacturer-backed replacement candidate: Blum71B7550 CLIP top BLUMOTION155° zero-protrusion,0 mm plate. Official Blum documentation states−2.3 mm door protrusion at90° and allows doors up to650 mm wide with an additional hinge. Exact source CAD, mounting plate, fastening and profile integration remain under investigation; no source model or full-motion approval is claimed yet.

- User selected visibly illuminating neutral-white cabinet lighting. Project now selects the existing supported DOMUS APEX 84 HI 4300 K product variant; this is fixed CCT, not a promise of selectable temperature. Parent owns efficient viewer illumination; worker owns project source/emission placement and final material preparation. New export and visual proof remain required.

- Neutral-white presentation update produced furniture_01-white.glb with nine emitters, preserving CAD binary and node transforms. Parent verified interior illumination after correcting the viewer area-light initialization. Shared 4300 K review tint now stays neutral; actual source CAD regeneration remains pending better hinge integration.
- Exact Blum 71B7550 hinge and 173H7100 plate public manufacturer-authored ACIS DXF retrieved from SWS Hardware. Live Blum portal explicitly requires login. Current CadQuery lacks ACIS import; installed Fusion access was denied by Computer Use, so no conversion occurred there. Isolated conversion runtime is being assessed; this is a format barrier, not a hardware/design incompatibility.

- Source checkpoint review: all25 project Python files parse. The153-line initializer-generated specification contract received independent separation-of-concerns review: cohesive immutable contracts/re-exports; no project-copy refactor needed. Future changes belong to the shared initializer/template. Full lit/open GLB now precedes expensive per-part STEP/DXF in the serial build sequence.
