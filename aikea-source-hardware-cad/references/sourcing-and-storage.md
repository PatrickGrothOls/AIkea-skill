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
retrieved when its source permits that access. When a portal requires a personal
account, confirmation, or agreement, take the user to the exact configured item
and state the one format to download. Resume after the user confirms the file is
present. Do not automate protected searches, accept agreements for the user,
store account details, or bypass download controls.

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

Finish this stage when the exact requested item is stored and its source record
names at least one STEP file. Do not call it build-ready. Hand the source
directory to the consuming skill, which owns geometry and fit verification.
