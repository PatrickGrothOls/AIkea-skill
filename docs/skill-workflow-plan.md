# AIkea skill workflow and command interface plan

## Scope and current state

Planning branch: `codex/skill-workflow-plan`, based on public main `2f60a51`.
Patrick requested a plan after comparing AIkea with the installed gstack and
HyperFrames packages. This document proposes implementation; it does not approve
architecture decisions or authorize deployment, release, or manufacturing.

- [x] Inspect current routing, construction protocol, installation and command entry points.
- [x] Compare local gstack workflow tooling and HyperFrames workflow/domain separation.
- [x] Save a phased plan with acceptance criteria and independently mergeable slices.
- [x] Incorporate Patrick's request for an early live viewer and animated build updates.
- [ ] Patrick reviews the proposed direction before implementation.
- [ ] Implement the work packages below on separate, focused branches.

No runtime, skill instructions, project schemas, or released packages changed.
The current fabrication checks already exist. This work makes them easier to
invoke and their outcomes easier for an agent to interpret.

## Intended outcome

An agent should be able to start or resume a furniture project, identify the
next unfinished obligation, invoke the correct existing tool, and explain any
real blocker without rereading every skill or guessing script paths. A request
to inspect or revise one feature must not restart intake.

Borrow HyperFrames' separation of entry routing, owning workflow and on-demand
domain capabilities. Borrow gstack's explicit review and release responsibilities.
Retain AIkea's measured inputs, reusable construction code and physical checks.
Neither comparison justifies introducing a new agent framework or background daemon.

### Live build experience

Patrick wants to watch the cabinet take shape throughout construction, rather
than receive the viewer only at the end. Open one persistent viewer early, with
an empty state until the first usable geometry exists. After every successful
supported build/export checkpoint, update that same viewer automatically.
Keep the camera, zoom and relevant inspection controls steady between updates.

Show real completed geometry as work in progress: shell, shelves, fronts,
drawers, purchased fittings and lighting appear when actually built. A successful
script that produces no geometry must not trigger an invented visual update.
The first version updates after completed checkpoints; streaming intermediate
CAD Boolean operations is outside its scope. The preview must not wait for
photorealistic baking or the complete fabrication package.

Proposed motion: new parts fade into their real positions with a short stagger;
changed geometry crossfades; unchanged parts stay still. This gives the requested
piece-by-piece reveal without distorting the real CAD shape. Arbitrary topology
morphing is deferred: a drilled panel and an undrilled panel need not have matching
vertices. Motion is illustrative, not a physical assembly sequence. Respect
reduced-motion preferences and keep controls responsive during transitions.

## Proposed ownership

| Layer | Responsibility | Authority it must not acquire |
| --- | --- | --- |
| `aikea` entry skill | Resolve active project and request; select or resume the owning workflow | CAD calculations, duplicate construction policy |
| Intake reference under `aikea` | Guide measurements and shared choices; route material decisions to their owner | Invented measurements or new approval rules |
| `aikea-design-furniture` | Own the design workflow and compose applicable capabilities | Reimplementing builders or certifying unsupported hardware |
| Existing specialist skills | Complete materials, units, doors, drawers, lights and hardware within explicit contracts | Restarting global intake or taking over the whole workflow |
| Shared command interface | Resolve paths/runtime; dispatch existing operations; present consistent results | New geometry logic or a second readiness engine |
| Existing builders and validators | Calculate, build, export and validate actual project artifacts | Inferring user approval from a successful command |
| Live build publisher and viewer | Publish complete preview revisions; display and animate their differences | Editing CAD or approving a moving target |
| `aikea-review-unit` and existing fabrication gate | Coordinate review evidence and report manufacturing readiness | Treating an attractive preview as manufacturing approval |

The entry skill routes once for an active workflow, but explicit new user intent
can select a different operation. The owner resumes after specialist handoffs.
Existing project files remain authoritative; do not add a parallel workflow-state
file or migrate `aikea.yaml` as part of this plan. The live preview may have a
small, derived revision manifest for delivery, not a second design specification
or workflow authority. Any later project-schema need gets a separate proposal
before implementation.

## Work packages and branch sequence

### WP1 — Stage contracts and baseline scenarios

First implementation PR: contracts and regression scenarios, no behavior changes.

- [ ] Inventory each public skill, executable entry point and packaged counterpart.
- [ ] Map both the standard wardrobe route and authored/custom composition route.
- [ ] For each stage, record owner, required inputs, written outputs, exact check,
      completion evidence, blocker categories, invalidation triggers and next owner.
- [ ] Distinguish permission required, user design choice required, missing vendor
      input and recoverable tool error; only request user input when needed.
- [ ] Reuse existing synthetic fixtures and capture current outputs as the baseline.
- [ ] Include fresh intake, saved-project resume, inspect-only, material revision,
      drawer addition, missing hardware, stale review evidence and custom composition.
- [ ] Add progressive-build scenarios: empty project, first geometry, added part,
      modified/removed part, failed build, rapid successive builds and viewer reconnect.

Acceptance: every stage has one owner; success refers to existing evidence rather
than conversational claims. Missing or stale evidence never becomes a pass. Keep
client data and manufacturer CAD out of checked-in fixtures and reports.

### WP2 — Slim entry routing and preserve intake behavior

Second PR: reorganise instructions without altering construction rules.

- [ ] Move detailed measurement guidance and calculator sequence from
      `aikea/SKILL.md` into a focused intake reference; retain the existing
      conversation contract and material-owner boundary.
- [ ] Keep entry instructions focused on project discovery, supplied-input reuse,
      version check, request classification and workflow handoff.
- [ ] Make `aikea-design-furniture` the continuing owner after intake; references
      carry detailed policies, and specialists return to that owner.
- [ ] Preserve direct invocation of existing specialist skills and their names.
- [ ] Reuse the package verifier to check discovery and moved document links.
- [ ] Run the WP1 routing scenarios with fresh agent context and saved-project resumes.

Acceptance: explicit inputs are not asked for again; inspect-only is read-only;
custom furniture is not forced through wardrobe-only fields; acknowledgements
continue authorized work; first-complete-unit approval remains required where
the current workflow requires it. Measure entry instruction size before/after,
but do not split coherent instructions merely to hit a line count.

### WP3 — Command foundation and read-only project status

Third PR: a small CLI boundary before exposing mutating operations.

- [ ] Define one documented launcher available in both source checkout and
      portable installation; preserve the source workflow's `direnv exec .` use.
- [ ] Add help, version and status commands with explicit project and assembly
      selection; do not guess between multiple assemblies.
- [ ] Read existing specifications/reports and expose their source, freshness and
      missing evidence. Status must not build geometry or refresh approval.
- [ ] Define a versioned JSON result envelope plus concise human output, stable
      exit codes, artifact references and actionable blocker descriptions.
- [ ] Separate command execution outcome from project readiness. Existing valid
      evidence can be reported; a successful status command does not certify it.
- [ ] Test paths with spaces, wrong runtime, missing project, ambiguous assembly,
      missing/stale evidence, and source versus installed invocation.

Suggested command vocabulary is `aikea status`, `aikea build`, `aikea check`,
`aikea preview` and `aikea export`. The exact launcher/module location is a WP3
design choice, to be confirmed against the portable package before coding.

Acceptance: read-only means no project writes; JSON goes to stdout and diagnostics
to stderr; expected failures retain useful errors without exposing credentials.
Do not invent freshness information that existing reports cannot establish.

### WP4 — Build and check adapters

Fourth PR: wrap existing construction operations rather than replace them.

- [ ] Map supported standard/authored build routes to existing builders, including
      `aikea-review-unit/scripts/build_furniture_design.py` where applicable.
- [ ] Map check scopes to existing geometry, panel-setup and fabrication checks,
      including `check_panel_setups.py` and `check_fabrication_readiness.py`.
- [ ] Keep legacy scripts callable and preserve their inputs, outputs and exit behavior.
- [ ] Extract reusable command handlers only where needed; no wholesale package move.
- [ ] Translate current reports into the shared envelope without hiding failures.
- [ ] Verify old/new invocation parity on artifacts, geometry, inventory, evidence
      fingerprints and failure cases, using tolerance-aware CAD comparisons.

Acceptance: CLI and legacy routes reach the same validation gates. Changed
geometry, materials, hardware or placement invalidate affected evidence exactly
as before. Default assembly IDs must not silently switch between routes.

### WP5a — Live preview publication after builds

Separate PR: publish complete preview revisions without changing approval sessions.

- [ ] Identify the shared successful-build/export boundary for supported standard,
      authored and legacy commands. Attach publication there rather than only
      adding a CLI wrapper hook or watching arbitrary script/file saves.
- [ ] Export a lightweight preview using the existing CAD-to-GLB path. Allow an
      incomplete design with valid displayable geometry; show unresolved work
      explicitly and retain all fabrication gates.
- [ ] Define a derived manifest with project/assembly identity, ordered revision,
      source fingerprint, immutable asset references and stable part IDs/hashes.
      Reuse existing catalog identities where possible; qualify them by owner path.
- [ ] Write and validate assets before atomically publishing the new manifest.
      Reject out-of-order completions; never expose partially written GLBs.
- [ ] Report build-in-progress and failures separately. A failed build leaves the
      last successful model visible with an explicit stale/failed-update status.
- [ ] Keep preview export failure distinct from CAD build failure; report the
      preview problem without claiming the successful CAD output was lost.
- [ ] Add bounded retention for preview revisions, preserving assets still in use
      or referenced by formal review. Preserve project/source files.

Acceptance: partial writes and slower old builds cannot replace a newer completed
preview. Stable identities survive repeated builds. A draft preview cannot create
or preserve fabrication-ready status by itself.

### WP5b — Persistent viewer updates

Separate PR: show build progress in one viewer without manual refresh.

- [ ] Open the viewer at workflow start or first available supported delivery,
      and reuse it across subsequent builds rather than opening multiple tabs.
- [ ] Extend the existing local viewer lifecycle with revision discovery; select
      polling or server events after checking local and hosted delivery support.
      Do not introduce a second always-running agent daemon.
- [ ] Load and validate a new revision offscreen before swapping its scene.
      Keep the last working scene when assets fail to load.
- [ ] Preserve orbit/zoom and surviving selections; fit only the first model or
      on explicit user action. Handle removed selections and updated bounds.
- [ ] Keep warm lighting, textured materials, hardware and machining visible.
      Dispose of superseded scene resources after replacement.
- [ ] Test repeated updates, reconnects, two different project sessions and
      assets completing out of order. Keep project sessions isolated.
- [ ] Preserve the immutable snapshot/token behavior of existing formal review
      sessions. Enter review on an explicit revision; approval must match that
      revision, and changed geometry must invalidate affected evidence.

Acceptance: two consecutive builds become visible automatically in one tab;
camera position survives; failed updates are visible and recoverable. No approval
request can silently change the geometry the user is being asked to approve.

### WP5c — Animated part appearance

Separate PR: polish the verified live-update path.

- [ ] Diff revisions by stable owner-qualified part identity and content/placement
      hashes; do not infer change from mesh order, filenames or timestamps alone.
- [ ] Fade/stagger newly added pieces into their actual positions; crossfade
      replaced geometry, transition placement-only changes, and fade removals.
- [ ] Leave unchanged parts untouched. Start with short transitions; tune timing
      against a real cabinet and cap total initial-reveal time.
- [ ] Coalesce bursts toward the newest complete revision instead of queuing a
      long backlog. Define interrupt behavior when a build arrives mid-transition.
- [ ] Restrict temporary transforms/materials to presentation clones; keep CAD,
      exports, measurements and collision/approval evidence unchanged.
- [ ] Check transparent wood, metal, LED glow and shadows during transitions;
      avoid flashing, depth fighting and abrupt shadow jumps.
- [ ] Support reduced motion and immediate inspection; formal review and static
      exports use the settled scene, never transitional geometry.
- [ ] Measure frame time and memory across repeated representative full-cabinet
      updates. Set a supported-device budget from baseline measurements and use
      an immediate swap if the animation would exceed it.

Acceptance: the user can see which parts were added or changed, can still rotate
the cabinet, and sees the exact completed geometry after motion settles. No
fabrication meaning is attached to the visual order of appearance.

### WP5d — Preview and export command integration

Separate PR: expose the proven live experience through the shared command interface.

- [ ] Route preview to the live session and existing GLB/Blender/review mechanisms.
- [ ] Keep preview/export commands explicit about generated files and viewer
      lifecycle; no hidden model repair or automatic supplier contact.
- [ ] Distinguish prototype exports from manufacturing release. Manufacturing
      output must pass the existing gate; a prototype remains labelled as such.
- [ ] Preserve approved geometry, hardware inclusion and component ownership.
- [ ] Verify actual rotation/zoom and relevant open/closed states where supported.
- [ ] Test hosted delivery separately from a local viewer; unavailable delivery
      is a specific blocker, never an invented pass or inaccessible localhost link.
- [ ] Report continuous updates as unsupported where the host cannot deliver
      them. Offer explicit static/reopenable snapshots there, without describing
      those as a live viewer. No implicit upload of private furniture projects.

Acceptance: exported artifacts correspond to the active checked design; static
images do not satisfy interactive delivery, and visual approval is never inferred.

### WP6 — Adopt contracts across skills and package a candidate

Sixth PR: route skill instructions through the proven command interface.

- [ ] Update specialist handoff/return instructions using the WP1 contract map.
- [ ] Replace scattered public script-path instructions with tested CLI commands
      where parity exists; retain documented escape hatches for uncovered operations.
- [ ] Make review reporting distinguish preview available, evidence current,
      user review pending and fabrication-ready according to existing gates.
- [ ] Instruct the design owner to open the live viewer early and retain it
      through construction. Treat successful-build publication as tool behavior,
      not an extra action the model has to remember after every edit.
- [ ] Update portable packaging, integrity checks, discovery and installation docs.
- [ ] Build and inspect a candidate archive from the current source; do not publish
      a new release automatically or assume the existing v0.1 bundle contains changes.

Acceptance: an installed candidate can execute the same supported commands as
the checkout, with no developer-only path/import workarounds. Existing projects
remain usable without migration. The release document lists platform limitations.

### WP7 — Independent end-to-end acceptance

Final acceptance slice; fixes go into small follow-up PRs at their owning layer.

- [ ] Run fresh standard and custom synthetic projects using only distributed
      entry instructions; include saved-project resume and a deliberate revision.
- [ ] Exercise missing hardware, failed checks and stale approvals as negative cases.
- [ ] Observe a complete progressive run with new, changed and removed parts;
      test interrupted builds, refresh/reconnect, animation interruption and
      entering formal review while newer geometry is being built.
- [ ] Have independent reviewers assess routing, code boundaries and false-ready risks.
- [ ] Run relevant Python/viewer suites and package-integrity checks.
- [ ] Compare repeated questions, unnecessary skill reads and manual path recovery
      against WP1; record failures and limitations, not just successful runs.
- [ ] Report evidence separately for local runtime, hosted runtime, visual delivery
      and manufacturing readiness. Request release approval only after review.

Acceptance: no new false-ready outcomes, no lost saved decisions, no duplicated
construction engine, and demonstrated improvement in agent navigation. Actual
manufacturing still requires the existing project-specific checks and approvals.

## Implementation and review rules

Each numbered implementation slice gets its own branch document and green PR.
Use stacked branches only when a predecessor is still under review; do not accumulate
unrelated refactors on one branch. No force-push, history rewriting or AWS deployment
is part of this plan. No new agent daemon, plugin framework, database or lazy
skill installer. A live viewer session reuses the existing local server lifecycle.

Use OOP command/adapter boundaries with narrowly scoped modules. Review touched
files over 150 lines for separation of concerns; request the required independent
refactor report for existing code over that threshold. Do not restructure unrelated
files. Tests should prove behavior, compatibility and rejection of invalid evidence.

Main risks are lost instructions during extraction, route-specific CLI behavior,
stale evidence being treated as current, and an installed package diverging from
the checkout. WP1 baselines, adapter parity and packaged acceptance address these.
Keep legacy entry points through the migration so a new CLI failure has a known
fallback; reverting a slice must not require rewriting user project data.

## Audit log and proposed decisions

1. Patrick requested this plan following the gstack/HyperFrames comparison.
   Inspection confirmed existing construction and readiness tools; a second
   validation engine would duplicate authority and is not proposed.
2. Proposed for Patrick's review: start with contracts, then routing, then CLI
   adapters. This establishes behavioral baselines before changing invocation.
3. Proposed for Patrick's review: keep detailed intake in a reference initially,
   rather than add another discoverable skill. It reduces entry context without
   expanding installation and routing complexity.
4. Proposed for Patrick's review: retain existing project schemas and evidence
   sources. Any discovered need for new persistent state is a separate decision.
5. Plan only: no implementation, release publication or fabrication approval has
   been performed or implied by writing this document.
6. Patrick explicitly requested an automatically updating viewer during building,
   with animated part appearance. Added this as a core experience requirement,
   split into publication, live refresh, animation and command-integration PRs.
7. Proposed for Patrick's review: publish completed build checkpoints and use
   fade/crossfade transitions first. This shows actual progress without requiring
   CAD topology correspondence or pretending an animation is fabrication proof.
8. Inspection found the current review session explicitly binds immutable GLB
   bytes and a token. The live draft view must preserve that formal approval
   boundary rather than making an approval session silently follow new geometry.
