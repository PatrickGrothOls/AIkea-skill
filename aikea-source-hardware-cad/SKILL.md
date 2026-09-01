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
3. Start from the manufacturer's official product page and catalogue item. Use
   its own CAD link when available; do not select a visually similar component.
4. Prefer a complete STEP assembly in millimetres. Confirm whether one download
   contains the complete pair or whether separate handed files and accessories
   are required.
5. When a vendor provides a public direct download whose terms permit automated
   retrieval, save it unchanged. When access requires registration, personal
   agreement, or a protected portal, open the exact page and give the user one
   clear action: choose the stated format and complete the download. Never collect
   or save their credentials.
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
