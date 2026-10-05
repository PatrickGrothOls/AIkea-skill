# AIkea skill workflow and command interface plan

## Scope and current state

Planning branch: `codex/skill-workflow-plan`, based on public main `2f60a51`.
Patrick requested a plan after comparing AIkea with the installed gstack and
HyperFrames packages. This document proposes implementation; it does not approve
architecture decisions or authorize deployment, release, or manufacturing.

- [x] Inspect current routing, construction protocol, installation and command entry points.
- [x] Compare local gstack workflow tooling and HyperFrames workflow/domain separation.
- [x] Save a phased plan with acceptance criteria and independently mergeable slices.
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

## Proposed ownership

| Layer | Responsibility | Authority it must not acquire |
| --- | --- | --- |
| `aikea` entry skill | Resolve active project and request; select or resume the owning workflow | CAD calculations, duplicate construction policy |
| Intake reference under `aikea` | Guide measurements and shared choices; route material decisions to their owner | Invented measurements or new approval rules |
| `aikea-design-furniture` | Own the design workflow and compose applicable capabilities | Reimplementing builders or certifying unsupported hardware |
| Existing specialist skills | Complete materials, units, doors, drawers, lights and hardware within explicit contracts | Restarting global intake or taking over the whole workflow |
| Shared command interface | Resolve paths/runtime; dispatch existing operations; present consistent results | New geometry logic or a second readiness engine |
| Existing builders and validators | Calculate, build, export and validate actual project artifacts | Inferring user approval from a successful command |
| `aikea-review-unit` and existing fabrication gate | Coordinate review evidence and report manufacturing readiness | Treating an attractive preview as manufacturing approval |

The entry skill routes once for an active workflow, but explicit new user intent
can select a different operation. The owner resumes after specialist handoffs.
Existing project files remain authoritative; do not add a parallel workflow-state
file or migrate `aikea.yaml` as part of this plan. Any later schema need gets a
separate proposal before implementation.

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

### WP5 — Preview and export adapters

Fifth PR: give the agent a consistent way to review and deliver outputs.

- [ ] Route preview to existing GLB/Blender/viewer delivery and review mechanisms.
- [ ] Keep preview/export commands explicit about generated files and viewer
      lifecycle; no hidden model repair or automatic supplier contact.
- [ ] Distinguish prototype exports from manufacturing release. Manufacturing
      output must pass the existing gate; a prototype remains labelled as such.
- [ ] Preserve approved geometry, hardware inclusion and component ownership.
- [ ] Verify actual rotation/zoom and relevant open/closed states where supported.
- [ ] Test hosted delivery separately from a local viewer; unavailable delivery
      is a specific blocker, never an invented pass or inaccessible localhost link.

Acceptance: exported artifacts correspond to the active checked design; static
images do not satisfy interactive delivery, and visual approval is never inferred.

### WP6 — Adopt contracts across skills and package a candidate

Sixth PR: route skill instructions through the proven command interface.

- [ ] Update specialist handoff/return instructions using the WP1 contract map.
- [ ] Replace scattered public script-path instructions with tested CLI commands
      where parity exists; retain documented escape hatches for uncovered operations.
- [ ] Make review reporting distinguish preview available, evidence current,
      user review pending and fabrication-ready according to existing gates.
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
is part of this plan. No new daemon, plugin framework, database or lazy skill installer.

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
