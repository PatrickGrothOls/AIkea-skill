# Hettich KA 4532 runner and 13952 spacer

Use this reference only for the approved 500 mm KA 4532 Silent System runner
and its paired spacer profiles.

## Exact sources

### Runner pair

- Manufacturer: Hettich.
- Product: KA 4532 Silent System.
- Catalogue item: `9114276`.
- Official product page:
  `https://shop.hettich.com/de_EN/Runner-systems/Ball-bearing-runners/Side-installation/KA-4532-Silent-System-ball-bearing-runner%2C-side-installation%2C-dimensions-%28H-x-W%29-46-x-12-7-mm%2C-500/p/9114276`
- Official CAD entry:
  `https://hettich-embedded.partcommunity.com/3d-cad-models/sso/?varset=%7BARTICLENO%3D9114276%7D&languageIso=en&info=hettich%2Fdrawer_runners%2Fball_bearing_slides%2Fmounted_on_sides%2Fka_4532_sisy%2Fka_4532_sisy_asmtab.prj`
- Approved STEP SHA-256:
  `bbc769c02aa3729f345cd957beaa2b5e21df1659609d9e4e1eff7ed97e80a806`.

### Spacer profile

- Manufacturer: Hettich.
- Product: spacer profile, 25 x 486 x 50 mm.
- Catalogue item: `13952`.
- Official product page:
  `https://shop.hettich.com/de_EN/Drawer-systems/Accessories/Spacer-profile%2C-25-x-486-x-50%2C-white/p/13952`
- Official CAD entry:
  `https://hettich-embedded.partcommunity.com/3d-cad-models/sso/?varset=%7BARTICLENO%3D13952%7D&languageIso=en&info=hettich%2Fcabinet_interiors%2Fkitchens%2Finterior_fitting_base_unit%2Finternal_ppd%2Facces_internal_ppd%2F13952.prj`
- Approved STEP SHA-256:
  `d753d47a3cf8713440ef1d97ff4497cd24fb033221b9f1084f5dde7d3426d1cc`.

The vendor CAD remains project-local. The public skill stores only identity,
source links, hashes, and native observations.

## Storage

Store each official ZIP separately with the general hardware command. Use
product families `KA 4532 Silent System` and `KA 4532 spacer profile`, with
catalogue items `9114276` and `13952`. The returned directories must end in:

```text
hardware/hettich/ka-4532-silent-system/9114276/source
hardware/hettich/ka-4532-spacer-profile/13952/source
```

Pass the common project `hardware/` library to the drawer builder only after
both source records exist and both STEP checksums match the public manifest.
