---
name: aikea-add-lighting
description: Add recessed linear lighting to an AIkea sheet-material furniture part from one saved part-local run. Use when a generated cabinet, wardrobe, shelf, or furniture assembly needs an integrated light groove, a purchased light body, or an illuminated visual review.
---

# AIkea Add Lighting

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

Design the smallest complete purchased-light solution that gives the furniture
the intended light. Treat the host panel, its machining, the purchased luminaire,
and the emitted light as one coordinated feature.

## Build from one saved run

1. Read `references/recessed-linear-lighting.md` completely.
2. Identify the owning part and its local face plane. Save the light run as two
   endpoints in that plane; do not duplicate its placement in separate models.
3. Select a verified purchased-luminaire profile suitable for the installation.
   Let the profile own its groove and product dimensions.
4. Use the saved run to create the panel groove, place the purchased light, and
   place the emitted light. Keep all three aligned to the same local frame.
5. Check that the complete groove stays inside the host face, retains material
   behind it, and accepts the purchased-light envelope without solid overlap.
6. Export an unlit and lit visual review from the same GLB. Explain the useful
   physical result rather than reciting the workflow.
7. After the standalone profile is approved, save the chosen run with its owning
   generated part. Rebuild that one cabinet with the groove and purchased light,
   then show the actual interior illumination.
8. Stop for the client's cabinet approval before repeating the lighting pattern
   across the furniture or creating an eval set.

For the first standalone proof, run:

```bash
python <this-skill>/scripts/generate_lighting_panel_review.py \
  --output-directory <project>/build/lighting-panel-review
```

This first proof is a straight run in one rectangular 18 mm panel. It establishes
the reusable run-to-groove-to-light contract; it is not permission to infer a
cabinet installation position.

After that profile is approved, save one cabinet placement with:

```bash
python <this-skill>/scripts/add_cabinet_lighting.py <project>/aikea.yaml \
  --assembly-id <cabinet-id> \
  --part-id <host-part-id> \
  --base-builder-module <current-composed-builder> \
  --run-id <stable-light-id> \
  --start <face-x> <face-y> \
  --end <face-x> <face-y>
```

Then export that cabinet with:

```bash
python <this-skill>/scripts/generate_cabinet_lighting_review.py \
  <project>/aikea.yaml \
  --assembly-id <cabinet-id> \
  --part-id <host-part-id> \
  --base-builder-module <current-composed-builder> \
  --hardware-directory <verified-existing-hardware-source>
```

The generated cabinet keeps `lighting.yaml` beside its owning part. Its local
builder adds the groove after earlier machining, and the cabinet builder records
the complete luminaire as one purchased item. The review report must expose the
part, face, run, and cabinet frames so local-to-global placement remains visible.

## Keep responsibilities local

- The host part owns the groove and its local placement.
- The purchased profile owns manufacturer dimensions and electrical facts.
- The furniture assembly owns the host part's placement in the complete model.
- The viewer derives emitted-light placement from the purchased-light node in
  the exported assembly.

Do not design mains wiring, certification, custom LED electronics, or a power
supply enclosure. Do not model loose channels, diffusers, clips, or end caps when
a verified complete luminaire meets the design goal with fewer installed parts.
