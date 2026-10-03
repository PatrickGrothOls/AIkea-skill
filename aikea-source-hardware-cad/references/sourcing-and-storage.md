# Hardware CAD sourcing and storage

Use this reference for every purchased component before a hardware-specific
builder consumes it.

## Choose the source

Establish the exact manufacturer, product family, catalogue item, nominal size,
handedness, and required companion parts from the official product page. Follow
the manufacturer's own CAD link before considering a third-party catalogue. A
file for another length, hand, load class, or mechanism is a different product,
even when its visible shape looks interchangeable.

Prefer STEP when available because AIkea's deterministic CadQuery import can
inspect its solids and preserve its native millimetre frame. Never scale,
recenter, mirror, simplify, or repair source CAD during storage. Import and rigid
placement are later, separately evidenced operations.

## Handle vendor access

Read the current download terms at the time of use. A public direct file may be
retrieved when its source permits that access. Use available browser tools for
the normal configured-item, format, generation and download steps. For Hettich,
execute the [shared browser procedure](hettich-cad-download.md).

If an observed step requires personal authentication, confirmation or agreement,
prepare the exact item and ask the user for that action only. Resume the remaining
browser steps after it is completed; do not transfer the whole sourcing task to
the user merely because a portal exists. Without browser capability, provide the
configured link and visual guidance. Never store credentials, accept agreements
without required authorization, bypass access controls or disable protections.

Keep vendor files local. Do not place CAD bytes in the public skill, an eval
fixture, a model prompt, or a source-control commit. Use local deterministic CAD
tools to inspect them and return only the measurements and checksums needed by
the construction workflow.

## Storage authority

`HardwareCadStore` resolves the library from `<project>/aikea.yaml` and creates:

```text
hardware/<manufacturer>/<product-family>/<catalog-item>/
├── source-record.json
└── source/
```

It retains the original download, safely expands ZIP archives, records SHA-256
checksums for every stored file, and writes the exact source URLs. The returned
`source/` directory is the only directory later hardware resolvers should read.

The generated `hardware/.gitignore` excludes the complete local library. Public
machine-readable manifests live with the consuming AIkea skill and contain only
the evidence required to recognize a previously approved source file.

## Completion

Finish this stage when the exact requested item and original download are stored,
the source record contains their checksums, and the STEP actually imports with
the expected units, valid solids and native bounds. A filename or download click
alone is not proof. Hand the source directory to the consuming skill and resume
installation; that skill owns placement, fixing, movement and fit verification.
