---
name: aikea-source-hardware-cad
description: Find exact manufacturer CAD for purchased furniture hardware, guide the user through any required vendor download, and store the untouched files in an AIkea project's local hardware library. Use when a runner, hinge, bracket, lift, or other bought component needs exact CAD before sizing, placement, or visual review.
---

# AIkea source hardware CAD

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

## Goal

Give later AIkea builders the exact purchased component they are designing
around. Match the manufacturer, product family, catalogue item, size, and handed
set before accepting a file. Preserve the downloaded bytes and their original
coordinate frame so local construction can verify and place them later.

## Source and store one product

1. Resolve the active project from its completed `aikea.yaml`.
2. Read [references/sourcing-and-storage.md](references/sourcing-and-storage.md)
   completely.
   If an available item does not fit or a required source is missing, also follow
   [the hardware recovery flow](references/resolve-missing-hardware.md). Keep the
   requested furniture features and dimensions in scope while resolving their hardware.
   Select hardware to fit the intended design, including unregistered products;
   do not silently narrow cabinets/doors/fronts or add fillers/cover panels to fit
   the current hardware cache. Dimensional or layout compromises require an
   explicit user request or approval. Continue through source/profile integration
   and actual fixing/motion checks before treating the better candidate as solved.
3. Start from the manufacturer's official product page and catalogue item. Use
   its own CAD link when available; do not select a visually similar component.
   For **every Hettich item**, first read and execute the
   [Hettich browser download procedure](references/hettich-cad-download.md), then
   the product-specific reference below. This includes newly sourced articles.
4. Prefer a complete STEP assembly in millimetres. Confirm whether one download
   contains the complete pair or whether separate handed files and accessories
   are required.
5. When a vendor provides a public direct download whose terms permit automated
   retrieval, save it unchanged. Otherwise use the normal browser download flow
   yourself when browser tools are available. A portal is not automatically a
   user-only task. Ask for help only at an observed step requiring the user's
   action, such as personal authentication, agreement or an unavailable download
   capability. Prepare the exact item and format first, explain that one step,
   then resume retrieval and verification. Never collect or save credentials.
6. After the file reaches the computer, run:

   `python <skill-directory>/scripts/store_hardware_cad.py <project>/aikea.yaml --manufacturer <name> --product-family <family> --catalog-item <item> --product-url <official-product-url> --cad-page-url <official-cad-url> --terms-url <terms-url> --download <downloaded-file>`

7. Use the returned `hardware_directory` for the relevant AIkea construction
   skill. Sourcing proves identity, provenance, and unchanged bytes only. The
   consuming skill must still verify solids, native bounds, placement, fit, and
   machining before it can treat the hardware as build-ready.

For Hettich KA 5332 article 9057405, also read
[references/hettich-ka-5332.md](references/hettich-ka-5332.md).
For the Hettich KA 4532 runner and its approved 13952 spacer, instead read
[references/hettich-ka-4532-spacer.md](references/hettich-ka-4532-spacer.md).
For the 400 mm KA 4532 article 9114274, read
[the verified download route](references/hettich-ka-4532-400.md). This is a sourced
candidate, not an approved shorter version of the 500 mm installation.
For SL 322 hanging-rail support **70664**, read
[the configured support download and native datums](references/hettich-sl322.md).

For GRASS Tiomos 155 Plus F028122660 and its F058139748 plate, use
[the verified public STEP archive route](references/grass-tiomos-155-plus.md).
Do not stop at the separate configurator's login screen.

## Project storage

Purchased CAD is shared project input, not part of one cabinet assembly:

```text
<project>/hardware/<manufacturer>/<product-family>/<catalog-item>/
├── source-record.json
└── source/
    ├── <original-download>
    ├── <exact-cad-file>
    └── <vendor-supplied-notices>
```

The `hardware/` library is local-only and ignored by Git. The public AIkea skill
may keep product identity, source links, checksums, and verified observations,
but never the vendor's CAD bytes.

## Responsibility boundary

This skill owns exact product discovery, the user download handoff, unchanged
local storage, and source provenance. It does not decide cabinet geometry,
articulate unavailable motion, infer mounting transforms, or approve fabrication.
Those decisions remain with the hardware-specific construction and review skills.
