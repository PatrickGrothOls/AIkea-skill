# Compose furniture from an envelope and requirements

## Scope and current state

Patrick's direction: the model should design furniture from an envelope and a few requirements using reusable panels, joints, drawers and hardware. A furniture-purpose registry must not determine what it can design. Existing specialised builders remain useful components.

The isolated branch builds on the runner-discovery workflow. The composed runtime and skill route are implemented; nothing is published or installed. The independent prototype and final runtime geometry checks pass. Visual inspection is pending because the Mac was locked. This work changes the design route and supplies an executable composition entry point. It does not claim universal manufacturing capability or silently convert a concept into fabrication approval.

## Workpackages

- [x] Trace the existing registry gate and reusable construction tools.
- [x] Independently review composition boundaries and hidden cabinet assumptions.
- [x] Provide geometry-driven panels and explicit paired-joint composition.
- [x] Initialise a local design without generating a predefined cabinet.
- [x] Build arbitrary nested project-authored assemblies and check actual solids against their envelope and each other.
- [x] Route the main skill to model-led design and document tool discovery and extension.
- [x] Test real novel compositions and preserved existing construction.
- [x] Run an independent skill forward test and review its complete prototype.
- [x] Save the reviewed runtime, tests and skill route as one coherent local checkpoint.

## Audit log

1. User authorised the architectural direction: envelope plus requirements, with rudimentary construction tools available to the model. Custom composition is the default design route; named templates are optional conveniences.
2. Inspection found reusable assembly-tree transforms, CadQuery blanks, paired Cabineo/miter cuts and exporters. The current type registry, role-based panel geometry and implicit System 32 drilling prevent general composition. Reuse the lower-level tools with explicit geometry and machining.
3. Keep generated project contracts and real BuiltAssembly output. A focused generic panel assembly avoids adding cabinet dimensions to arbitrary furniture. Preserve the existing template route for existing projects.
4. Geometric checks must report exact intersections and envelope violations. They do not establish load capacity, hardware suitability, missing requirements or manufacturing readiness; those remain explicit design evidence.

5. Focused geometry and existing Cabineo/flat/base regression checks passed (20 tests plus 62 subtests at the initial checkpoint). Independent review reproduced omitted multi-object Workplane geometry and incomplete custom-tool machining. Added explicit single-Shape and complete-participation contracts with regression tests; compounds remain supported.
6. The independent skill run found a missing sibling import in the documented build CLI. Fixed the CLI bootstrap and tested it in a fresh subprocess without PYTHONPATH.
7. The independent model authored a complete 1200 × 400 × 1000 mm bench/tower prototype: 12 panels, 28 custom tongue/socket joints and 56 participant cuts. It corrected a project-local receiver-placement error caught by the paired-cut check. Geometry and construction reports pass; load, adhesive, fabrication and visual approval remain unverified.

8. Final verification: 27 focused tests plus 62 existing Cabineo/flat/base subtests pass; all 10 skills and their links validate. After refreshing the generated panel contract, the independent full prototype rebuilt with the final runtime and again had 12 parts, zero invalid solids, zero envelope violations and zero overlaps. No shared template registration or prototype-specific primitive was added.
9. Test model and authored evidence remain outside this feature branch at `/private/tmp/aikea-composition-forward-test`. The read-only viewer is `http://127.0.0.1:8772/`; computer use reported the Mac locked, so visual inspection is pending. No visual approval, strength rating or fabrication readiness is claimed.

## Verification evidence

- Skill entry: [aikea-design-furniture](../aikea-design-furniture/SKILL.md).
- Automated regression tests: `tests/test_panel_assembly_design.py`, `tests/test_panel_assembly_extensions.py`, `tests/test_furniture_geometry_check.py`, and the existing Cabineo, flat carcass and base geometry suites.
- Independent prototype: `/private/tmp/aikea-composition-forward-test/reviews/furniture_01.glb`.
- Geometry and construction reports: `/private/tmp/aikea-composition-forward-test/reviews/`.
- Assumptions and commands: `/private/tmp/aikea-composition-forward-test/docs/`.
- Reviewed code files are all below 150 lines. The boundary review retained focused existing renderers instead of adding another furniture-specific branch.

10. Saved one coherent feature checkpoint: runtime, its regression tests, discovery links and the consuming skill instructions belong together. Generated evaluation source and artifacts, vendor CAD and the virtual environment are excluded. Main and installed global skill links remain unchanged; no push or merge.
