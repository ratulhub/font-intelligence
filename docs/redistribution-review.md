# Font Licensing & Redistribution Review

> [!IMPORTANT]
> **Core Mandate**: Do **NOT** assume that *'free for commercial use'* equals *'allowed to redistribute on GitHub'*.
> Many freeware fonts permit commercial design output (e.g. logos, graphics, website text rendering) while strictly forbidding re-hosting, bundling, or redistributing the raw font binary files (`.ttf`, `.otf`) in public repositories.
> **Zero Deletion Policy**: Never delete original license, EULA, or README text files bundled within the source packages.

**Audit Date**: 2026-09-29 | **Total Families Audited**: 103

---

## 1. Executive Summary

| Verification Status | Count | Percentage | Redistribution Policy | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Verified** | **48** | 46.6% | Allowed | 100% compliant under explicit open-source licenses (OFL-1.1, CC0-1.0, Apache-2.0, Fontshare FFL, Ubuntu). |
| **Needs Review** | **42** | 40.8% | Conditional / Prohibited | Commercial design use granted, but public repository redistribution is restricted, ambiguous, or requires proof. |
| **Restricted** | **10** | 9.7% | Prohibited | Proprietary copyright, demo/evaluation cuts, or explicit 'no redistribution' EULAs. Do NOT push binaries to public repos. |
| **Unknown** | **3** | 2.9% | Prohibited | No license file or grant found. Treated as restricted until audited. |

---

## 2. GitHub Publishing & Repository Hygiene Rules

1. **Tier 1 (Safe for Public Git Repository)**:
   - Fonts with status `verified` (e.g. `chillax`, `general-sans`, `ubuntu`, `credit-valley`, `aclonica`) may be hosted, distributed, and bundled in open-source GitHub repositories.
   - Keep the corresponding `OFL.txt`, `LICENSE.txt`, or author notice alongside the binary.

2. **Tier 2 (Internal / Private Use Only)**:
   - Fonts with status `needs-review` (e.g. 1001Fonts FFC, Creative Fabrica, Letterlays) can be used within local client projects to generate web/app interfaces, but raw font files **must NOT be committed to public GitHub repositories**.
   - Add their directories to `.gitignore` if publishing the codebase publicly, or rely on end-user local installation.

3. **Tier 3 (Replace or Purchase)**:
   - Fonts with status `restricted` (e.g. `warriot` [demo cut], `timeburner` [NimaVisual], `antapani` [unspecified copyright]) should be replaced with open-source alternatives or purchased commercially before public distribution.

---

## 3. Verified Fonts (Allowed for GitHub & Redistribution)

Total: **48 families**. These fonts carry formal open-source licenses allowing redistribution, modification, and commercial deployment:

| ID | Family Name | License Name | SPDX ID | Commercial | Redistribution | Modification | License File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `achtung-bravo` | Achtung Bravo | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `aclonica` | Aclonica | Apache License 2.0 | `Apache-2.0` | Yes | **Yes** | Yes | `LICENSE.txt` |
| `arnprior` | Arnprior | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `balhattan` | Balhattan | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `bm-dohyeon` | BM DoHyeon | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `read.txt` |
| `chillax` | Chillax | ITF Free Font License (Fontshare FFL 2.0) | `N/A` | Yes | **Yes** | Yes | `FFL.txt` |
| `credit-river` | Credit River | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `credit-valley` | Credit Valley | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `cuyabra` | Cuyabra | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `SIL Open Font License v1 - cuyabra.docx` |
| `delta-block` | Delta Block | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `1001fonts-delta-block-eula.txt` |
| `die-nasty` | Die Nasty | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `dosis` | Dosis | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `OFL.txt` |
| `free-cheese` | Free Cheese | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `1001fonts-free-cheese-eula.txt` |
| `general-sans` | General Sans | ITF Free Font License (Fontshare FFL 2.0) | `N/A` | Yes | **Yes** | Yes | `FFL.txt` |
| `guanine` | Guanine | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `gudea` | Gudea | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `OFL.txt` |
| `holstein` | Holstein | Public Domain Dedication | `N/A` | Yes | **Yes** | Yes | `holstein.txt` |
| `inflammable-age` | Inflammable Age | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `ithaca` | Ithaca | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `kaph` | Kaph | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `kineks-round` | Kineks Round | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `OFL.txt` |
| `kingsbridge` | Kingsbridge | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `lumierepolis` | Lumierepolis | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `martius` | Martius | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `neuropol` | Neuropol | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `newestshape` | NewestShape | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `SIL - Open Font License.txt` |
| `newshape` | NewShape | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `SIL - Open Font License.txt` |
| `opsilon` | Opsilon | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `raster-forge` | Raster Forge | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `1001fonts-raster-forge-eula.txt` |
| `relish-gargler` | Relish Gargler | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `ruthless-sketch` | Ruthless Sketch | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `LICENSE.txt` |
| `sagewold` | Sagewold | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License-b6e3.txt` |
| `serati` | Serati | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `simply-sans` | Simply Sans | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `SIL - Open Font License.txt` |
| `stampcraft` | Stampcraft | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `1001fonts-stampcraft-eula.txt` |
| `street-cred` | Street Cred | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `styllo` | Styllo | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `LICENSE.rtf` |
| `ubuntu` | Ubuntu | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `LICENCE-FAQ.txt` |
| `ubuntu-condensed` | Ubuntu Condensed | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `LICENCE-FAQ.txt` |
| `ubuntu-mono` | Ubuntu Mono | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `LICENCE-FAQ.txt` |
| `unispace` | Unispace | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `unsteady-oversteer` | Unsteady Oversteer | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `vaticanus` | Vaticanus | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `1001fonts-vaticanus-eula.txt` |
| `viga` | Viga | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `OFL.txt` |
| `vincendo` | Vincendo | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `world-of-water` | World of Water | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |
| `zero-cool` | Zero Cool | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | `License.txt` |
| `zorque` | Zorque | Creative Commons Zero 1.0 Universal (CC0) | `CC0-1.0` | Yes | **Yes** | Yes | `Metadata` |

---

## 4. Fonts Requiring Review (Commercial Design OK, Redistribution Restricted)

Total: **42 families**. Commercial use is permitted for design projects, but raw font files may **NOT** be redistributed on public repositories without written permission:

| ID | Family Name | License Grant | Commercial | Redistribution | Redistribution Review Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `aix-milan` | Aix Milan | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `al-saflers` | Al Saflers | Freeware (Personal & Commercial - Aluyeah Studio Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `alphakind` | Alphakind | Freeware (Personal & Commercial Use Granted) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `ampunsuhu` | Ampunsuhu | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `anak-bijak` | Anak Bijak | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `anak-gedong` | Anak Gedong | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `bakula` | Bakula | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `bedizen` | Bedizen | Freeware (Author Freeware Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `biocats` | Biocats | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `butflow` | Butflow | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `castle-chunk` | Castle Chunk | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `courbe-sans` | Courbe Sans | Courbe Sans Free Standard License | Yes | **No** | Author grants free standard commercial design usage, but does not grant third-party public git repository redistribution rights. |
| `crucial` | Crucial | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `enter-sansman` | Enter Sansman | Freeware (General) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `halo-dek` | Halo Dek | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `heming` | Heming | Freeware (Commercial Use Allowed - Befonts Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `hijo` | HiJO | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `hirolliv` | HiRolliv | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `imuch` | iMuch | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `jazzy-huitbits` | Jazzy HuitBits | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `jazzyrabbit` | JazzyRabbit | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `jazzyrabbit-remake` | JazzyRabbit Remake | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `jogrunge` | JOGRUNGE | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `jumping-chick` | Jumping Chick | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `kalima` | KALIMA | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `kastore` | Kastore | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `marker2` | Marker2 | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `modestic-sans` | Modestic Sans | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `mousou-record-g` | Mousou Record__G | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `oligopoly` | Oligopoly | Freeware (Commercial Use For Everyone - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `paint-marker` | Paint Marker | Letterlays Commercial License (Receipt PDF) | Yes | **No** | Commercial design grant with receipt PDF. Prohibits raw font file distribution or open-source repackaging. |
| `pingsan` | Pingsan | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `progo` | PROGO | Freeware (Free Commercial - Author Grant) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `reckoner` | Reckoner | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `spicy-sale` | Spicy Sale | Creative Fabrica Commercial License | Yes | **No** | Commercial license covers end-product creation by licensee. License text strictly prohibits redistributing, sharing, sublicensing, or extracting raw font binary files. |
| `super-joyful` | Super Joyful | Freeware (General) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `super-malibu` | Super Malibu | Freeware (General) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `super-starfish` | Super Starfish | Freeware (Personal & Commercial Use Granted) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `tycho` | Tycho | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |
| `wide-road` | Wide Road | Letterlays Commercial License (Receipt PDF) | Yes | **No** | Commercial design grant with receipt PDF. Prohibits raw font file distribution or open-source repackaging. |
| `zillah-modern` | Zillah Modern | Freeware (General) | Yes | **No** | Author text grants commercial design use. File redistribution on public code repositories is ambiguous or requires author written confirmation. |
| `zt-nature` | ZT Nature | 1001Fonts Free For Commercial Use License (FFC) | Yes | **No** | Commercial design use permitted. However, Section 3 of FFC explicitly prohibits standalone font file redistribution, bundling, or re-hosting on GitHub/mirrors without written author permission. |

---

## 5. Restricted Fonts (Do NOT Redistribute / Purchase Required)

Total: **10 families**. These fonts have restrictive EULAs, evaluation demo limitations, or unspecified copyrights:

| ID | Family Name | License / Terms | Commercial | Redistribution | Action Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `antapani` | Antapani | Unspecified Copyright (copyright © 2020 by monocotype. all rights reserved.) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |
| `bjorn` | Bjorn | Unspecified Copyright (typeface © (tugcu co). 2016. all rights reserved typeface © ) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |
| `garute` | Garute | Unspecified Copyright (garute© (mjtype). 2023. all rights reserved garute© (mjtype)) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |
| `lokro` | Lokro | Unspecified Copyright (copyright © 2021 by denny-0980. copyright © 2021 by denny-09) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |
| `neris` | Neris | Eimantas Paškonis EULA (Commercial OK, No File Sharing) | No / Demo | **No** | RESTRICTED FOR REDISTRIBUTION: Commercial design use granted, but license explicitly forbids uploading to public file-sharing sites or redistributing font binaries. |
| `quango` | Quango | NimaVisual End User License Agreement | No / Demo | **No** | RESTRICTED: License text explicitly states 'strictly no redistribution, selling, or file sharing'. Commercial design usage requires commercial license purchase. |
| `the-bold-font` | THE BOLD FONT | Unspecified Copyright (copyright (c) 2015 by sven pels. all rights reserved. copyri) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |
| `timeburner` | Timeburner | NimaVisual End User License Agreement | No / Demo | **No** | RESTRICTED: License text explicitly states 'strictly no redistribution, selling, or file sharing'. Commercial design usage requires commercial license purchase. |
| `warriot` | Warriot | Evaluation / Demo Cut (Commercial Purchase Required) | No / Demo | **No** | RESTRICTED: Personal use / demo cut only. Commercial usage and redistribution prohibited without purchasing commercial license from author. |
| `zt-shago` | Zt Shago | Unspecified Copyright (copyright © 2022 by zelow type. copyright © 2022 by zelow ty) | No / Demo | **No** | RESTRICTED: Contains standard copyright notice without explicit open-source or redistribution grant. Font files must not be published to public code repos. |

---

## 6. Unknown / Missing Documentation

Total: **3 families**. No license documents were found in source packages. Treat as all rights reserved until verified:

| ID | Family Name | Source Package | Recommendation |
| :--- | :--- | :--- | :--- |
| `society` | Society | `society` | Contact foundry or replace with verified open-source alternative. |
| `sweet-school` | Sweet School | `sweet-school` | Contact foundry or replace with verified open-source alternative. |
| `talero` | TALERO | `talero` | Contact foundry or replace with verified open-source alternative. |

---

## 7. Complete Font Tracking Inventory (All 103 Families)

| Font ID | Family Name | Category | Status | License | SPDX | Comm. | Redist. | Mod. | Verification Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `achtung-bravo` | Achtung Bravo | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `aclonica` | Aclonica | sans-serif | `verified` | Apache License 2.0 | `Apache-2.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `aix-milan` | Aix Milan | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `al-saflers` | Al Saflers | display | `needs-review` | Freeware (Personal & Comm | `-` | Yes | No | No | 2026-09-29 |
| `alphakind` | Alphakind | handwriting | `needs-review` | Freeware (Personal & Comm | `-` | Yes | No | No | 2026-09-29 |
| `ampunsuhu` | Ampunsuhu | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `anak-bijak` | Anak Bijak | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `anak-gedong` | Anak Gedong | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `antapani` | Antapani | display | `restricted` | Unspecified Copyright (co | `-` | No | No | No | 2026-09-29 |
| `arnprior` | Arnprior | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `bakula` | Bakula | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `balhattan` | Balhattan | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `bedizen` | Bedizen | display | `needs-review` | Freeware (Author Freeware | `-` | Yes | No | No | 2026-09-29 |
| `biocats` | Biocats | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `bjorn` | Bjorn | display | `restricted` | Unspecified Copyright (ty | `-` | No | No | No | 2026-09-29 |
| `bm-dohyeon` | BM DoHyeon | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `butflow` | Butflow | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `castle-chunk` | Castle Chunk | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `chillax` | Chillax | sans-serif | `verified` | ITF Free Font License (Fo | `-` | Yes | **Yes** | Yes | 2026-09-29 |
| `courbe-sans` | Courbe Sans | sans-serif | `needs-review` | Courbe Sans Free Standard | `-` | Yes | No | No | 2026-09-29 |
| `credit-river` | Credit River | sans-serif | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `credit-valley` | Credit Valley | serif | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `crucial` | Crucial | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `cuyabra` | Cuyabra | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `delta-block` | Delta Block | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `die-nasty` | Die Nasty | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `dosis` | Dosis | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `enter-sansman` | Enter Sansman | sans-serif | `needs-review` | Freeware (General) | `-` | Yes | No | No | 2026-09-29 |
| `free-cheese` | Free Cheese | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `garute` | Garute | sans-serif | `restricted` | Unspecified Copyright (ga | `-` | No | No | No | 2026-09-29 |
| `general-sans` | General Sans | sans-serif | `verified` | ITF Free Font License (Fo | `-` | Yes | **Yes** | Yes | 2026-09-29 |
| `guanine` | Guanine | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `gudea` | Gudea | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `halo-dek` | Halo Dek | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `heming` | Heming | sans-serif | `needs-review` | Freeware (Commercial Use  | `-` | Yes | No | No | 2026-09-29 |
| `hijo` | HiJO | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `hirolliv` | HiRolliv | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `holstein` | Holstein | display | `verified` | Public Domain Dedication | `-` | Yes | **Yes** | Yes | 2026-09-29 |
| `imuch` | iMuch | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `inflammable-age` | Inflammable Age | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `ithaca` | Ithaca | serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `jazzy-huitbits` | Jazzy HuitBits | monospace | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `jazzyrabbit` | JazzyRabbit | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `jazzyrabbit-remake` | JazzyRabbit Remake | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `jogrunge` | JOGRUNGE | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `jumping-chick` | Jumping Chick | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `kalima` | KALIMA | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `kaph` | Kaph | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `kastore` | Kastore | display | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `kineks-round` | Kineks Round | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `kingsbridge` | Kingsbridge | sans-serif | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `lokro` | Lokro | sans-serif | `restricted` | Unspecified Copyright (co | `-` | No | No | No | 2026-09-29 |
| `lumierepolis` | Lumierepolis | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `marker2` | Marker2 | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `martius` | Martius | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `modestic-sans` | Modestic Sans | sans-serif | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `mousou-record-g` | Mousou Record__G | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `neris` | Neris | sans-serif | `restricted` | Eimantas Paškonis EULA (C | `-` | Yes | No | No | 2026-09-29 |
| `neuropol` | Neuropol | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `newestshape` | NewestShape | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `newshape` | NewShape | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `oligopoly` | Oligopoly | sans-serif | `needs-review` | Freeware (Commercial Use  | `-` | Yes | No | No | 2026-09-29 |
| `opsilon` | Opsilon | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `paint-marker` | Paint Marker | display | `needs-review` | Letterlays Commercial Lic | `-` | Yes | No | No | 2026-09-29 |
| `pingsan` | Pingsan | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `progo` | PROGO | display | `needs-review` | Freeware (Free Commercial | `-` | Yes | No | No | 2026-09-29 |
| `quango` | Quango | display | `restricted` | NimaVisual End User Licen | `-` | No | No | No | 2026-09-29 |
| `raster-forge` | Raster Forge | monospace | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `reckoner` | Reckoner | sans-serif | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `relish-gargler` | Relish Gargler | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `ruthless-sketch` | Ruthless Sketch | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `sagewold` | Sagewold | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `serati` | Serati | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `simply-sans` | Simply Sans | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `society` | Society | display | `unknown` | Unknown / Missing License | `-` | No | No | No | 2026-09-29 |
| `spicy-sale` | Spicy Sale | handwriting | `needs-review` | Creative Fabrica Commerci | `-` | Yes | No | No | 2026-09-29 |
| `stampcraft` | Stampcraft | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `street-cred` | Street Cred | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `styllo` | Styllo | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `super-joyful` | Super Joyful | handwriting | `needs-review` | Freeware (General) | `-` | Yes | No | No | 2026-09-29 |
| `super-malibu` | Super Malibu | handwriting | `needs-review` | Freeware (General) | `-` | Yes | No | No | 2026-09-29 |
| `super-starfish` | Super Starfish | handwriting | `needs-review` | Freeware (Personal & Comm | `-` | Yes | No | No | 2026-09-29 |
| `sweet-school` | Sweet School | handwriting | `unknown` | Unknown / Missing License | `-` | No | No | No | 2026-09-29 |
| `talero` | TALERO | display | `unknown` | Unknown / Missing License | `-` | No | No | No | 2026-09-29 |
| `the-bold-font` | THE BOLD FONT | display | `restricted` | Unspecified Copyright (co | `-` | No | No | No | 2026-09-29 |
| `timeburner` | Timeburner | sans-serif | `restricted` | NimaVisual End User Licen | `-` | No | No | No | 2026-09-29 |
| `tycho` | Tycho | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `ubuntu` | Ubuntu | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `ubuntu-condensed` | Ubuntu Condensed | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `ubuntu-mono` | Ubuntu Mono | monospace | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `unispace` | Unispace | monospace | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `unsteady-oversteer` | Unsteady Oversteer | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `vaticanus` | Vaticanus | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `viga` | Viga | sans-serif | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `vincendo` | Vincendo | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `warriot` | Warriot | display | `restricted` | Evaluation / Demo Cut (Co | `-` | No | No | No | 2026-09-29 |
| `wide-road` | Wide Road | display | `needs-review` | Letterlays Commercial Lic | `-` | Yes | No | No | 2026-09-29 |
| `world-of-water` | World of Water | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `zero-cool` | Zero Cool | display | `verified` | SIL Open Font License 1.1 | `OFL-1.1` | Yes | **Yes** | Yes | 2026-09-29 |
| `zillah-modern` | Zillah Modern | display | `needs-review` | Freeware (General) | `-` | Yes | No | No | 2026-09-29 |
| `zorque` | Zorque | display | `verified` | Creative Commons Zero 1.0 | `CC0-1.0` | Yes | **Yes** | Yes | 2026-09-29 |
| `zt-nature` | ZT Nature | display | `needs-review` | 1001Fonts Free For Commer | `-` | Yes | No | No | 2026-09-29 |
| `zt-shago` | Zt Shago | display | `restricted` | Unspecified Copyright (co | `-` | No | No | No | 2026-09-29 |
