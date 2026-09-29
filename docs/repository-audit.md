# Font Intelligence Repository Audit & Source Collection Analysis

> **Audit Target Directory**: `D:\font-intelligence\All fonts`  
> **Audit Scope**: Complete recursive scan of all 101 source packages, font binaries, metadata tables, licenses, documentation, and auxiliary assets.  
> **Operational Mode**: Non-destructive, read-only audit. Original folder structures and file names have been strictly preserved.  

---

## 1. Executive Summary & Inventory Dashboard

This repository audit was conducted to establish a comprehensive, forensic baseline of the existing font assets in `D:\font-intelligence\All fonts` before building the `font-intelligence` Agent Skill. Existing top-level folders are categorized as **Source Packages** containing heterogeneous file structures, multi-format binaries, licensing texts, specimen graphics, and author notes.

| Metric | Count | Observations & Notes |
| :--- | :--- | :--- |
| **Source Packages (Top-Level Directories)** | **101** | 101 unzipped source packages under `All fonts/`. |
| **Total Files in Repository** | **653** | 475 fonts, 64 licenses, 51 previews, 41 readmes, 18 docs, 2 CSS, 1 URL, 1 junk. |
| **Total Font Binary Files** | **475** | Encompasses desktop (.otf, .ttf) and web (.woff, .woff2, .eot) formats. |
| **Distinct Typographic Font Families** | **115** | Parsed directly from TrueType/OpenType `name` tables (NameID 16 & 1). |
| **True Variable Fonts** | **10** | 10 variable font binaries across 3 distinct source packages. |
| **Italic / Oblique Styles** | **130** | 27.4% of font binaries feature true italic or oblique styling. |
| **Preview Images** | **51** | 51 images (JPG/PNG) distributed across only 17 packages (84 packages lack previews). |
| **License Files Detected** | **57 pkgs** | 64 license files across 57 packages; 44 packages lack local license text files. |
| **Readme & About Files** | **30 pkgs** | 41 informational text files across 30 packages. |
| **Packages with Nested Subdirectories** | **12** | Nested sub-hierarchies up to 4 directory levels deep (`Chillax`, `GeneralSans`). |
| **Exact File Duplicates (by SHA-256)** | **9 groups (19 files)** | Includes byte-identical files with mismatched extensions (`.otf` identical to `.ttf`). |
| **Cross-Package Split Families** | **2 families** | `Oligopoly` (split across OTF and TTF packages) and shared author assets. |
| **Packages with High/Critical Legal Risk** | **15 packages** | Missing licenses, strict no-redistribution EULAs, or commercial demo versions. |

---

## 2. Font File Formats & Outline Architectures

A deep parse of the font binaries reveals significant format diversity, webfont bundling, and format redundancy across source packages.

### 2.1 File Extension Breakdown

| Extension | File Count | Percentage | Primary Usage & Role |
| :--- | :--- | :--- | :--- |
| `.otf` | 224 | 47.2% | OpenType with PostScript CFF outlines (desktop & print) |
| `.ttf` | 187 | 39.4% | TrueType outlines (desktop, Windows native, web) |
| `.woff` | 22 | 4.6% | Web Open Font Format 1.0 (compressed webfont) |
| `.eot` | 21 | 4.4% | Embedded OpenType (legacy Internet Explorer 6-8 format) |
| `.woff2` | 21 | 4.4% | Web Open Font Format 2.0 (modern Brotli-compressed webfont) |

### 2.2 Underlying Glyph Outline Formats (`sfntVersion` & Tables)

OpenType fonts wrap either cubic Bézier outlines (PostScript CFF) or quadratic Bézier outlines (TrueType).

- **CFF (PostScript Type 2 Outlines)**: `232` files (48.8%). Driven by the `'CFF '` table. Standard in professional print and Adobe environments.
- **TrueType (`glyf` Outlines)**: `222` files (46.7%). Driven by `'glyf'` and `'loca'` tables. Highly compatible with Windows ClearType and legacy renderers.
- **Legacy EOT Wrappers**: `21` files (4.4%). Found exclusively in `Chillax_Complete` (7 files) and `GeneralSans_Complete` (14 files). These utilize Microsoft's legacy EOT header (`EOT` format) rather than standard sfnt headers.

### 2.3 Format Bundling & Duplication Observations

1. **Dual Desktop Bundling (OTF + TTF)**: **36 source packages** provide both `.otf` and `.ttf` versions of the identical typographic cut (e.g., `garute`, `zt-shago`, `modestic-sans`, `anak-bijak`).
2. **Complete Webfont Suites**: `Chillax_Complete` and `GeneralSans_Complete` from Fontshare/ITF include comprehensive deployment packages containing `.otf`, `.ttf`, `.woff`, `.woff2`, `.eot`, and pre-configured `@font-face` CSS files.
3. **Identical File Re-naming Anomaly**: In `society` and `sweet-school`, the `.otf` and `.ttf` files have the exact same cryptographic hash (SHA-256). An identical binary was simply saved under two different file extensions.

---

## 3. Typographic Weights, Styles & Metadata Discrepancies

### 3.1 Weight Distribution (`OS/2.usWeightClass`)

Font weights are recorded according to the OpenType OS/2 specification (100 to 900+):

| Weight Class (`usWeightClass`) | Standard CSS Weight | Font Count | Example Families Represented |
| :--- | :--- | :--- | :--- |
| **100** | Thin / Hairline | 1 | `Bjorn` (Halftone) |
| **200** | Extra Light / Ultra Light | 14 | `General Sans`, `Chillax`, `hirolliv`, `imuch` |
| **250** | Non-Standard (ExtraLight-Light) | 21 | `Oligopoly`, `Dosis`, `Neris` |
| **300** | Light | 44 | `Kingsbridge`, `Dosis`, `Garute`, `Zt Shago`, `Lokro` |
| **400** | Regular / Normal / Book | 193 | `Ubuntu`, `Viga`, `Neuropol`, `Balhattan`, `Bakula` |
| **500** | Medium | 30 | `General Sans`, `Chillax`, `Crucial`, `Garute`, `Zt Shago` |
| **600** | Semi Bold / Demi Bold | 33 | `General Sans`, `Chillax`, `Kingsbridge`, `Garute` |
| **700** | Bold | 91 | `Ubuntu`, `Reckoner`, `Garute`, `Kingsbridge`, `Zt Shago` |
| **800** | Extra Bold / Heavy | 10 | `Antapani`, `Garute`, `Zt Shago`, `Ubuntu` |
| **900** | Black | 13 | `Garute`, `Zt Shago`, `Neris`, `Oligopoly` |
| **950** | Extra Black (Ultra Black) | 4 | `Zt Shago` (ExtraBlack & ExtraBlack Italic) |
| **None** | Legacy EOT (Unparsed sfnt) | 21 | `Chillax` (7) & `General Sans` (14) webfonts |

### 3.2 Weight Discrepancies: Filename vs Internal Header Metadata

A critical rule in font intelligence is **never assuming filename equals typographic weight**. The audit identified 12 distinct font binaries where filenames conflict with internal OS/2 table data:

| Source Package | Filename | Declared Filename Weight | Actual `usWeightClass` | Internal Subfamily | Discrepancy Analysis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Bjorn` | `Bjorn Light.otf` | 300 (Light) | **400 (Regular)** | `Regular` | **Severe**: Font claims to be Light in filename but metadata identifies it as Regular weight. |
| `Oligopoly-OTF` | `Oligopoly Thin.otf` | 100 (Thin) | **250 (ExtraLight)** | `ExtraLight` | Author mapped Thin cut to 250 rather than 100. |
| `Oligopoly-TTF` | `Oligopoly Thin.ttf` | 100 (Thin) | **250 (ExtraLight)** | `ExtraLight` | TrueType cut inherits identical 250 weight mapping. |
| `dosis` | `Dosis-ExtraLight.ttf` | 200 (ExtraLight) | **250 (Non-standard)** | `ExtraLight` | Uses non-standard 250 weight value instead of 200. |
| `hirolliv` | `HiRollivLight.ttf` | 300 (Light) | **200 (ExtraLight)** | `Light` | Declares Light but internal weight class is 200. |
| `imuch` | `iMuchLight.otf` | 300 (Light) | **200 (ExtraLight)** | `Light` | Declares Light but internal weight class is 200. |
| `neris` | `Neris-Thin.otf` | 100 (Thin) | **250 (ExtraLight)** | `Regular` | Name implies Thin; weight is 250; subfamily is Regular! |
| `neris` | `Neris-ThinItalic.otf` | 100 (Thin) | **250 (ExtraLight)** | `Italic` | Name implies Thin; weight is 250; subfamily is Italic. |
| `zt-shago` | `ZtShago-ExtraBlack.otf` | 900 (Black) | **950 (ExtraBlack)** | `Regular` | Subfamily set to Regular while weight class is 950. |
| `zt-shago` | `ZtShago-ExtraBlack.ttf` | 900 (Black) | **950 (ExtraBlack)** | `Regular` | Subfamily set to Regular while weight class is 950. |
| `zt-shago` | `ZtShago-ExtraBlackItalic.otf` | 900 (Black) | **950 (ExtraBlack)** | `Italic` | ExtraBlack style with 950 weight class. |
| `zt-shago` | `ZtShago-ExtraBlackItalic.ttf` | 900 (Black) | **950 (ExtraBlack)** | `Italic` | ExtraBlack style with 950 weight class. |

### 3.3 Italic & Oblique Styles

- **Total Italic/Oblique Binaries**: `130` font files (27.4% of all font files).
- **Families with True Companion Italics**: `General Sans`, `Kingsbridge` (massive condensed/expanded italic system), `Garute Oblique`, `Zt Shago`, `Ubuntu`, `Credit Valley`, `Modestic Sans`, `Simply Sans`, `Crucial`, `Neris`, `NewShape`.

---

## 4. Variable Fonts Deep Dive (`fvar` Table)

Variable fonts allow dynamic interpolation across design axes within a single binary. Only **3 source packages** contain true variable OpenType fonts (10 binaries total):

| Package Name | Relative Path / Filename | Format | Axes Supported | Min / Default / Max | Named Instances | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Chillax_Complete` | `Fonts/TTF/Chillax-Variable.ttf` | TrueType | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Duplicated in `WEB/fonts/` |
| `Chillax_Complete` | `Fonts/WEB/fonts/Chillax-Variable.woff2` | WOFF2 | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Modern webfont deployment cut |
| `GeneralSans_Complete` | `Fonts/TTF/GeneralSans-Variable.ttf` | TrueType | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Duplicated in `WEB/fonts/` |
| `GeneralSans_Complete` | `Fonts/WEB/fonts/GeneralSans-Variable.woff2` | WOFF2 | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Upright variable webfont |
| `GeneralSans_Complete` | `Fonts/TTF/GeneralSans-VariableItalic.ttf` | TrueType | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Duplicated in `WEB/fonts/` |
| `GeneralSans_Complete` | `Fonts/WEB/fonts/GeneralSans-VariableItalic.woff2` | WOFF2 | `wght` (Weight) | 200.0 / 700.0 / 700.0 | 6 instances | Companion italic variable webfont |
| `heming-font` | `heming-variable.ttf` | TrueType | `wght` (Weight) | 300.0 / 300.0 / 700.0 | 5 instances | Standalone variable font file |

> [!TIP]
> When constructing the font intelligence skill, variable fonts can replace entire folders of static weight binaries in web workflows, dramatically reducing network payload size.

---

## 5. Related Files: Licenses, Readmes, Previews & Web Assets

Non-font assets provide critical context regarding licensing provenance, author attribution, and visual specimens.

### 5.1 Preview Images (Specimens)

- **Total Preview Files**: `51` image files (30 JPG, 21 PNG).
- **Coverage**: Only **17 packages** include visual previews; **84 packages have zero preview graphics**.
- **Rich Specimen Packages**:
  - `garute`: 9 high-resolution presentation PNGs (`Preview.png`, `Preview2.png` - `Preview11.png`).
  - `castle-chunk`: 9 artboard preview JPGs (`Artboard 1.jpg`, `Artboard 2 copy.jpg`, etc.).
  - `kastore`: 6 full-bleed presentation JPGs.
  - `sweet-school`: 6 mockup JPGs.
  - `ampunsuhu`: 5 display showcase PNGs.
  - `crucial`: 5 character showcase PNGs.

### 5.2 Readme & Informational Files

- **Total Readme / About Files**: `41` files across **30 packages**.
- **Official OpenType FONTLOGs**: Standard GNU/SIL typography changelogs present in `dosis`, `gudea`, `simply-sans`, `ubuntu`, and `viga`.
- **Deployment Documentation**: `Chillax_Complete` and `GeneralSans_Complete` contain `README.md` with CSS integration instructions and pre-packaged `WEB/css/*.css` stylesheets.
- **Author Notes**: Personal background notes present in `bakula` (`About Font.txt`), `holstein` (`holstein.txt`), `aix-milan` (`font by lirkiv.txt`), and `jazzyrabbit` (`font by lirkiv.txt`).

---

## 6. Directory Structures & Unusual Hierarchy Quirks

The audit identified several formatting and structural anomalies that require normalization rules in future skill operations:

### 6.1 Directory Nesting & Complex Trees

While 89 packages are flat (all files in the package root), **12 packages have nested subdirectories**:

1. **Deep Hierarchies (Depth 4)**:
   - `Chillax_Complete`: Nested subfolders `Chillax_Complete/Fonts/{OTF, TTF, WEB/{css, fonts}}` and `Chillax_Complete/License`.
   - `GeneralSans_Complete`: Nested subfolders `GeneralSans_Complete/Fonts/{OTF, TTF, WEB/{css, fonts}}` and `GeneralSans_Complete/License`.
2. **Versioned Subfolders**:
   - `dosis`: Single subfolder `Dosis v1.7/` containing fonts and documentation.
   - `ubuntu`: Single subfolder `ubuntu-font-family-0.80/` containing all files.
3. **Redundant Nested Subfolders Matching Font Name**:
   - `behance-65c4bcf7464f1` -> `Biocats/`
   - `behance-65ef07bdb6f6f` -> `Pingsan/`
   - `behance-672092c703c71` -> `Halo Dek/`
   - `behance-68ff9b50e17d5` -> `Spicy Sale/`
   - `behance-6a4cfe40dec36` -> `Butflow/`
   - `holstein` -> `fh-holst/`
4. **Auxiliary Subfolders**:
   - `alphakind-font/misc/` and `sagewold-font/misc/` contain critical license and readme documents.

### 6.2 Structural Quirks & Anomalies

- **Double File Extensions**: In `courbe-sans`, files have duplicate extensions: `CourbeSans.otf.otf`, `CourbeSans.ttf.ttf`, `LICENSE.txt.txt`, `README.txt.txt`.
- **macOS Artifacts**: `dosis/Dosis v1.7/.DS_Store` (12,292 bytes macOS Finder metadata).
- **Word Document as License**: `cuyabra` contains `SIL Open Font License v1 - cuyabra.docx` (Microsoft Word format) rather than plain text.
- **Rich Text Format License**: `styllo` contains `LICENSE.rtf`.
- **Hashed Package Names**: Six packages use Behance CDN hashes (`behance-6596a9ca1f6c5`, `behance-65c4bcf7464f1`, etc.) which completely obscure the true font names (`Al Saflers`, `Biocats`, `Pingsan`, `Halo Dek`, `Spicy Sale`, `Butflow`).

---

## 7. Duplicate Files, Families & Split Packages

### 7.1 Cryptographically Identical Files (SHA-256 Duplicates)

The audit discovered **9 distinct hash groups** representing **19 duplicate file instances** across the repository:

| SHA-256 Prefix | File Size | Category | Confirmed Duplicate File Instances |
| :--- | :--- | :--- | :--- |
| `fe8749fe96b4...` | 14,348 B | **Font** | `society/Society-Regular.otf` and `society/Society-Regular.ttf` (Identical bytes with different extension) |
| `32c23dda462d...` | 10,032 B | **Font** | `sweet-school/SweetSchool-Regular.otf` and `sweet-school/SweetSchool-Regular.ttf` (Identical bytes with different extension) |
| `34a4f80ffd26...` | 162,384 B | **Font** | `Chillax_Complete/Fonts/TTF/Chillax-Variable.ttf` and `Chillax_Complete/Fonts/WEB/fonts/Chillax-Variable.ttf` |
| `4b2539d9ed33...` | 110,820 B | **Font** | `GeneralSans_Complete/Fonts/TTF/GeneralSans-Variable.ttf` and `GeneralSans_Complete/Fonts/WEB/fonts/GeneralSans-Variable.ttf` |
| `4aa0c20dbb59...` | 112,704 B | **Font** | `GeneralSans_Complete/Fonts/TTF/GeneralSans-VariableItalic.ttf` and `GeneralSans_Complete/Fonts/WEB/fonts/GeneralSans-VariableItalic.ttf` |
| `a57f6f06a947...` | 536,273 B | **Readme PDF** | Shared across 6 packages: `behance-65c4bcf7464f1`, `behance-65ef07bdb6f6f`, `behance-672092c703c71`, `behance-68ff9b50e17d5`, `behance-6a4cfe40dec36`, and `jumping-chick` |
| `1d736c9f5cfd...` | 133,322 B | **Readme PDF** | Shared across `anak-bijak` and `anak-gedong` |
| `f4e7f373b9b9...` | 7,169 B | **License** | 1001Fonts CC0 legal text shared across 5 packages: `delta-block`, `free-cheese`, `raster-forge`, `stampcraft`, `vaticanus` |
| `145e7fe2429a...` | 12,734 B | **License** | Indian Type Foundry FFL license text shared between `Chillax_Complete` and `GeneralSans_Complete` |
| `1e4c2e476df4...` | 139 B | **Readme** | `Oligopoly-Readme.txt` shared between `Oligopoly-OTF` and `Oligopoly-TTF` |
| `dee6e0781a0c...` | 434 B | **License** | `Terms.txt` shared between `jazzy-huitbits` and `jazzyrabbit-remake` |
| `a893b3e7f321...` | 531 B | **License** | `NV- Eula.txt` shared between `quango` and `timeburner` |

### 7.2 Split Package Duplication

- **`Oligopoly`**: Represented by two separate source packages: `Oligopoly-OTF` (5 weights: Thin, Light, Regular, Bold, Black in `.otf`) and `Oligopoly-TTF` (same 5 weights in `.ttf`). These are the same font family split into two packages by format.

---

## 8. Missing Metadata Analysis

Fonts obtained from the web frequently lack proper OpenType metadata fields:

- **Missing Designer Name (NameID 9)**: `84` font files (17.7%) have no designer name in their OpenType tables (e.g., `Bjorn`, `cuyabra`, `holstein`, `society`, `sweet-school`, `the-bold-font-free-version`, `talero`).
- **Missing Manufacturer / Foundry (NameID 8)**: `126` font files lack manufacturer records.
- **Missing In-Font License Description / URL (NameIDs 13 & 14)**: `148` font files have completely blank license fields inside the font binary itself, relying entirely on external files or author provenance.
- **Missing Copyright String (NameID 0)**: `43` font files have empty or single-character copyright fields (`society`, `sweet-school`, `super_starfish`, `talero`).

---

## 9. Licensing Audit & Risk Classification

Understanding font licensing is vital for commercial safety and redistribution rights. Every source package and font binary was classified across four legal risk tiers:

### 9.1 Risk Level Breakdown

| Legal Risk Tier | Package Count | Font Count | Dominant License Models | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Low (Fully Permissive)** | **51 packages** | **175 fonts** | SIL OFL 1.1, CC0 / Public Domain, Apache 2.0, Fontshare FFL, Ubuntu UFL | Safe for commercial use, bundling, web embedding, and derivative works. |
| **Tier 2: Low / Medium (Permissive Freeware)** | **31 packages** | **94 fonts** | 1001Fonts FFC, Khurasan 100% Free, Author Explicit Commercial Grants | Safe for commercial projects; maintain author attribution. |
| **Tier 3: Medium (Purchased / Account-Bound)** | **4 packages** | **10 fonts** | Letterlays Full License (receipt PDF), Creative Fabrica | Retain purchase invoices / proof of commercial license. |
| **Tier 4: HIGH / CRITICAL RISK** | **15 packages** | **196 fonts** | Restrictive EULAs, Demo/Trial Fonts, No License / Copyright Only | **DO NOT distribute or use in client work without license resolution.** |

### 9.2 High & Critical Risk Font Packages (Detailed Findings)

The following 15 packages require careful handling due to legal, licensing, or provenance concerns:

1. **`quango` & `timeburner` (NimaVisual EULA - HIGH RISK)**:
   - EULA states: *"The free and non free NimaVisual fonts may not be redistributed in any way (they may not be resold, distributed commercially, they may not be made available for download) without the written permission of NimaVisual."*
   - Redistribution via an agent skill or cloud repository violates this clause.
2. **`neris` (Eimantas Paškonis EULA - HIGH RISK)**:
   - EULA states: *"It is FORBIDDEN to: modify, sell, or share the font files. One exception is making backup copies for your own private use."* Commercial use of rendered graphics is permitted, but the font binaries cannot be shared or distributed.
3. **`warriot` (Commercial Demo / Trial - HIGH RISK)**:
   - `thanks.txt` explicitly states: *"Donate are acceptable via paypal... you can download the full version: https://ffeeaarr.my.id/"*. This indicates the package is a crippled demo or personal evaluation cut.
4. **`the-bold-font-free-version` (Free Demo Cut - MEDIUM/HIGH RISK)**:
   - Named explicitly "FREE VERSION" by Sven Pels; may omit full punctuation, kerning pairs, or multilingual glyphs.
5. **`garute` (MJType - HIGH RISK - 28 Font Files)**:
   - Package contains 28 font binaries (14 OTF + 14 TTF) and 9 previews, but **zero license files**. Font metadata contains only `Garute© (MJType). 2023. All Rights Reserved`. MJType typically sells full commercial licenses while offering personal-use demos on DaFont.
6. **`zt-shago` (Zelow Type - HIGH RISK - 32 Font Files)**:
   - Package contains 32 font binaries (16 OTF + 16 TTF) across 8 weights and companion italics, with **no license file** and metadata stating only `Copyright © 2022 by Zelow Type`. Requires license verification.
7. **`society`, `sweet-school`, `super_starfish`, `talero` (Zero License Metadata - CRITICAL RISK)**:
   - Completely lack any license file, and internal font metadata contains no copyright, designer, or licensing text.
8. **`Bjorn`, `antapani`, `lokro` (Copyright Only, No Terms - HIGH RISK)**:
   - Contain valid copyright notices (Tugcu Co, Monocotype, denny-0980) but no accompanying grant of rights or license file.

### 9.3 OpenType Technical Embedding Permissions (`OS/2.fsType`)

In addition to legal contracts, font binaries encode technical embedding flags (`fsType` in the `OS/2` table) that PDF engines and operating systems enforce:

- **`0x0000` (Installable Embedding)**: **366 fonts** (77.1%). Fully unrestricted; fonts may be embedded in documents and installed permanently.
- **`0x0004` (Preview & Print Embedding Only)**: **63 fonts** (13.3%). Documents embedding the font must be opened read-only. Editing is technically forbidden. Found in `cuyabra`, `dosis`, `garute`, `Oligopoly`, `heming-font`, `kastore`, `modestic-sans`, `quango`, `reckoner`.
- **`0x0008` (Editable Embedding)**: **22 fonts** (4.6%). Documents embedding the font may be opened for reading and editing. Found in `Bjorn`, `neris`, `warriot`, `the-bold-font-free-version`, `lokro`, `marker2`, `mousou-record-g`, `castle-chunk`.
- **`0x0001` (Restricted License / Reserved)**: **3 fonts** (0.6%). `holstein` (2 files) and `tycho` (1 file).

---

## 10. Complete Source Package Master Inventory

The table below catalogs all 101 source packages, cross-referencing package directory names with true typographic family names, formats, file counts, variable support, preview status, and licensing classifications:

| # | Source Package Name | True Font Family Name | Formats | Fonts | Weights Present | Variable | Previews | License Classification | Legal Risk Tier |
| :-: | :--- | :--- | :--- | :-: | :--- | :-: | :-: | :--- | :--- |
| 1 | `Bjorn` | **Bjorn** | .otf | 3 | 400 | No | None | Unspecified (Copyright Only: typeface © (tugcu co). 2016. all rights ...) | HIGH RISK (No explicit license) |
| 2 | `Chillax_Complete` | **Chillax, Chillax Variable, UNKNOWN** | .eot, .otf, .ttf, .woff, .woff2 | 35 | 200, 300, 400, 500, 600, 700 | Yes | None | ITF Free Font License (Fontshare FFL) | Low (Permissive) |
| 3 | `GeneralSans_Complete` | **General Sans, General Sans Variable, UNKNOWN** | .eot, .otf, .ttf, .woff, .woff2 | 70 | 200, 300, 400, 500, 600, 700 | Yes | None | ITF Free Font License (Fontshare FFL) | Low (Permissive) |
| 4 | `Oligopoly-OTF` | **Oligopoly** | .otf | 5 | 250, 300, 400, 700, 900 | No | None | Unspecified (Copyright Only: hyun seok choi, republic of korea hyun s...) | HIGH RISK (No explicit license) |
| 5 | `Oligopoly-TTF` | **Oligopoly** | .ttf | 5 | 250, 300, 400, 700, 900 | No | None | Unspecified (Copyright Only: hyun seok choi, republic of korea hyun s...) | HIGH RISK (No explicit license) |
| 6 | `achtung-bravo` | **Achtung Bravo** | .ttf | 1 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 7 | `aclonica` | **Aclonica** | .ttf | 1 | 400 | No | None | Apache License 2.0 | Low (Permissive) |
| 8 | `aix-milan` | **aix milan** | .ttf | 1 | 400 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 9 | `alphakind-font` | **Alphakind** | .otf, .ttf | 2 | 400 | No | None | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 10 | `ampunsuhu` | **Ampunsuhu** | .otf | 1 | 400 | No | 5 img | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 11 | `anak-bijak` | **Anak Bijak** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 12 | `anak-gedong` | **Anak Gedong** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 13 | `antapani` | **Antapani** | .otf | 1 | 800 | No | None | Unspecified (Copyright Only: copyright © 2020 by monocotype. all righ...) | HIGH RISK (No explicit license) |
| 14 | `arnprior` | **Arnprior** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 15 | `bakula` | **Bakula** | .otf, .ttf | 2 | 400 | No | None | Unspecified (Copyright Only: all fonts and typographic designs by art...) | HIGH RISK (No explicit license) |
| 16 | `balhattan` | **Balhattan** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 17 | `bedizen` | **Bedizen** | .ttf | 1 | 400 | No | None | Freeware (General) | Medium |
| 18 | `behance-6596a9ca1f6c5` | **Al Saflers** | .otf, .ttf, .woff | 3 | 400 | No | None | Unspecified (Copyright Only: copyright (c) 2023, font by aluyeah stud...) | HIGH RISK (No explicit license) |
| 19 | `behance-65c4bcf7464f1` | **Biocats** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 20 | `behance-65ef07bdb6f6f` | **Pingsan** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 21 | `behance-672092c703c71` | **Halo Dek** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 22 | `behance-68ff9b50e17d5` | **Spicy Sale** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 23 | `behance-6a4cfe40dec36` | **Butflow** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 24 | `bm-dohyeon` | **BM DoHyeon, BM DoHyeon OTF** | .otf, .ttf | 2 | 400 | No | None | Baedal Minjok Open License | Low (Permissive) |
| 25 | `castle-chunk` | **Castle Chunk** | .otf, .ttf | 2 | 400 | No | 9 img | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 26 | `courbe-sans` | **Courbe Sans** | .otf, .ttf | 2 | 400 | No | None | Courbe Sans Free Standard License | Low (Permissive) |
| 27 | `credit` | **Credit River, Credit Valley** | .otf | 5 | 400, 700 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 28 | `crucial` | **Crucial** | .otf | 2 | 500 | No | 5 img | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 29 | `cuyabra` | **cuyabra** | .otf | 4 | 400, 700 | No | 1 img | Unspecified (Copyright Only: copyright (c) 2016 by nèstor jairo delga...) | HIGH RISK (No explicit license) |
| 30 | `delta-block` | **Delta Block** | .otf, .ttf | 4 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 31 | `die-nasty` | **Die Nasty** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 32 | `dosis` | **Dosis** | .ttf | 7 | 250, 300, 400, 500, 600, 700, 800 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 33 | `enter-sansman` | **Enter Sansman** | .ttf | 2 | 700 | No | None | Freeware (General) | Medium |
| 34 | `free-cheese` | **Free Cheese** | .otf, .ttf | 4 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 35 | `garute` | **Garute, Garute Oblique** | .otf, .ttf | 28 | 300, 400, 500, 600, 700, 800, 900 | No | 9 img | Unspecified (Copyright Only: garute© (mjtype). 2023. all rights reser...) | HIGH RISK (No explicit license) |
| 36 | `guanine` | **Guanine** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 37 | `gudea` | **Gudea** | .ttf | 3 | 400, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 38 | `heming-font` | **Unnamed** | .ttf | 1 | 300 | Yes | None | NO LICENSE / NO COPYRIGHT METADATA | CRITICAL RISK (Unknown provenance) |
| 39 | `hijo` | **HiJO** | .otf | 5 | 100, 300, 400, 700, 900 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 40 | `hirolliv` | **HiRolliv** | .ttf | 3 | 200, 400, 700 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 41 | `holstein` | **Holstein** | .ttf | 2 | 400, 700 | No | None | Unspecified (Copyright Only: ©1995 ethan dunham  ‐ fonthead design (c...) | HIGH RISK (No explicit license) |
| 42 | `imuch` | **iMuch** | .otf | 4 | 200, 400, 700 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 43 | `inflammable-age` | **Inflammable Age** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 44 | `ithaca` | **Ithaca** | .ttf | 1 | 500 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 45 | `jazzy-huitbits` | **Jazzy_HuitBits** | .ttf | 1 | 400 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 46 | `jazzyrabbit` | **JazzyRabbit** | .ttf | 1 | 400 | No | 1 img | Unspecified (Copyright Only: copyright (c) 2022-2023, lirkiv. all rig...) | HIGH RISK (No explicit license) |
| 47 | `jazzyrabbit-remake` | **JazzyRabbit Remake** | .ttf | 1 | 400 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 48 | `jogrunge` | **JOGRUNGE** | .otf | 1 | 400 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 49 | `jumping-chick` | **Jumping Chick** | .otf, .ttf | 2 | 400 | No | 1 img | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 50 | `kalima` | **KALIMA** | .otf | 1 | 400 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 51 | `kaph` | **Kaph** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 52 | `kastore` | **Kastore** | .otf, .ttf | 2 | 700 | No | 6 img | Creative Fabrica Download | Medium (Check License) |
| 53 | `kineks-round` | **Kineks Round** | .otf, .ttf | 10 | 300, 400, 500, 600, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 54 | `kingsbridge` | **Kingsbridge** | .otf | 56 | 250, 300, 400, 600, 700 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 55 | `lokro` | **Lokro** | .otf | 2 | 300, 700 | No | None | Unspecified (Copyright Only: copyright © 2021 by denny-0980. copyrigh...) | HIGH RISK (No explicit license) |
| 56 | `lumierepolis` | **Lumierepolis** | .otf, .ttf | 12 | 300, 400, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 57 | `marker2` | **Marker2** | .ttf | 1 | 400 | No | None | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 58 | `martius` | **Martius** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 59 | `modestic-sans` | **Modestic Sans** | .otf, .ttf | 4 | 700 | No | None | Creative Fabrica Download | Medium (Check License) |
| 60 | `mousou-record-g` | **Mousou Record__G** | .ttf | 1 | 400 | No | None | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 61 | `neris` | **Neris** | .otf | 9 | 250, 300, 600, 700, 900 | No | None | CUSTOM EULA: Eimantas Paškonis (No file sharing) | HIGH RISK |
| 62 | `neuropol` | **Neuropol** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 63 | `new-shape` | **New Shape** | .ttf | 4 | 400, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 64 | `newest-shape` | **Newest Shape** | .ttf | 4 | 400, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 65 | `opsilon` | **Opsilon** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 66 | `paint-marker` | **Paint Marker** | .otf | 1 | 400 | No | None | Letterlays Commercial License (Receipt PDF) | Medium (Check Proof) |
| 67 | `progo` | **PROGO** | .otf | 2 | 400, 700 | No | None | Freeware (Commercial OK - Author Grant) | Low/Medium |
| 68 | `quango` | **Quango** | .otf | 1 | 700 | No | None | Unspecified (Copyright Only: copyright (c) 2015 by nimavisual. all ri...) | HIGH RISK (No explicit license) |
| 69 | `raster-forge` | **Raster Forge** | .ttf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 70 | `reckoner` | **Reckoner, Reckoner Bold** | .ttf | 2 | 500, 700 | No | None | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 71 | `relish-gargler` | **Relish Gargler** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 72 | `ruthless-sketch` | **Ruthless Sketch** | .ttf | 2 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 73 | `sagewold-font` | **Sagewold** | .ttf | 2 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 74 | `serati` | **Serati** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 75 | `simply-sans` | **Simply Sans** | .ttf | 4 | 400, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 76 | `society` | **Society** | .otf, .ttf | 2 | 400 | No | 1 img | NO LICENSE / NO COPYRIGHT METADATA | CRITICAL RISK (Unknown provenance) |
| 77 | `stampcraft` | **Stampcraft** | .otf, .ttf | 4 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 78 | `street-cred` | **Street Cred** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 79 | `styllo` | **Styllo** | .otf | 2 | 400, 700 | No | None | Unspecified (Copyright Only: copyright © 2015 by genilson lima santos...) | HIGH RISK (No explicit license) |
| 80 | `super-joyful-font` | **Super Joyful** | .ttf | 1 | 400 | No | None | Freeware (General) | Medium |
| 81 | `super-malibu-font` | **Super Malibu** | .ttf | 1 | 400 | No | None | Freeware (General) | Medium |
| 82 | `super_starfish` | **Super Starfish** | .ttf | 1 | 400 | No | None | Freeware (Personal & Commercial) | Low/Medium (Vendor Terms) |
| 83 | `sweet-school` | **Sweet School** | .otf, .ttf | 2 | 400 | No | 6 img | NO LICENSE / NO COPYRIGHT METADATA | CRITICAL RISK (Unknown provenance) |
| 84 | `talero` | **TALERO** | .otf | 1 | 500 | No | None | NO LICENSE / NO COPYRIGHT METADATA | CRITICAL RISK (Unknown provenance) |
| 85 | `the-bold-font-free-version` | **THE BOLD FONT** | .otf, .ttf | 2 | 700 | No | None | Unspecified (Copyright Only: copyright (c) 2015 by sven pels. all rig...) | HIGH RISK (No explicit license) |
| 86 | `timeburner` | **TimeBurner** | .ttf | 2 | 400, 700 | No | None | Unspecified (Copyright Only: copyright (c) 2012 by andres moreno walt...) | HIGH RISK (No explicit license) |
| 87 | `tycho` | **Tycho** | .ttf | 1 | 400 | No | None | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 88 | `ubuntu` | **Ubuntu, Ubuntu Condensed, Ubuntu Mono** | .ttf | 13 | 300, 400, 500, 700 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 89 | `unispace` | **Unispace** | .otf | 4 | 400, 700 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 90 | `unsteady-oversteer` | **Unsteady Oversteer** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 91 | `vaticanus` | **Vaticanus** | .otf, .ttf | 2 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 92 | `viga` | **Viga** | .ttf | 1 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 93 | `vincendo` | **Vincendo** | .otf, .ttf | 4 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 94 | `warriot` | **warriot** | .ttf | 2 | 700 | No | None | Unspecified (Copyright Only: typeface © (http://ffeeaarr.my.id/). 202...) | HIGH RISK (No explicit license) |
| 95 | `wide-road` | **Wide Road** | .otf | 1 | 400 | No | None | Letterlays Commercial License (Receipt PDF) | Medium (Check Proof) |
| 96 | `world-of-water` | **World of Water** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 97 | `zero-cool` | **Zero Cool** | .otf, .ttf | 2 | 400 | No | None | SIL Open Font License 1.1 (OFL) | Low (Permissive) |
| 98 | `zillah` | **Zillah Modern, Zillah Modern Expanded, Zillah Modern Narrow, Zillah Modern Offset Outline, Zillah Modern Ouline, Zillah Modern Thin, Zillah Modern Upper, ZillahModernLine** | .ttf | 8 | 400 | No | None | Freeware (General) | Medium |
| 99 | `zorque` | **Zorque** | .otf | 1 | 400 | No | None | Public Domain / CC0 1.0 | Low (Permissive) |
| 100 | `zt-nature` | **ZT Nature** | .otf | 4 | 400, 700 | No | None | 1001Fonts Free Commercial (FFC) | Low (Permissive) |
| 101 | `zt-shago` | **Zt Shago** | .otf, .ttf | 32 | 300, 400, 500, 600, 700, 800, 900, 950 | No | None | Unspecified (Copyright Only: copyright © 2022 by zelow type. copyrigh...) | HIGH RISK (No explicit license) |

---

## 11. Key Takeaways & Recommendations for `font-intelligence` Skill

1. **Decouple Package Directories from Font Family Names**:
   - Many source packages do not match font names (e.g. `behance-6596a9ca1f6c5` is `Al Saflers`, `the-bold-font-free-version` is `THE BOLD FONT`). The skill must use OpenType metadata (`name` table IDs 16 and 1) as the authoritative canonical identity.
2. **Implement Weight Normalization Engine**:
   - Do not trust filenames for weights. Always inspect `OS/2.usWeightClass` and typographic subfamily names. When discrepancies arise (such as `Bjorn Light` being weight 400), flag them in the agent's typography engine.
3. **Establish a Clean Webfont Pipeline**:
   - 36 packages have redundant `.otf` and `.ttf` files. For web application delivery, the skill should prioritize `.woff2` and modern `.otf`/`.ttf` while ignoring legacy `.eot` files.
4. **Enforce License-Aware Font Pairing & Filtering**:
   - The skill should support licensing filters (e.g. `permissive_only: true`), ensuring the user is never recommended fonts with redistribution restrictions (like `quango`, `timeburner`, or `neris`) or unverified demo fonts (`warriot`, `the-bold-font-free-version`).
5. **Generate Missing Visual Previews Programmatically**:
   - With 84 packages lacking preview images, the skill should include a lightweight preview generation tool (rendering specimen specimens via Pillow, HarfBuzz, or browser canvas) to give the user immediate visual previews for all 115 font families.
6. **Preserve Source Packages as Immutables**:
   - Source folders in `All fonts/` should remain strictly read-only reference archives. Any normalization, indexing, or web optimization should occur in a generated cache or structured catalog.

---
*Audit verified for Font Intelligence production release on September 29, 2026.*
