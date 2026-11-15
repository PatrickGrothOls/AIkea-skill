# WardrobeAgentWizard release

## Scope

Patrick selected WardrobeAgentWizard as the public product name. Update public
entrypoints, viewer branding, release packaging and official links while keeping
the existing `aikea*` construction modules, saved files and environment variables
compatible. This is a product rename, not a claim of trademark clearance.

Branch `codex/wardrobe-agent-wizard` stacks above the tested reporting change and
the independently committed installer-checksum fix. No client projects change.

## Work packages

- [x] Record the selected name and inspect the current public release surfaces.
- [x] Add the new public skill entrypoint and update visible branding.
- [x] Update packaging and version checks, retaining legacy release recognition.
- [x] Rebuild the viewer and inspect phone, tablet and desktop captures.
- [x] Verify reporting, download counts and update behavior.
- [x] Verify the complete renamed release archive and its checksum.
- [ ] Prepare the release artifact, official links and publication checkpoint.

## Current state

The reporting implementation is locally verified but hosted reporting remains
inactive. The Google configuration check was rejected by automatic approval
review; this rename does not authorize a credential change or bypass that block.
Download visibility uses GitHub's release counts without client telemetry.
The renamed `v0.1.1` archive is built from `e748e4c`. Full archive integrity,
all 13 skill entrypoints, the exact stamped release identity and exclusion of
operator infrastructure/private runtime files are verified. Its checksum is
pinned in `START_HERE.md`. Hosted reporting remains inactive in this archive.
Focused Python verification passes: 50 tests and four packaging subtests. The
receiver's six tests and all 13 discoverable skill links pass. Package generation
now stamps the exact release version automatically and keeps the public alias.
The viewer's 89 tests and both production builds pass. Responsive captures of the
actual header components use an explicitly labelled offline fixture; the public
showcase captures use the built site with its real model loaded. No horizontal
document overflow was measured at any of the three widths.

| Viewport | Review wordmark width | Review header width | Public header width |
| --- | ---: | ---: | ---: |
| 390 × 844 | 150 px | 366 px | 390 px |
| 820 × 1180 | 188.6 px | 786 px | 820 px |
| 1440 × 1000 | 285 px | 1406 px | 1440 px |

The review-wordmark container occupies 41.0%, 24.0% and 20.3% of its header,
respectively; the existing container sizing is preserved. New review typography
uses the 21/13 Fibonacci pair. Detailed measurements and six reviewed captures
are in this chat's Codex artifacts under `launch/branding-review/`.

## Visual constraints

Preserve the existing viewer layout and forest-green identity. Replace the old
image wordmark with accessible text. Retain the existing header width; the new
two-line wordmark uses 21 px desktop and 13 px phone type (21/13 ≈ 1.615).
The wardrobe remains the primary content; review controls and geometry are unchanged.
Record measured header bounds with the final responsive captures.

## Audit log

1. Patrick corrected his naming choice to WardrobeAgentWizard. Use that spelling
   consistently on public surfaces.
2. Preserve internal names so an emergency rebrand does not migrate existing
   furniture specifications or construction code.
3. Add a neutral public entrypoint and keep legacy commands available. Recognize
   both legacy and renamed official release assets during version comparison.
4. The Vite development server advertises the compressed model with HTTP gzip
   encoding, which causes double decoding in the showcase loader. Verify the
   production static build, whose model loads correctly; no unrelated geometry
   or loader change is included in the rename.
