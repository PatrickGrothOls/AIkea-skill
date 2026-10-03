# Included lighting: pricing and removal

## Design and quote

Include lighting in new designs and in the quoted total by default. Its position
and product must fit the current furniture; the default is not a fixed run on
every panel. Preserve a client's explicit opt-out and show `Lighting: excluded`
in that quote. The existing generator supports one saved lighting feature per
cabinet; do not call it repeatedly expecting it to accumulate multiple runs.

Give Lighting its own section in every price overview:

| Lighting item | Basis |
| --- | --- |
| Complete luminaires | Exact product, saved run lengths and quantities |
| Compatible power supply | Actual combined load and selected manufacturer's sizing guidance |
| Switching/sensor and low-voltage connections | Selected controls, leads and connectors |
| Lighting machining | Incremental groove and cable-exit operations actually generated |
| Lighting subtotal | Included in total; show the saving if lighting is removed |

Use dated supplier prices on the same VAT/currency basis as the rest of the
quote. Count each purchased luminaire once even if the viewer separates body
and emitter meshes. Keep these items out of the general hardware subtotal, and
lighting machining out of the general CNC subtotal, to avoid double counting.
Never price an unknown supply, control, route or machining time at zero. Mark
the section provisional and identify the missing input. Do not claim an order
price until all included items have prices. Use verified off-the-shelf electrical
components; this section does not authorize custom mains wiring design.

## Remove as one module

The unlit cabinet builder retains all normal panel machining. Lighting adds its
groove and purchased body through `lighting.feature` in `features.json`.

Run in the active environment:

```bash
python <skill-directory>/scripts/remove_cabinet_lighting.py <project>/aikea.yaml --assembly-id <cabinet-id>
```

This removes only the lighting registration. It retains the saved plan for reuse
and leaves drawer, door and other feature registrations intact. Rebuild through
`complete_builder.py` in a fresh process so cached imports do not retain the old
feature list. Re-export geometry, BOM, machining and the quote. Do not merely
hide emitter meshes: the unlit version must have no lighting grooves or hardware.
Remove only lighting-owned cable features and costs; preserve shared services.

Re-enable using `add_cabinet_lighting.py` with the saved plan's exact inputs. No
physical placement should be inferred from the default. Use the lit/unlit preview
to approve the first cabinet before repeating it across the run.
