# Font Intelligence: Incremental Font Ingestion & Catalog Audit

> **Audit Date**: 2026-09-29  
> **Total Source Packages Scanned**: 386 (285 new packages ingested)  
> **Total Font Binaries Processed**: 1052  
> **Total Typographic Families Mapped**: 413  

---

## 1. Executive Summary & Ingestion Metrics

| Ingestion Metric | Baseline V1 | Incremental Addition | Current Total | Notes |
| :--- | :-: | :-: | :-: | :--- |
| **Source Packages** | 101 | +285 | **386** | All packages in `All fonts/` preserved without renaming |
| **Font Binaries Processed** | 475 | +577 | **1052** | TrueType, OpenType, WOFF, WOFF2 |
| **Typographic Families** | 103 | +310 | **413** | Baseline 103 families strictly preserved |
| **Variable Font Families** | 6 | +-2 | **4** | Verified `fvar` registered axes |
| **Italic / Oblique Styles** | 29 | +55 | **84** | True companion italics |
| **Public-Asset Families** | 57 | — | **107** | Verified permissive open-source redistribution |
| **Catalog-Only Families** | 33 | — | **69** | Retained for AI styling intelligence |
| **Restricted / Demo Cuts** | 4 | — | **2** | Demo / personal use only; export blocked |
| **Unknown Provenance** | 9 | — | **235** | Unverified foundry EULAs |

---

## 2. Duplicate Detection (SHA-256 Cryptographic Audit)

Found **17 duplicate binary groups** (34 identical files) across packages.
Identical files have been mapped without data corruption or redundant catalog indexing.

| SHA-256 Hash Prefix | File Count | Identified File Instances |
| :--- | :-: | :--- |
| `34a4f80ffd26...` | 2 | `All fonts/Chillax_Complete/Chillax_Complete/Fonts/TTF/Chillax-Variable.ttf`<br>`All fonts/Chillax_Complete/Chillax_Complete/Fonts/WEB/fonts/Chillax-Variable.ttf` |
| `4b2539d9ed33...` | 2 | `All fonts/GeneralSans_Complete/GeneralSans_Complete/Fonts/TTF/GeneralSans-Variable.ttf`<br>`All fonts/GeneralSans_Complete/GeneralSans_Complete/Fonts/WEB/fonts/GeneralSans-Variable.ttf` |
| `4aa0c20dbb59...` | 2 | `All fonts/GeneralSans_Complete/GeneralSans_Complete/Fonts/TTF/GeneralSans-VariableItalic.ttf`<br>`All fonts/GeneralSans_Complete/GeneralSans_Complete/Fonts/WEB/fonts/GeneralSans-VariableItalic.ttf` |
| `71ceb1751dc5...` | 2 | `All fonts/anak-bijak/Anak Bijak.otf`<br>`All fonts/anak-bijak-font/AnakBijak-R9aZW.otf` |
| `da99f0d0e564...` | 2 | `All fonts/anak-bijak/Anak Bijak.ttf`<br>`All fonts/anak-bijak-font/AnakBijak-BLKwx.ttf` |
| `9f37755d4e7e...` | 2 | `All fonts/bakula/Bakula-OTF.otf`<br>`All fonts/bakula-font/BakulaRegular-PVwMP.otf` |
| `961c3aebbf37...` | 2 | `All fonts/bakula/Bakula-TTF.ttf`<br>`All fonts/bakula-font/BakulaRegular-LVMBy.ttf` |
| `00933cf15579...` | 2 | `All fonts/ithaca/Ithaca.ttf`<br>`All fonts/ithaca-font/Ithaca-LVB75.ttf` |
| `55afe260dd59...` | 2 | `All fonts/martius/Martius-Italic.otf`<br>`All fonts/martius-font/MartiusItalic-PVA4E.ttf` |
| `5fb2cc843885...` | 2 | `All fonts/martius/Martius-Regular.otf`<br>`All fonts/martius-font/Martius-LV9L4.ttf` |
| `67f0bdb3490a...` | 2 | `All fonts/opsilon/Opsilon-Italic.ttf`<br>`All fonts/opsilon-font/OpsilonItalic-3lm9p.ttf` |
| `93ce3c2c66ec...` | 2 | `All fonts/opsilon/Opsilon-Regular.ttf`<br>`All fonts/opsilon-font/Opsilon-xRj8m.ttf` |
| `7b7026730e15...` | 2 | `All fonts/raster-forge/RasterForge.ttf`<br>`All fonts/raster-forge-font/RasterForgeRegular-JpBgm.ttf` |
| `fe8749fe96b4...` | 2 | `All fonts/society/Society-Regular.otf`<br>`All fonts/society/Society-Regular.ttf` |
| `32c23dda462d...` | 2 | `All fonts/sweet-school/SweetSchool-Regular.otf`<br>`All fonts/sweet-school/SweetSchool-Regular.ttf` |
| `99bbabffb331...` | 2 | `All fonts/timeburner/timeburnerbold.ttf`<br>`All fonts/timeburner-font/TimeburnerBold-peGR.ttf` |
| `1c227248b019...` | 2 | `All fonts/timeburner/timeburnernormal.ttf`<br>`All fonts/timeburner-font/Timeburner-xJB8.ttf` |

---

## 3. Script & Language Coverage (Zero Tofu Audit)

- **Latin Coverage**: 413 families (100% of collection)
- **Cyrillic Coverage**: 46 families verified with OpenType `cmap` Cyrillic glyphs
- **Greek Coverage**: 28 families verified with Greek glyphs
- **Arabic Coverage**: 0 families
- **Bangla Coverage**: 0 families
- **Hangul Coverage**: 2 families
- **Devanagari Coverage**: 1 families

> **Zero Tofu Policy Enforcement**: If a language script (e.g. Bangla) has 0 verified catalog families, the engine strictly reports `LOCAL CATALOG: 0 VERIFIED FONTS` and injects verified external open-source companions (`Hind Siliguri`, `Noto Sans Bengali`).

---

## 4. Preservation of Curated Typography Intelligence

All 103 baseline font families retain their calibrated categories, style tags, typography roles, and readability ratings without alteration.
Newly ingested families have been classified using controlled vocabulary categories, styles, and initial readability matrices based on their technical classifications.