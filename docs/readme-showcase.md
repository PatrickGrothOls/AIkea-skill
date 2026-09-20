# README furniture showcase

## Scope

Use Patrick's two supplied cabinet images in the repository README. Show the
assembled design first, then the exploded assembly, with a concise explanation
of AIkea and a clear distinction between the available repository workflow and
the desktop installation flow still being tested.

## Current state

README and image assets prepared on docs/readme-showcase from origin/main
d593d31. Exact supplied JPEGs retained without retouching. Existing alpha,
fabrication, hardware and license limitations retained. All local README links
resolve, both images match their sources byte for byte, and the diff is reviewed.
Completed as one documentation checkpoint. Nothing published.

## Work packages

- [x] Inspect the current README and preserve technical and license guidance.
- [x] Add the two original images using repository-relative paths and alt text.
- [x] Introduce the design/review flow and current installation status.
- [x] Check links, exact image copies and the final diff.
- [x] Commit this documentation-only change separately from the installer.

## Audit log

1. Patrick requested a README using these two attached images while desktop
   acceptance testing is pending. Assembled-first and exploded-second follows
   the intended whole-design-to-parts review sequence.
2. Installer status refers to the completed isolated runtime trials recorded in
   feat/desktop-installer. It explicitly leaves desktop Work/Cowork acceptance
   pending and does not claim an available public starter URL.
3. Verification passed for local Markdown links, HTML image paths, exact source
   checksums and whitespace. No production code changed, so no runtime suite was
   needed. Image assets total approximately 227 kB; no new rendering dependencies.
