# Hardware CAD sourcing and storage

Use this reference for every purchased component before a hardware-specific
builder consumes it.

## Choose the source

Start with the consuming skill's physical requirements when no exact article is
selected. Follow a requested manufacturer or family; otherwise search suitable
manufacturers without promoting an old prototype to a default. The package's
registered profiles are reusable knowledge, not an exhaustive product catalog.

Official starting points for runner discovery include:

| Manufacturer | Where to look |
| --- | --- |
| Hettich | [Hettich shop](https://shop.hettich.com/): open Runner systems, narrow the mounting/closing system and length, then read the exact article's technical details, installation downloads and Hettich CAD link. |
| Blum | [Product Database](https://www.blum.com/us/en/services/e-services/productdatabase/): use the product hierarchy or search to find the exact runner, technical attributes, planning drawings and CAD. Follow the relevant regional catalog/configurator for sizing. |

These are entry points, not exclusive brands or required products. Use another
manufacturer's official catalog when appropriate. Public search may locate an
official page or installation sheet when a portal is difficult to navigate;
search snippets or retailer descriptions alone do not establish compatibility.

Compare the facts the caller needs: exact length and minimum installation space,
mounting arrangement, width/material limits, load class and its conditions,
extension/closing behavior, required accessories and available CAD. Record an
official URL and document/page for each decisive planning value. Do not transfer
specifications between nearby lengths, hands or load classes. Return unresolved
facts for the consuming skill to handle before declaring fit.

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

Discovery returns exact candidates and the official evidence needed to compare
them, including remaining fit or access questions. Storage is complete when the
selected product's required handed set and companions are accounted for and
their source records identify the actual CAD files. A single STEP can contain a
complete pair; one file alone does not prove completeness.

Hand the source directory, selected identities, planning evidence and any missing
components back to the consuming skill. It owns geometry, profile integration,
fit and movement verification; do not call a stored download build-ready.
