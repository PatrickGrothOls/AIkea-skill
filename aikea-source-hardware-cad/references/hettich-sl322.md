# Hettich SL 322 hanging-rail support

Exact article **70664**, nickel-plated die-cast zinc, three screw holes.
Use with the 30 x 15 mm oval wardrobe rail. This is a product-source recipe;
installation is owned by [hanging rails](../../aikea-build-units/references/hanging-rails.md).

## Official sources

- [Dimensioned drawing](https://catalog.hettich.com/General/TA_2025/en_DE/catalogs/TA_2025_en_DE/pdf/save/bk_974.pdf), printed page 972.
- [Configured CAD portal](https://hettich-embedded.partcommunity.com/?encoding=%25&info=hettich%2Fcabinet_interiors%2Fwardrobe_sys%2Fwardrobe_rail_support%2Frail_support_sl322.prj&languageIso=en&varset=%7BARTICLENO%3D70664%7D).
- [Public DWG/DXF archive](https://web2.hettich.com/hbh/addon/cad/70664_3d.zip).

## Download flow

Open the configured portal with browser tools, or give the link to the user when
browser control is unavailable. Confirm the actual table says **70664**; a generic
family link can select 9056579 instead.

1. Click **CAD**. If no format is selected, choose **Add formats**.
2. Select **Download**, then **STEP AP214 (3D)**. Click the green plus beside the
   format name if the hidden checkbox does not respond.
3. Click **CAD** again. Wait for **Files** to show **70664 (CAD)** and **Download**.
4. Download the ZIP, inspect it and import its STEP before reporting success.
   Keep the original archive, vendor notice, checksum and unmodified native axes
   in the project's private hardware library.

Observed 2026-09-21: generation worked without a login. The generated download was
blocked by the browser (ERR_BLOCKED_BY_CLIENT); direct HTTP returned 403. The
public archive downloaded successfully and contains a 3D DXF with one ACIS body,
three 2D DXFs and a DWG, not STEP. Do not rename it. Follow the verified conversion
workflow in [missing hardware](resolve-missing-hardware.md) or finish the portal
download. Fusion was available but app capture failed in this session.

## Verified datums

The drawing specifies hole heights 0, 9.5 and 32 mm, with 4 mm countersunk screws.
The official 3D DXF ACIS surfaces independently show fixing cylinders of radius
2 at native (X,Y,Z) = (0,0,0), (0,0,9.5), (0,0,32). Native X runs away from the
mounting face; Z is up. The cradle's lower circular surface has centre Z=3.9 and
radius 7.6, so the seat bottom is Z=-3.7 and a 30 mm rail's centre is Z=11.3.
No load rating or panel-specific screw pull-out capacity is provided here.

After obtaining STEP, verify these datums, units, support bounds and the unchanged
body before passing it to `HangingRailFeature`. A successful download alone does
not prove the installation fits.

Observed original 3D DXF SHA-256: `ba9355509dc362a0c987fbe9d517ada1dba18e2969a6f6e76448c2e4f8b94e4f`.
