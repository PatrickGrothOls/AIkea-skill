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
- [x] WP2: Generate all carcasses, foot base, doors, shelves, lighting and six complete drawer assemblies with compact supports (provisional physical qualification remains inWP3).
- [ ] WP3: Validate actual subtractive geometry/material removal, one-face policy, obsolete-hole absence, fixing alignment/engagement, fit tolerances and motion. Distinguish provisional source or load assumptions from proven geometry.
- [x] WP4: Export full provisional assembly STEP/GLB and84 current part STEP/DXF plus draft inventory; confirm all six drawers and hardware exist. Broad-face access and export geometry checks pass; unresolved construction/motion qualifications remain inWP3 and reports.
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

**Current geometry is v3:** all six centered468.75 mm fronts/boxes are regenerated. Exact whole-tree checks confirm no runner/front, shelf-pin/wood, support-fixing/rail or wood/wood contacts; no outside-envelope or invalid solids, no uncertain intersections. V2 assets below are preserved historical evidence. Remaining275 source engagement/illustrative screw contacts remain unqualified. Matching v3 baked appearance has passed all four geometry/coverage/export checks; parent visual delivery remains pending.

- Patrick explicitly retained all four616.75 mm doors provisionally. The current source and viewer now use four618.75 mm carcasses over2475 mm, with no fillers or narrowing. GRASS F028122660/F058139748 exact closed CAD replaces NC70; source-derived cup/plate machining is regenerated.
- Current v3 artifact: `local-evidence/fresh-project/reviews/furniture_01-grass-closed-diagnostic-v3.glb`,50,994,300 bytes, SHA256 `f1d85cb574b6dcdde81bb0e560dc29fdf8d79e25666fe6bf75f9f342876115b7`. Its manifest is `reviews/grass-closed-diagnostic-v3.json`: CLOSED_DIAGNOSTIC_ONLY, complete_review:false, fabrication_ready:false. It includes84 manufactured parts,6 structural drawer fronts,4 doors,2 decks,16 Korrekt pairs,17 GRASS hinge/plate pairs,102 selected illustrative hinge screws and9 neutral-white emitters.
- Parent delivered the earlier v1 diagnostic through the existing port51696 viewer (session36148), titled “Vilja — provisional full-width doors”. Exterior/interior screenshots were captured at `/private/tmp/vilja-full-width-exterior.png` and `/private/tmp/vilja-full-width-interior.png`; the single tab shows doors hidden for inspection. No new browser viewer was opened.
- Closed-only drawer dimensions: opening586.75 mm; centered fronts468.75 mm with59 mm equal side reveals; boxes468.75 mm on46.3/46.3 mm supports. All6 retain3 mm floor/stack/cap gaps, one structural front and captured bottoms. Complete motion-derived maximum width remains unverified, and the shared completion gate correctly reports missing travel evidence.
- All6 drawer assemblies and all GRASS drilling pass declared broad-face compatibility. The setup checker now resolves Korrekt through-bores and equal-thickness miter access, with eight focused tests passing; the current complete tree now passes declared broad-face compatibility for all12 assembly nodes. Exact cuts, fastening, tool reach and CAM remain separate.
- Native closed GRASS-versus-wood check now passes:34 bodies against84 machined wood parts,59 exact candidate intersections,zero positive overlaps. Matching `reviews/furniture_01-grass-closed-provisional-v3.step` is48,550,209 bytes, SHA256 `3a9ff738ea0f758856f112df3021d75e2a45c59a913585e07273cd8a550d80f8`. Previous86-part STEP/DXF and full NC70 STEP are preserved historical exports, not current full-width manufacturing data. Current84 STEP and84 blank-perimeter DXF exports are complete under `deliverables/grass-v3/manufacturing`, with84 manifest rows and641 hardware components. The mechanically corrected v3 Blender presentation passes all four geometry/coverage/export reports. Parent has the final v3 baked and matching packed inspection paths for the same viewer.
- Seven focused GRASS installation tests pass. Unchanged vendor sources, cup/plate datums and wood-screw pilots avoiding the Ø5 System32 grid are checked. The inferred source hinge/plate pair overlaps536.39245 mm³; clip engagement versus simplified-body representation is unresolved.
- Reference-chart width/load, actual MDF density/finish/hardware mass, screw seating and holding, calibrated support stock/lamination, base/cabinet/wall anchoring, kickboard fixings and electrical routing remain unqualified. User acceptance of the width uncertainty does not waive movement or manufacturing requirements.
- Exact runner source axes remain checked at all12 openings. The complete native pair uses a common2 mm inset; fixed axes39/167/231 mm from cabinet front and moving axes37/165/291 mm from drawer front. The0.2 mm native/nominal spacing difference remains explicit.
- Shelf pins, connector bodies and screws use labelled dimensional illustrations. Hinges, plates, runners and feet use unchanged source CAD. Grid-hole depth13 mm does not establish the selected shelf-pin insertion length.
- No large conversion runtime was installed. Fusion is authorized but the locked Mac prevents control. Exact Blum ACIS/SAT remains prepared for later local conversion; GRASS supplied a public native STEP route. No vendor login was bypassed or private project data uploaded.

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

- Latest user clarification: maximize each drawer within its actual unobstructed travel width while preserving the intended hinge pattern. Necessary hinge-side narrowing is correct, not an exception. Superseded582.75 mm front/511.35 mm box planning numbers and symmetric25 mm assumptions removed from replacement planning. Shared policy now requires independent obstruction/fit/support/runner dimensions backed by current sweep evidence; missing or stale evidence blocks review/completion. No new complete geometry export is claimed.

- Subsequent user clarification retains unified symmetry: independent hardware deductions are inputs, but centered fronts use the governing side clearance on both sides and across their alignment group. Hidden supports may differ only as needed. No asymmetric-front geometry was exported. Current project policy groups all six Vilja fronts; exact verified travel evidence remains missing, correctly blocking the new gate.

- Symmetric-front policy and review gate verified together: 28 focused layout/export/fabrication/fingerprint tests passed. Asymmetric obstruction requires a centered front; off-center front fails; hidden required support asymmetry passes; stale/missing sweep evidence and unnecessary support narrowing fail. This validates gate behavior with synthetic fixtures, not Vilja hinge-motion approval.

### Source-format recovery recheck

- [x] Rechecked existing tools without installing a large runtime: CadQuery/OCP has STEP/IGES readers but no ACIS reader; FreeCAD, ODA File Converter and CAD Exchanger are absent. Fusion is installed/running but its previous Computer Use denial remains in force. The tool supplied only “Computer Use was not approved to use Autodesk Fusion”; no more specific reason was returned. No OS scripting or alternate app-control route was used. Disk free is now approximately2.87 GB.
- [x] Rechecked public SWS downloads: exact71B7550 offers DWG/DXF only. Both saved original DXF checksums still match the source record.
- [x] Prepared live Chrome tab1513940861 on https://shop.blum.gr/en/clip-top-blumotion-wide-angle-hinge-for-zero-protrusion-69689716 with exact nickel screw-on item01181769 and CAD/CAM selected. The live panel requires registration/login; it is not an empty format list or pending CAD generation. No credentials or terms were entered.
- [ ] Blum native conversion remains available when the authorized Fusion session can be used; user cannot sign in from the phone, so public alternative sourcing proceeds without requiring that handoff.

### Public native STEP recovery checkpoint

- [x] User explicitly authorized Fusion. Parent attempted its exact bundle, but the locked Mac prevented control; automatic unlock failed. Subsequent authorized window capture found Fusion window292, but capture failed and the ID was rechecked. No Fusion import/export or control occurred. This supersedes the previous approval-denied state; manual unlock is the present boundary.
- [x] Extracted the eight exact decoded Blum DXF ACIS SAT bodies into `hardware/blum-71b7550/source-sat/` with checksums and original entity handles. No geometric reconstruction or neutral conversion is implied.
- [x] Downloaded official GRASS Tiomos155Plus and mounting-plate ZIP archives via the public CAD page; no login, upload or converter installation required. Stored exact F028122660 screw-on damped K3 hinge and F058139748 3 mm screw-on plate through HardwareCadStore, retaining original ZIP archives and SHA-256 provenance.
- [x] Both unchanged STEP inputs import as valid single solids in their native millimetre frame. Hinge bounds: X−13..53.95354, Y−49.5..42.71395, Z−31..31; plate bounds: X−3..10.5, Y−25.55..39.95, Z−24..24. Sourcing is complete for this candidate; installation is not approved.
- [x] Current GRASS2026.27 pages518–519 specify K3 +3 mm plate flush at90°, 35 mm cup,45×9.5 fixing pattern, minimum11.5 mm cup depth and18 mm door compatibility. Page580 identifies F058139748 and Ø3.5×15 wood screws.
- [ ] Resolve616.75 mm door load/width qualification: current page594 gives hinge-count guidance for standard600 mm leaves and requires trial fitting in doubt; it is not an explicit600 mm maximum, but it does not certify this wider leaf. Do not silently narrow the wardrobe or assert supplier approval.
- [x] Visually read the official page519 grid: K3 hinge,3 mm mounting plate and6 mm cup distance give15 mm overlay. This matches16 mm stock with1 mm door setback at each carcass edge and616.75 mm leaves on618.75 mm carcasses.
- [ ] Verify native placement, exact intended hinge pattern, fixing engagement and full drawer travel before selecting this alternative and replacing the rejected NC70 arrangement. The supplied STEP is one closed-position solid, not separately articulated links or an open-pose proof.

Public authority: https://www.grass.eu/en/tec-center/cad-data/ ; https://mediacenter.grass.eu/Katalog/EN/518/ ; https://mediacenter.grass.eu/Katalog/EN/519/ ; https://mediacenter.grass.eu/Katalog/EN/580/ ; https://mediacenter.grass.eu/Katalog/EN/594/ . Vendor CAD bytes remain ignored and local-only.

### WP: user-owned door layout and reference-width decisions

- [x] Locate and remove the contradictory instruction to revise the arrangement instead of sourcing hardware.
- [x] Define reference-chart versus hard-limit handling in the shared door skill, including actual material/door mass and hinge configuration.
- [x] Require a user decision before adding leaves, narrowing cabinets or introducing fillers; preserve a labelled provisional review for unresolved reference-width qualification.
- [x] Validate the revised skill and review the policy diff for conflicting instructions. Skill Creator quick validation passed; targeted search and manual review confirm the forced-redesign rules were replaced. No CAD or motion test is implied by this documentation check.
- [x] Present the concrete mass/width choices; Patrick subsequently chose to retain the full doors provisionally, as recorded below.

Audit decision (explicit user direction): consider dividing genuinely wide leaves where it solves the problem, then seek other hardware/construction when division is unsuitable. For small reference-width overruns, explain the measured difference, material/weight dependency and practical options instead of making the layout decision for the user. The existing opposed rules plausibly explain the unwanted side strips. This changes decision guidance, not the current CAD or its motion/fabrication status.

- Further public-source verification: saved official pages518/519 as small standalone PDFs with checksums in the GRASS candidate technical folder. The12 mm/8 mm opening dimensions on page518 apply to the different K9.5/8 mm plate mitred application and are explicitly excluded from this K3/3 mm installation. Door flushness at90° is not the complete moving-arm envelope. Exact distributor article44.012.51/F028122660 routes its CAD link to the same manufacturer ZIP catalogue; the GRASS iFurn route requires login. Current EU600 mm and US24-inch load guides both require trial fitting and provide no explicit616.75 mm approval. No approximation, narrowed cabinet, new drilling or replacement export was introduced to hide these qualifications.

### Full-width door decision calculation

- [x] Read the revised door policy in10d4e96 and retain the current layout while calculating the intended full-width proposal.
- [x] Calculate all four actual polygon areas using the authored18 mm single-slab painted-MDF construction, with618.75 mm bay pitch and15 mm overlay. No frames or second front layers are present. The616.75 mm width exceeds the600 mm chart reference by16.75 mm/2.7917%; this is not a demonstrated hard maximum.
- [x] Save reproducible calculator `local-evidence/fresh-project/tools/calculate_door_proposal.py` and local result `reviews/door-proposal-mass.json`. Shoelace areas agree with piecewise integration and the actual CarcassRecipe proposal outlines. The active project parameters and preview remain unchanged.

| Door, left to right | Width × thickness (mm) | Left → right height (mm) | Blank mass (kg) | Estimated painted panel (kg) | Proposed hinges |
| --- | --- | --- | --- | --- | --- |
| 1 | 616.75 ×18 | 2272 →2272 | 18.92 | 19.64 | 5 |
| 2 | 616.75 ×18 | 2272 →1998.11; first370.25 mm flat | 18.46 | 19.17 | 5 |
| 3 | 616.75 ×18 | 1995.89 →1310.61 | 13.77 | 14.30 | 4 |
| 4 | 616.75 ×18 | 1308.39 →623.11 | 8.04 | 8.35 | 3 |

These are estimates, not measured finished masses. MDF density750 kg/m³ is an explicit assumption because no stock supplier/density is selected. Coating allowance0.25 kg/m² covers both faces and all edges; it is not a specified paint product. With700–800 kg/m³ stock, painted-panel estimates are18.38–20.90 /17.94–20.40 /13.38–15.21 /7.82–8.89 kg. Moving hinge parts, screws and unselected handles remain additional unknown masses, not zero. Unfinalized drilling is not subtracted. The shared DoorHingePlanner’s650 kg/m³ plywood/left-height-rectangle estimate is unsuitable for these sloping MDF leaves and was not used.

The GRASS F028122660/F058139748 proposal uses5/5/4/3 hinges, corresponding to the reference chart’s2500/22,2500/22,2000/17 and1600/10 height/weight regions for600 mm leaves. These comparisons do not extrapolate capacity to616.75 mm. Left-hand layout remains intended; exact centers and fastener engagement require the new hardware installation and obstruction check. Existing NC70 positions are not represented as GRASS-approved.

Decision-ready options for Patrick:

1. Retain four616.75 mm leaves as an explicitly accepted provisional proposal, then resolve stock/finished mass and obtain supplier confirmation or the prescribed trial fit. This would not waive actual drawer collision or fixing checks, and no acceptance is recorded yet.
2. Divide selected openings into two leaves (about307.38 mm each with an additional2 mm central reveal), changing the visual pattern and access. Requires a user layout decision and new hinge/weight checks; no automatic split.
3. Continue with alternative hardware preserving four leaves. Blum71B7550 has stronger published width guidance already saved, but native conversion is blocked by the locked Mac. Unlocking enables the already-authorized Fusion attempt; no success is assumed.

Fitting strips/narrowing remain rejected and are not applied; they would require a new explicit user decision.

### User decision: retain full doors

- [x] Patrick explicitly chose “Retain full door”. Retain all four intended616.75 mm leaves provisionally, with the previously disclosed reference-chart width qualification unresolved. No fillers, narrowing or extra leaves. This choice does not approve load, fixings or motion, but width uncertainty alone does not block independent construction or labelled provisional review.
- [x] Integrate exact GRASS hinge/plate closed placement and source-derived drilling; corrected v2 closed wood-fit passes.
- [ ] Verify intended hinge positions, actual fixings and compact drawer clearance; preserve centered fronts with hardware-constrained symmetry.
- [x] Regenerate the complete provisional assembly and matching baked presentation after the corrected closed wood-fit check; retain all load/motion/manufacturing qualifications explicitly.

### GRASS closed installation checkpoint

- [x] Added shared exact-source loader, K3/3 mm profile, feature-aware placement, four-point drilling and purchased-body placement. Five focused tests pass. The full-width preflight places hinge centers at132/612/1156/1668/2148 mm in bays1–2,228/708/1284/1892 in bay3, and228/644/1188 in bay4. Source mounting bodies avoid shelves and runner strips; mounting pilots avoid the existing Ø5 grid.
- [x] Cup bores retain6.5 mm of18 mm door stock; provisional Ø2.5×12 pilots retain4 mm in16 mm carcass. Pilot sizes and stock screw-holding still need qualification. Native source cup/plate datums reconcile15 mm overlay and the selected zero rear-door gap by shifting the whole pair1.5 mm deeper than the37 mm reference.
- [x] Exact closed source first-drawer intersection reachesX67.913152 mm in the Y2..18 mm front slab andX72.953543 mm in the Y18..402 mm side-wall span. The side inside face isX16. These are closed-only obstructions, not a certified moving-arm envelope. Source pair overlap536.39245 mm³ remains explicitly unresolved (clip engagement versus simplified source solids).
- [x] Integrate the corrected closed placement into the full-width project with provisional drawer geometry; preserve separate diagnostic artifacts while the complete-review motion gate remains unsatisfied. Do not issue a full-travel certificate from these closed measurements.

Skill review: the source/paired-machining/retained-stock obligations are represented; exact moving-arm poses, hardware/stock screw qualification, full-tree collision proof and load/trial-fit acceptance remain open. No original source STEP was modified and no NC70 motion was reused for GRASS.

### Full-width closed diagnostic build

- [x] Active source now restores four618.75 mm carcasses and616.75 mm leaves across2475 mm, with no fitting panels. The prior NC70 recipe, source placements and hinge cuts are replaced by GRASS operations; no retired hinge pilots are retained.
- [x] Calculate provisional closed-fit front478.75 mm within586.75 mm opening, equal54 mm visible reveals across all six fronts. Exact closed obstruction51.913152 mm plus2 mm fit allowance rounds upward to the0.1 mm dimension resolution. Left box obstruction56.953543 mm plus2 mm fit allowance and12.7 mm runner space gives46.3 mm support; the right41.3 mm support is required for the single front to reach its box-side joint, not a fabricated right hinge obstruction. Box473.75 mm is shifted2.5 mm relative to the centered front, hidden behind it. Full-motion maximum width remains unverified.
- [x] Recalculate support attachment lengths: selected SPAX0201010400605 Ø4×60 left and0201010400503 Ø4×50 right give13.7/8.7 mm nominal substrate penetration; full support clearance and14 mm side pilots are included. Calibrated birch support stock/lamination, head bearing and substrate holding remain unresolved. These are not asserted load-qualified. Manufacturer article authority: https://www.spax.com/de-de/p/universalschraube-vollgewinde-halbrundkopf-t-star-plus-4cut-wirox.html .
- [x] Include six selected GRASS F072135961 Ø3.5×15 screws per hinge pair, with explicit simplified visual geometry and provisional seating. Manufacturer identifies this countersunk wood-screw article; exact nickel-kit suitability, seating and MDF holding remain open. Source: https://mediacenter.grass.eu/Katalog/EN/524/ .
- [x] Full-width base trial caught14 mm plate-to-deck-seam clearance where15 mm is required. Shift cabinet-local foot stations1 mm inward and regenerate both deck operations and matching cabinet-floor access from the same axes. The two decks and16 foot/plate pairs remain.
- [x] Finish serial full-tree closed diagnostic export. Completion gate failure is retained in its manifest; parent delivered the explicitly provisional view and screenshots. This is not passed opening motion or fabrication approval.

- Native follow-up: serial exact closed GRASS-versus-wood checks and matching provisional STEP are running from unchanged construction inputs. The GLB delivered to the parent is not modified by that check. The remaining unsupported setup joint kinds were traced to the checker's Cabineo-only joint dispatch; no evidence was relabelled as passing.

### Exact closed-fit failure and correction

- [x] First exact native GRASS-versus-machined-wood check evaluated34 purchased bodies against84 wood parts,54 candidate intersections. It found129.00264 mm³ cup-flange overlap with each of17 left sides, plus244.80079 mm³ at bay3's upper hinge/sloping roof. No closed drawer collision was found. The first provisional STEP and failed report are preserved; neither is manufacturing approval.
- [x] Isolate the repeated side collision to the cup flange's0.55 mm projection behind the zero-gap door. The source mounting line37 mm and cup plane−38.5 mm require1.5 mm rear-door clearance. **The earlier interpretation of the catalogue's minimum lateral reveal as permission for zero rear clearance was wrong and is superseded.** The shared profile now requires the native1.5 mm rear gap; a regression test rejects zero gap.
- [x] Set the carcass front back1.5 mm while retaining the door, back plane,450 mm overall depth and all user-selected widths. Carcass/floor/top depth is414.5 mm to the inner back. The closed drawer front stays2 mm behind the door (0.5 mm behind the carcass front), with its runner pair unchanged; left mounting pilots compensate the changed panel origin. Floor adjustment axes remain mapped from the base; top lighting remains aligned at globalY20.
- [x] Add whole-body roof clearance to the shared GRASS planner. A conservative source bounding box must clear the actual inner roof plane by2 mm; top centers become1860 mm in bay3 and1156 mm in bay4. This adjustment addresses physical roof interference, not cosmetic drawer width. Seven focused tests pass, including sloped-roof and zero-gap regressions.
- [x] Regenerate v2 GLB and native STEP and repeat exact closed-body-versus-wood checks in the same serial build. CheckPASS with34 bodies,84 wood parts,61 exact candidates andzero overlaps. V1 files are preserved; parent has the verified replacement paths/hash for the same viewer.

Review distinction: source registration and actual wood collision checks now actively challenge the installation. A pretty diagnostic render never overrules an observed collision. Open/moving-arm evidence, hardware-to-hardware clip representation, fixing/stock and load qualifications remain separate after this correction.

- V2 skill review: six full captured-bottom drawer assemblies and real native runner pairs remain present; front symmetry and3 mm vertical gaps are measured in the exported mesh. Exact closed GRASS-versus-wood now passes after physical corrections. Full travel and source clip engagement are still unresolved, so the complete-review gate remains failed and fabrication_ready remains false. Existing Blender.app/CLI reports exact5.2.1 LTS; the appearance stage can reuse it instead of installing a duplicate runtime on the low-space disk.

### Presentation stage using the existing engine

- [x] Prepare representative white painted MDF, birch support/deck, HDF and hardware materials with part-local UVs from the corrected v2 GLB. Material preparation verifies unchanged original CAD buffers/transforms; product/coating choices remain representative.
- [x] Shared mesh packing passes:743 items,14,571→743 draw primitives, indexed positions/normals/UVs bitwise equal, transforms/identities/materials preserved, no simplification. Packed source SHA256 `898ec5b9c5b41e7ef982a11e5c0ecae58dd44eb121be5caf118b799d5a36edda`.
- [x] Discover existing `/opt/homebrew/bin/blender` / Blender.app5.2.1 LTS. The sandboxed background probe crashed in Metal device detection before Python; the same bounded probe with normal local device access passed background/Cycles/glTF checks. This is a sandbox graphics boundary, not a locked-Mac or missing-runtime failure. No software installation or GUI/lock-setting change occurred.
- [x] Run unchanged shared Blender worker via the verified installed CLI, one CPU thread,4096² atlas,16 samples, immutable output `reviews/presentation-grass-v2-02`. All four coverage/geometry/export reports PASS:84 panels,775,824 triangles,zero uncovered centroids,743 preserved identities and maximum export rounding0.0007836 mm. Assembled GLB76,321,948 bytes, SHA256 `9b58499d9762158e634c22a3bb7e84454cf751213567611f8623a6ad0db086c5`. The failed pre-Python startup remains in `presentation-grass-v2-01`. Parent received the verified baked file and matching packed inspection source for the same viewer; visual close-up review remains pending. This appearance result does not grant manufacturing authority.

### Setup audit support for registered joint types

- [x] Trace unsupported statuses to the setup checker's Cabineo-only joint dispatch. Add a focused joint-face resolver for the existing registered Korrekt through-bore cutter and equal-thickness miter half-space. Korrekt permits either broad face only when its bore axis is parallel to panel thickness. Miter access follows the removed half-space's sign in each part frame; an outward ray must remain in removed material, so no undercut is assumed. Unknown joint kinds still fail.
- [x] Eight focused setup regression tests passed4.20s, including a rotated incompatible Korrekt axis and an actual miter/opposed-blind-cut conflict. This extends declared face access only; material removal, tool reach, workholding, CAM and load remain separate checks.
- [x] Re-run the complete current assembly audit against unchanged v2 construction SHA256 `48952f26c3b7ea027f8f7c2b485155612567747a7fbbfc88940ecb849f3f9ec0`: all12 assembly nodes have compatible declared broad-face access. Export84 STEP and84 blank-perimeter DXF files,84 manifest records and inventory641 hardware components/134 Cabineos/134 brass inserts under `deliverables/grass-v2`. Six complete five-panel drawer sets remain. DXFs are explicitly blank perimeters, not machining toolpaths. Layout gate still fails missing verified travel-clearance evidence; construction requirement coverage still flags undeclared/unresolved attachment evidence. No report is relabelled fabrication-ready.

### Reproducible provisional delivery checkpoint

- [x] Preserve the successful existing-engine bake command and current84-part export command as project tools. Both ran to completion against the corrected v2 geometry;27 combined setup/GRASS/layout tests pass4.63s. The bake remains an appearance proof and part DXFs remain blank outlines.
- [x] Retire the project `build_review.py` route that still selected NC70 open poses. It now stops immediately with current closed-only commands and the missing GRASS motion requirement; it cannot silently produce an incorrect open-hinge presentation if another gate later passes. Prior implementation remains in Git history.
- [ ] Parent visual review of `presentation-grass-v2-02/assembled.glb` with `grass-v2-materials-packed.glb` as its matching inspection source. Keep the same viewer/tab and provisional qualification.

### Broader v2 check and remaining closed-contact corrections

- [x] Run the shared complete-tree geometry/construction checker:725 valid solids,none outside the envelope,no wood-to-wood overlap,applied operations PASS. Overall status is invalid with319 undeclared overlaps and18 uncertain Boolean intersections. Source clip/foot engagement and illustrative screw seating are not silently allowed.
- [x] The broader audit finds real front-to-runner interference: six front/left-moving contacts630.6141 mm³ and six front/left-fixed contacts30.6849 mm³. The5 mm structural-front overhang covers a rail that starts within the front slab depth. Moving the entire400 mm rail behind the16 mm slab would exceed the supplied450 mm depth.
- [x] Correct the authored closed-fit proposal to centered468.75 mm fronts and boxes with59 mm side reveals and46.3 mm supports both sides. The left hinge sets the minimum support; the right matches to center a single front terminating on both side walls without a rail-clashing overhang. No extra fascia or thin rear relief pocket is introduced. Hardware-safe width includes runners as well as hinge obstruction; full moving-arm qualification still remains open.
- [x] Align front shelf-pin centers with the1.5 mm carcass-front datum plus37 mm grid setback; old centers were1.5 mm off-axis. Move support screw heights6/70 mm within80 mm strips, clear of the rail body; both46.3 mm supports now use selected Ø4×60 screws with13.7 mm nominal engagement.
- [x] Regenerate v3 and repeat exact contact checks before replacing the preserved v2 appearance. These corrections are mechanically necessary within the approved footprint/symmetry, not a change to the door or hinge layout.

- V3 result:725 valid physical solids,zero outside the envelope,zero uncertain intersections and275 remaining overlaps, confined to16 foot/plate,17 hinge/plate and242 illustrative screw seating/wood-engagement contacts. No wood/wood, runner/front, pin/wood or support-fixing/rail collision remains. Applied operations and all12 declared broad-face setup audits pass. Exact GRASS-versus-wood also remains PASS. No remaining contact is silently approved; source engagement, fixing geometry/holding and full motion remain qualifications.
- V3 construction SHA256 `35d1da79993d75672f860d86bc44eb4d305c246ef648984cd98a5d8f3ca14d3f`; diagnostic GLB50,994,300 bytes, SHA256 `f1d85cb574b6dcdde81bb0e560dc29fdf8d79e25666fe6bf75f9f342876115b7`. All84 current STEP/DXF pairs and draft inventory are under `deliverables/grass-v3`. Earlier native and presentation outputs remain intact. The whole-tree status remains invalid because remaining contacts/requirements are unqualified, despite the specific geometry corrections passing.

- Presentation tools now require explicit source/output paths, removing stale model defaults. Both CLI help paths passed; v3 material preparation and shared packing pass, with743 identities and bitwise-equal indexed geometry. The v3 packed inspection SHA256 is `ebd4013871b0a1376ee38ade83ee532e0d5a42b3ea753184f48e87b0c350941f`. Exported mesh measurements confirm all six468.75 mm fronts,59/59 mm side reveals and all3 mm floor/interdrawer/cap gaps (`reviews/grass-v3-glb-dimensions.json`). V3 white-bake coverage passes84 panels/775,824 triangles/zero uncovered centroids; lighting bake is running with one CPU thread.

### V3 presentation delivery

- [x] Completed one-thread Blender5.2.1 LTS bake in `reviews/presentation-grass-v3-01`. All four reports PASS;743 identities preserved,zero uncovered triangle centroids,max vertex rounding0.0007836 mm. Output SHA256 `f9968c556ea28dac14f9faebddebf6e77ac80894942c43f9f6628517114f05ad`; input hash independently rechecked against `ebd4013871b0a1376ee38ade83ee532e0d5a42b3ea753184f48e87b0c350941f`.
- [x] Update the v3 delivery README with current artifact links and specific qualifications. No baking or CAD job remains running. No new viewer/tab was opened by this worker.
- [ ] Parent replaces the existing single viewer with the v3 baked model plus matching inspection model, checks edge close-ups/interior lighting and captures phone screenshots. Visual acceptance and all WP3 manufacturing/motion qualifications remain separate.

### Requested first-door-open screenshot

- [x] Re-read official GRASS page518 and v3 source. K3+3 mm plate documents lateral flush at90°, not the fore/aft endpoint. The neighbouring mitred dimensions concern K9.5 and cannot supply the missing datum.
- [x] Parent authorized an explicitly illustrative90° endpoint for the screenshot. `reviews/grass-v3-first-door-open-illustrative.glb` moves only cabinet1 door and its10 owned cup screws, omits its5 fused hinge bodies and retains fixed plates and all other nodes unchanged. Doors2–4 remain closed; original mesh/material buffers and original files are preserved. The `.pose.json` records the missing fore/aft datum, assumedY0 hinge edge/X16 flush rearface and no articulation/motion/manufacturing authority. Parent received the path immediately, before any commit; no CAD rebuild/bake or viewer takeover occurred.
- [x] Parent delivered `/private/tmp/vilja-cabinet-1-door-open.png` from the same port51696 viewer (session99233). Cabinet1 open and other3 closed were visually verified; title explicitly says illustrative. The live packed material was used, so assembled baked shadows were not moved. This records screenshot delivery, not motion or fabrication approval.


### Branch skill capture and independent rerun — 2026-09-16

- [x] Patrick corrected the release instruction: rebase this branch on main and
  run the fresh agent here. Fetched `origin/main` at `52facbf`; rebase was already
  up to date. No merge, push or installed-skill promotion.
- [x] Capture and review shared lessons in [skill-capture-before-fresh-run.md](skill-capture-before-fresh-run.md).
  Six coherent checkpoints committed; 48 focused tests before review and 21
  overlapping targeted tests after review fixes passed. Seven skills validate.
- [x] Launch a fresh no-history agent against branch-local skills with the original
  envelope and material/function brief, excluding the existing project's answers.
- [ ] Inspect new deliverables and compare against the skill's stated contract.
  Track execution in `docs/skill-cold-start-20260916.md` once the agent creates it.
