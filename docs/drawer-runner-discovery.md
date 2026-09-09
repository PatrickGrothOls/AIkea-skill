# Drawer runner discovery workflow

## Scope

Teach the drawer skill to derive hardware requirements from the current cabinet,
reference the existing hardware-sourcing skill to find suitable exact products,
and resume drawer verification with the returned evidence. Remove the implicit
Hettich article choice. Keep existing exact-product builders and verification
requirements; this branch does not add an unverified runner or change the PDF
design's other construction capabilities.

Patrick authorized this workflow and reuse of the sourcing skill in this thread.

## Current state

Workflow implementation and validation complete on
`feat/drawer-runner-discovery`, isolated from
`origin/main` at `52f3dbc`. The source skill already owns manufacturer discovery,
download access and provenance; the missing connection is requirements-led
discovery before drawer profile selection and its construction handoff. Both
independent selection scenarios passed. No runner-specific construction code
changed; the installed skills still resolve to main until this branch is merged.

## Workpackages

- [x] WP1: Verify baseline, existing sourcing responsibility and runner restrictions.
- [x] WP2: Replace the fixed-product drawer default with cabinet-led sourcing.
- [x] WP2: Document the sourced-product verification and construction handoff.
- [x] WP2: Extend existing sourcing guidance for requirements-led discovery.
- [x] WP3: Validate skills and references; independently exercise realistic cases.
- [x] WP4: Review the diff, record actual results and commit one coherent checkpoint.

## Validation

- Both skills pass `skill-creator/scripts/quick_validate.py`; all 15 local
  Markdown references and the new handoff anchor resolve. Staged diff checks pass.
- A fresh subagent used the edited skills and live official sources with a
  synthetic cabinet: 440 mm clear depth, 500 mm clear width, 200 mm clear height,
  15 mm drawer sides, 25 kg total moving load, full extension and no obstructions.
  It found Quadro V6 420 mm articles 9047747/9047748 plus catches 9144597; their
  published 433 mm installation depth fits that bound. It correctly reported
  candidate-only status, unresolved construction details, missing STEP sources
  and absent Quadro integration instead of calling discovery a completed build.
- In a separate exact-choice scenario it preserved 9114276/13952 and identified
  both the 504 mm depth requirement and 20 kg spacer limit as conflicts. It
  requested a client decision instead of substituting hardware or changing the
  cabinet/load requirements.
- Evidence and complete official links are retained in
  `/private/tmp/aikea-runner-forward-evidence/scenario-1-selection.md` and
  `/private/tmp/aikea-runner-forward-evidence/scenario-2-exact-choice.md`.
  These are selection/handoff tests, not geometry, machining or fabrication tests.

The commands below reproduce the static checks from this worktree:

```sh
direnv exec . python /Users/patrickolsen/.codex/skills/.system/skill-creator/scripts/quick_validate.py aikea-build-drawers
direnv exec . python /Users/patrickolsen/.codex/skills/.system/skill-creator/scripts/quick_validate.py aikea-source-hardware-cad
direnv exec . git diff --check
```

## Audit log

1. Patrick requested suitable-runner discovery and explicitly asked to reference
   existing sourcing guidance from the drawer skill. This supplies the scope and
   responsibility split for the change.
2. Fetched `origin/main`; created the isolated worktree at
   `/private/tmp/aikea-drawer-runner-discovery`. Existing main and `dist/` preserved.
3. Confirmed the drawer skill chooses an exact Hettich article for a broad Hettich
   request and only invokes sourcing when selected-profile CAD is absent. Current
   catalogs contain limited verified lengths; catalog rejection is not evidence
   about market availability.
4. Verified the existing official Hettich shop and Blum Product Database entry
   points live before adding reusable discovery directions. No product chosen.
5. Linked drawer selection to the sourcing skill, moved cabinet suitability and
   profile-integration guidance into a drawer reference, and extended the existing
   sourcing reference with discovery entry points and return evidence. Product
   implementations retain their exact verification boundaries.
6. Both modified skills pass the skill-creator validator; `git diff --check`
   passes. An independent subagent is exercising a synthetic 440 mm clear-depth
   cabinet and a separate explicit-product conflict. These are workflow tests,
   not measurements or a completed model of Patrick's PDF design.
7. Reviewed both independent outcomes and their official source evidence. The
   workflow discovered a product outside the bundled catalog and preserved an
   incompatible explicit selection with a precise client handoff. No behavior
   correction was needed after the forward test. Reviewed the six-file diff for
   the local checkpoint; no runtime, vendor CAD or evaluation scratch files are
   included in the feature branch.
