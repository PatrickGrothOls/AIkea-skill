# Fresh Vilja construction checkpoint

This project was authored from a blank shared AIkea project using the supplied room measurements and untouched vendor CAD. It contains four bays, six captured-bottom drawer subassemblies, thirteen shelves, two base deck sections and sixteen Korrekt feet.

This is an inspection checkpoint, **not fabrication release**. Current geometry still uses the rejected NC70 width/filler workaround and its wide-front pullout fails. The replacement Blum source and installation preparation are saved separately; no replacement source geometry is fabricated or relabelled as imported.

Run from the fresh worktree through `direnv exec . python local-evidence/fresh-project/tools/build_review.py` after restoring the documented raw hardware cache. Source CAD and generated STEP/GLB/DXF are intentionally not versioned here. The recipe uses this worktree's shared tools. It runs one native OCCT thread and emits lit inspection geometry before expensive manufacturing exports. Actual full collision and fabrication checks can fail and are retained as evidence.

The selected lighting variant is DOMUS APEX84 HI4300 K. Drawer layout evidence declares actual floor, cap, side and single-front paths; the shared gate runs before export. Physical screw/material/load, final door travel, anti-tip fixing and Blender presentation remain open. See `docs/vilja-fresh-restart.md` for current status and limitations.
