# Hettich KA 5332 drawer hardware

Use this reference for the visually approved 500 mm KA 5332 prototype.

The runner catalog resolves each drawer's requested depth independently. It may
use this article only for a 500 mm drawer. Another depth becomes available by
registering that exact product profile and its verified source CAD, never by
scaling this STEP assembly.

## Local source

Obtain article `9057405` through `$aikea-source-hardware-cad`. Pass its returned
`hardware_directory` directly to the Hettich generator. The expected project
directory ends in:

```text
hardware/hettich/ka-5332/9057405/source
```

Do not ask for or pass an individual STEP path. `HettichKa5332StepAssemblyLoader`
selects `9057405.stp` through the public product manifest, checks its approved
SHA-256 value, imports it unchanged, and verifies the six native solids and
bounds before classifying the paired runner members.

## Construction authority

`HettichKa5332RunnerProfile` owns the manufacturer planning values.
`HettichKa5332DrawerBoxProfileAdapter` converts the side clearance into generic
drawer-box sizing. `HettichKa5332MountingPlanner` places the cabinet and drawer
members from the cabinet's local faces. The review generator may compose those
results, but it must not replace their calculations.

For 500 mm article `9057405`, Hettich's installation sheet defines cabinet-side
fixings at 37, 128, 224, 352, and 416 mm from the cabinet front. The matching
drawer-member fixings are 37, 128, 192, 352, and 442 mm from the drawer front.
The fixing center is 23 mm above the drawer bottom inside a 46 mm installation
envelope. The first cabinet fixing aligns with the front System 32 column;
it occupies a shared node only when its height also matches a shelf row.
The remaining four are separate horizontal machining.

`HettichKa5332System32RowResolver` retains nearest-row placement for saved
grid-snapped layouts. Its exact route preserves compact planned positions and
rejects reservation conflicts. Use [compact stack placement](compact-stack-placement.md)
to size a collection without lifting its first drawer to the shelf-grid start.
`HettichKa5332PanelMachining` applies the handed blind-hole patterns in each
part's manufacturing frame. `hardware-reservations.json` records actual shared
nodes, if any, and the full rail envelope on both sides so other hardware can avoid it.

`generate_hettich_ka_5332_cabinet_drawer.py` saves the wooden box as a
cabinet-owned child, one cabinet-owned purchased runner pair, and the distinct
left and right translations used for all six source members. The visual review
must load that composed child and its saved frames. The composed builder now
loads the saved runner axes and produces the matching panel machining;
drawer-box joinery and manufacturing toolpaths remain later gates.
