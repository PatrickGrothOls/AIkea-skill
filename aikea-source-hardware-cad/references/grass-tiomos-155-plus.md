# GRASS Tiomos 155 Plus: public native STEP route

Verified 2026-09-16. This is a sourced option, not a universal hinge or a completed
load/motion qualification. Select the exact installation before downloading.

## Download without a portal login

The official [CAD catalogue](https://www.grass.eu/en/tec-center/cad-data/) provides
public product-group ZIPs, independently of its logged-in iFurn configurator.
Open the catalogue, choose Tiomos, then the 155 Plus and mounting-plate downloads.
The verified direct links are:

- [TIOMOS_155_PLUS.zip](https://www.grass.eu/fileadmin/user_upload/grass.eu/Downloads/Tiomos/TIOMOS_155_PLUS.zip)
- [MOUNTING_PLATES.zip](https://www.grass.eu/fileadmin/user_upload/grass.eu/Downloads/Tiomos/MOUNTING_PLATES.zip)

Download both unchanged using the host's network tools. Inspect archive member
names and extract only the exact selected STEP; multiple variants share each ZIP.
Retain the original archive and its URL/checksum in the local provenance record.
Do not put downloaded vendor bytes in the public skill or Git.

| Item | Exact STEP member | SHA-256 |
| --- | --- | --- |
| F028122660, screw-on damped K3 hinge | `F028122660_TIOMOS 155 PLUS_C03_DRILL 45_9-5_SCREW.step` | `823644b3ec2683fb40307bf66154c6e2c5c80d43cb28b4bc4e1b6a8f66bd8c2a` |
| F058139748, 3 mm screw-on plate | `F058139748_TIOMOS 1D CROSS PLATE_H03_DRILL 37_SCREW.step` | `8a043f77f0c595d8dc621d670218218732555c15f1879b905f55c6d4c0180c84` |

Store each selected STEP through `store_hardware_cad.py`, manufacturer `grass`,
families `tiomos-155-plus` and `tiomos-1d-cross-plate`, lowercase article IDs.
Use the official CAD page above and [terms page](https://www.grass.eu/en/terms-and-conditions/).
The resulting paths under `hardware/grass/` match `GrassTiomos155Loader`.
It checks unchanged bytes, one valid solid per item and native millimetre bounds.
A checksum change requires source re-verification, not disabling the check.

If the direct links change, revisit the official catalogue rather than guessing
URLs. A login redirect from iFurn does not mean the public ZIPs require login.
If user action is genuinely necessary, provide the exact link and observed
screenshots/steps; never claim a download succeeded before verifying the file.

## Hand back to construction

Read [the GRASS installation guide](../../aikea-build-doors/references/grass-tiomos-155-plus.md).
Source success is not completion: build the matching plate, fixings and actual
panel cuts, then check closed fit and movement against the whole furniture.
