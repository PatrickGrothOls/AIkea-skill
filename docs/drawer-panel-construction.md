# Drawer children through shared construction

## Scope and current state

WP5b child-construction slice on `feat/drawer-panel-construction`, based on
reviewed shared drilling `da45525`. Implementation and the review skill pass. Preserve each
selected runner recipe and its exact hardware ownership while making saved
drawer sheets and drilling use the common panel builder.

The next drawer slice handles host mounting inputs/operations and the configured
versus custom host proof. This child slice does not complete all of WP5b.

## Work package and tasks

- [x] Make drawer sheet/spec values satisfy the shared construction inputs while
  preserving existing positional callers and explicit material identity.
- [x] Emit KA 5332 drawer fixing holes as editable surface-drilling requests;
  preserve the existing profile dimensions and both hands.
- [x] Route all saved drawer child builders through one shared builder template,
  retaining exact hardware placeholders for the existing hydration path.
- [x] Declare box joinery, mounting and moving/purchased-hardware requirements;
  keep unresolved construction separate from successfully applied holes.
- [x] Verify generated/direct construction parity and selected-profile behavior,
  including material preservation and missing operation evidence.
- [x] Update skill guidance for the migrated child path and remaining host limits.
- [x] Run the review skill and fix/recheck findings. No findings remain.
- [x] Commit this reviewed slice.

## Validation

- Nine drawer-box, MOVENTO-generator and KA 5332-generator tests passed.
- Nine shared-construction parity, hardware-ownership and review-frame tests
  passed. KA 4532 generator and revision tests also passed in the earlier mixed
  run; two new cross-runtime dataclass comparisons in that run were corrected
  to compare values and then passed in the parity group.
- The independent testing reviewer changed the selected runner identity,
  fixing positions/count/depth, materials and bottom outline. Reloaded inputs
  retained those values, both hands matched the prior geometry, and shared
  result validation passed. The review skill reported no findings.
- All nine skill packages and their links verify. Changed code files are below
  the 150-line scope-review threshold. Hardware tests include synthetic CAD
  probes; they do not certify a newly sourced vendor model or physical assembly.

## Audit log

1. The existing five-panel sizing recipes remain optional calculators. Their
   results will be editable shared inputs; no new drawer dimensions, materials,
   screws or joinery policy are selected by this migration.
2. KA 5332's current drawer-side drilling is the geometry reference. KA 4532 plus
   spacer remains unmachined until its existing fixing blocker is resolved.
   Both use the same builder, with explicit different requests and requirements.
3. Saved child builders now execute shared panel inputs. The existing standalone
   box preview remains a sizing aid over the shared blank builder. Box joinery,
   support and installed movement remain explicit obligations rather than being
   inferred from a successful preview.
