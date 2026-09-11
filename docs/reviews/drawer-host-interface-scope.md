# Drawer host interface: scope review

Reviewed 2026-09-12 on `feat/drawer-host-interface`, against `a0ed283`.
Scope: the inherited 156-line `HettichKa4532SpacerCabinetDrawerPlanner` and
its immediate collaborators. This is a responsibility review, not a geometry
or fabrication approval. No code was changed and no tests were run.

**Recommendation: retain the current file; no extraction is required for this slice.**
Its single responsibility is to compose one exact KA 4532/13952 drawer plan
from compatible host, hardware and box inputs. It delegates the underlying
calculations and checks rather than implementing several independent engines.

| Responsibility | Location | Boundary assessment |
| --- | --- | --- |
| Resolve host and reconcile caller datums | planner lines 60–65 | These checks reconcile inputs to this plan. Host geometry and legacy adaptation remain in `DrawerHost` and `StandardDrawerHost`. |
| Place purchased hardware and verify fixing alignment | planner lines 66–74 | Delegated to the mounting planner and alignment checker, which own product geometry and fixing evidence. |
| Size the box and check fit | planner lines 75–98 | The planner translates between mounting and box contracts and checks their agreement. Sizing and spatial fit remain in dedicated collaborators. |
| Compose reservations | planner lines 133–149 | The short helper performs this product's replacement transaction, retains the explicit repetition restriction and delegates envelope construction and collision policy. It does not calculate reservation geometry. |
| Return the complete product plan | planner lines 106–124 | Combining the resolved outputs and preserving blocked machining authority is the orchestration result, not a separate export or machining concern. |
| Enforce selected-product dimensions | planner lines 126–131 | Two small product preconditions belong at this exact-product planning boundary. An additional validator class would only relocate them. |

The new host-based bottom/front references and host-aware reservations extend
the existing orchestration. They do not introduce a second coordinate engine
or put product-specific knowledge into the shared host.

Revisit extraction only if reservation replacement/repetition policy gains
another caller or independent variants. At that point, a focused product
reservation-planning collaborator would be a coherent seam. Moving the
current helper solely to reduce the file below 150 lines would add navigation
without improving separation.

Files inspected:

- `aikea-build-drawers/scripts/hettich_ka_4532_spacer_cabinet_drawer_planner.py`
- `aikea-build-drawers/scripts/hettich_ka_4532_spacer_mounting_planner.py`
- `aikea-build-drawers/scripts/hettich_ka_4532_spacer_hardware_reservations.py`
- `aikea-build-drawers/scripts/drawer_host.py`
- `aikea-build-drawers/scripts/cabinet_drawer_fit_checker.py`
