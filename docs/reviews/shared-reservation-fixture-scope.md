# Shared hardware reservation fixture: scope review

Reviewed 2026-09-12 on `test/shared-construction-regressions`.
Scope: the inherited `tests/test_panel_hardware_reservations.py`, now 157
lines, and its current fixture usage. No production or test code was changed;
no tests were run as part of this responsibility review.

**Recommendation: keep the fixture local; no extraction is required.**
The file has one coherent test responsibility: ensure runner, hinge and shelf
occupancy use the same physical reservation rules, beyond merely avoiding
shared System 32 nodes.

| Concern | Lines | Assessment |
| --- | --- | --- |
| Minimal panel and cabinet inputs | 22-71 | These private fixtures provide the one fixed geometry used by the resolver scenarios. The new support frames, inside faces and clear-space dimensions satisfy the current host contract rather than add another test concern. |
| Reservation envelope and node semantics | 77-104 | These establish the distinction the resolver scenarios depend on: hardware can physically conflict without sharing a node. |
| Cross-feature placement behavior | 106-153 | Runner placement around hinges, hinge placement around runners and shelf clearance belong together because they verify the shared reservation contract from both consumers. |

The fixtures are private to this test module and no external consumers were
found in the related reservation and drawer-host tests. Extracting them now
would move roughly fifty lines behind another import without reducing
coupling or duplicated setup. Splitting tests by hardware product would also
separate the cross-feature behavior this file is specifically meant to cover.

Keep the fixture's limited scope explicit: its `local_to_parent` property
models the two support-panel frames; the non-left branch is not a general
placement rule for every part. If future tests need placed door/shelf geometry
or differently named supports, give those fixture parts explicit placements
rather than extending the name-based inference. If that richer fixture then
has another independent consumer, extract a focused reservation-test project
helper at that point.

The 150-line threshold has prompted a responsibility review, not a numerical
reason to split this currently coherent test module.
