---
name: font-intelligence
description: Algorithmic typography decision system. Evaluates pairings across 10 dimensions, diagnoses project situations, prevents anti-patterns, verifies language/platform constraints, and generates implementation tokens.
---

# Font Intelligence: Typography Decision System

An engineering-grade typography decision engine. Understands the project, audience, platform, and language before selecting typefaces. Replaces generic defaults with mathematically scored, anti-pattern-checked pairings backed by clear typographic rationales.

---

## 1. Ten-Step Workflow

### Step 1: Detect Whether Typography is Relevant
Activate this skill when the task involves UI design, web/app development, branding, slide decks, documents, CSS styling, or font selection/pairing decisions.

### Step 2: Understand the Project Context
Before suggesting any typeface, determine:
- **Project Type**: Identify use case from `catalog/use-cases.json` (e.g., `saas`, `fintech`, `ecommerce`, `dashboard`, `blog`, `powerpoint`, etc.).
- **Platform**: Web (browser), Native Mobile (Flutter, React Native, iOS, Android), or Document (PowerPoint, Word, PDF).
- **Language & Scripts**: Target scripts (Latin, Cyrillic, Greek, Devanagari, Bangla, Arabic, etc.).
- **Style & Vibe**: Translate user terms (e.g., "expensive", "clean", "editorial", "not AI-looking") using `catalog/use-cases.json#style_interpretations`.
- **Audience**: Professional, consumer, high-wealth, technical, academic, or playful.
- **Existing Design System**: Check existing stylesheets, tokens, or brand assets.

### Step 3: Check for User-Selected Fonts
- If the user explicitly requested a font (e.g., "Use Playfair Display" or "We use Poppins"):
  - **Do NOT replace or override it**.
  - Respect their choice as the anchor (Primary or Secondary).
  - Find the optimal companion partner from the catalog that complements its classification, x-height, and tone.

### Step 4: Load Catalog Data & Utilize Supporting Tools
Access catalog files from `catalog/` or execute dedicated supporting CLI tools from `scripts/` (or `font-intelligence/scripts/`):
- **Recommend Pairings**: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <plat>`
- **Search Fonts**: `python scripts/search_fonts.py --mood "<vibe>" --role <body> --min-readability 8 --script <script>`
- **Score Pairings**: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
- **Export Assets & Code**: `python scripts/copy_fonts.py --fonts "<id1,id2>" --dest <assets/fonts> --snippets all`
- **Validate Catalog**: `python scripts/validate_catalog.py`
- **Audit Licenses**: `python scripts/validate_licenses.py --filter issues-only`
- **Scan Source Binaries**: `python scripts/scan_fonts.py --source "All fonts"`
- **Direct JSON Reading (Fallback)**: When Python cannot execute, read JSON files directly:
  - `catalog/use-cases.json`: Project requirements, performance budgets, and style mappings.
  - `catalog/fonts.json`: 103 verified font families with roles, readability (1–10), and technical tables.
  - `catalog/pairings.json`: Curated masterclass pairings.
  - `catalog/anti-patterns.json`: 10 typography anti-patterns with point deductions.
  - `catalog/scoring.json`: 10-dimensional mathematical scoring model.

### Step 5: Filter Candidates
Eliminate unsuitable fonts from consideration:
- **Script Support**: Filter out fonts lacking verified glyphs for target scripts in `technical.scripts` / `unicode_blocks`.
- **Role & Readability**: Filter out fonts with low scores (< 7/10) for required roles (e.g., body/UI must have `curated.readability.body >= 7` or `ui >= 7`).
- **Platform Constraints**: For PowerPoint/Word, filter out fonts lacking `.ttf` outlines or embeddable `OS/2.fsType` permissions.

### Step 6: Score Candidates
Evaluate remaining candidates across the 10 dimensions from `catalog/scoring.json`:
1. Visual Contrast (15%) | 2. Serif/Sans Relationship (12%) | 3. Personality Resonance (12%)
4. Readability (15%) | 5. Proportional Width (8%) | 6. Weight Availability (10%)
7. Role Compatibility (10%) | 8. Project Style (8%) | 9. Language Parity (5%) | 10. Platform (5%)
- Apply penalty deductions (-15 to -45 pts) for any triggered anti-patterns from `catalog/anti-patterns.json`.

### Step 7: Generate Pairing & Articulate the "WHY"
Select the highest-scoring combination (curated or dynamic). Explain clearly:
- **Structural Contrast**: Why the category combination (e.g. Geometric Display + Neo-Grotesque Body) creates clean hierarchy.
- **Visual Cadence**: How x-heights, apertures, and proportions harmonize without reader fatigue.
- **Personality**: How the pairing reinforces the project's brand intent without generic flatness.

### Step 8: Build Typography Hierarchy
Establish explicit size, letter-spacing, and line-height scales:
- **Display / Hero**: Tight tracking (`-0.02em` to `-0.03em`), line-height `1.1` to `1.15`.
- **Headings (H1–H3)**: Tracking `-0.01em` to `-0.02em`, line-height `1.2` to `1.3`.
- **Body Text**: Normal tracking (`0`), line-height `1.5` to `1.65` for optimal readability.
- **UI & Buttons**: Micro-tracking (`+0.01em` to `+0.02em`), line-height `1.0` to `1.25`.
- **Numbers / Data**: Tabular figures (`tnum`) for tables/dashboards.

### Step 9: Select Weights
- Only select integer weights confirmed in `technical.weights` (e.g., `400`, `600`, `700`).
- Maintain a weight delta of at least **200–300 units** between headline and body (e.g., 700 vs 400) to ensure immediate visual hierarchy.

### Step 10: Provide Implementation Tokens
Deliver clean, copy-pasteable configuration with robust fallbacks:
- **Web**: CSS Custom Properties (`--font-heading`, `--font-body`, `--weight-heading`), Google/local `@font-face`, and `font-display: swap`.
- **Flutter**: `pubspec.yaml` font entries and Dart `TextStyle` declarations.
- **React Native**: Platform-specific `StyleSheet` definitions.
- **Office / PowerPoint**: `.ttf` file paths and PowerPoint embedding instructions.

---

## 2. Hard Rules

1. **Never invent catalog fonts**: Only recommend real, verified fonts from `catalog/fonts.json` when making autonomous catalog recommendations.
2. **Never invent weights**: Only specify weights listed in `technical.weights`. Never specify a weight (e.g. 500 or 900) unless confirmed in the font's data.
3. **Never invent language support**: Zero tofu tolerance. If a script (e.g. Bangla, Arabic) is not verified in catalog font binaries, state 0 catalog fonts exist and recommend verified external companion fonts (`Hind Siliguri`, `Noto Sans Bengali`, `Amiri`, etc.).
4. **Never invent license permissions**: Verify `technical.license` and `embedding_permission`.
5. **Respect explicit user font choices**: If the user asks for a font, adopt it and pair around it. Never override user font selections.
6. **Do not replace existing typography systems**: If a codebase has an established font system, integrate with or enhance it; never overwrite it unprompted.
7. **No decorative fonts for body text**: Display, script, and decorative typefaces must never be assigned to `body`, `long_form`, or dense `ui` roles.
8. **Maximum of 2 primary families**: Stick to 1 heading family and 1 body/UI family. Add a 3rd family (monospace) only if code/telemetry is required.
9. **Prioritize readability for body and UI**: Body/UI fonts must have verified readability scores $\ge 7/10$, open apertures, and adequate x-height.
10. **Respect platform and performance**: Enforce Core Web Vitals budgets (< 100 KB payload, WOFF2/variable fonts). For PowerPoint/Word, enforce TrueType (`.ttf`) outlines to prevent Microsoft Office substitution bugs.
11. **Always generate robust fallbacks**: Pair custom fonts with calibrated system fallback stacks (e.g. `system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif`).

---

## 3. Direct JSON Catalog Reading (Offline / No Python Mode)

When Python scripts cannot be executed, inspect the catalog JSON files directly:
- **Find project requirements**: Check `catalog/use-cases.json` under `use_cases.<id>`.
- **Map colloquial vibes**: Check `catalog/use-cases.json` under `style_interpretations.<vibe>`.
- **Filter fonts**: Inspect `catalog/fonts.json` matching `curated.styles`, `curated.roles`, and `technical.scripts`.
- **Pick curated pair**: Match `catalog/pairings.json` by `project_styles` or `use_case`.
- **Check anti-patterns**: Scan `catalog/anti-patterns.json` to verify the chosen pair avoids all 10 listed anti-patterns.
