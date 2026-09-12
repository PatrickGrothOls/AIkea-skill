# Construction startup routes

## Scope and current state

Branch `fix/construction-startup-routes` closes reproducible setup failures from
the fresh-model standard and custom trials. Implementation, actual CLI reruns, targeted regression and independent review
are complete. Final candidate integration remains in WP7.

## Work package and tasks

- [x] Accept the saved assembly run in the overall calculation CLI by reusing
  the generator's existing adapter, without rewriting the source YAML.
- [x] Place the shared door/drawer specification loader with the common build
  tools so the door CLI does not depend on an undeclared drawer script path.
- [x] Use existing authoritative configured/authored envelope resolution in the
  common build, preserving its actual source in the position evidence.
- [x] Resolve full-wardrobe hardware inside the current project runtime.
- [x] Clarify the Workplane envelope contract and the inherited insert default.
- [x] Rerun the real commands without process-local import workarounds.
- [x] Run regression checks and review using the review skill.

## Audit log

1. The independent standard trial exposed a valid schema-v9 assembly_run being
   rejected by the older calculator CLI, an import from a drawer-only directory,
   and a generated root rejected for using configured measurement authority.
   Reuse the already supported adapter, module runtime and envelope resolver.
2. The custom trial exposed ambiguous envelope wording and an inventory message
   that described historical library input as if the current user supplied it.
   Preserve the configured default but state its project selection/compatibility
   is unverified. No new hardware or material policy is introduced.
3. Open-door posing and CAD Boolean invariance are separate observed defects;
   this startup slice does not mark either resolved or relax geometry checks.


## Validation

- Five new command/configured-root tests passed. Ten existing construction
  position/hardware tests also passed. Initial new-test setup mistakes (the legacy
  fixture has three cabinets, the measurement schema needs three points, and
  runpy needs the real script's parent path) were corrected without weakening
  production validation.
- Independent review: no findings. Fresh modern-v9 and legacy-v8 CLI subprocesses
  return identical 403.2/604.8 mm widths and preserve all input bytes; invalid IDs
  still return structured errors. The real door command reaches the explicit
  missing-vendor-CAD boundary after loading and planning its host.
- An independently generated two-cabinet root exports 24 valid physical panels
  through the common build. Its saved configured-measurement authority reproduces
  at the fabrication gate. The actual full-wardrobe CLI also exports successfully,
  resolving registered hardware within the project-runtime callback.
- Package verification passes for 11 skills; viewer tests pass (26), viewer build
  matches committed output, dependency check and diff whitespace checks pass.
- Prototype/fabrication gaps remain explicit. Open-state placed bounds and CAD
  Boolean consistency are separate following slices.
