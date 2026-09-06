# Drawer stack density

## Scope

Make automatically arranged drawer stacks use their vertical capacity while
keeping every purchased runner on its resolved mounting row and preserving any
drawer height explicitly chosen by the client.

## Workpackages and tasks

### 1. Shared calculation

- [x] Calculate a box height from each resolved drawer bottom, its next physical boundary, and the preferred clear gap.
- [x] Preserve explicitly fixed drawer heights.
- [x] Support equal automatic heights when a matching set is part of the design.

### 2. Skill guidance

- [x] Route automatic drawer stacks through the shared calculation.
- [x] Keep the exact arithmetic in code and the client conversation focused on the visible capacity and hand clearance.

### 3. Verification

- [x] Verify six-row, five-row, equal-height, fixed-height, and impossible-height examples.
- [x] Validate the updated skill package.

## Current state

The shared height planner is implemented and verified. Six mounting rows produce
170 mm boxes with 22 mm clear gaps; five rows produce 138 mm boxes with the same
gap. Fixed client heights remain unchanged, and impossible overlaps are rejected.
The active cabinet visual remains a separate approval artifact.

## Audit log

1. 2026-08-31 — the maintainer identified excessive air between drawer boxes as both wasted capacity and a visibly unfinished result. Automatic drawer heights will therefore be derived from the real mounting intervals and a deliberate clear gap; explicit client heights remain authoritative.
2. 2026-08-31 — The current design target is a 22 mm clear gap. It remains configurable so different handles, fronts, or client preferences can produce a different intentional result without changing the mounting-grid calculation.
