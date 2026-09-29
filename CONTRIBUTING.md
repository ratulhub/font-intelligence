# Contributing to Font Intelligence

Thank you for your interest in contributing to the **Font Intelligence Typography Decision System**!

Font Intelligence is an engineering-grade typography decision engine. We prioritize mathematical contrast scoring, verified OpenType technical metadata, strict language/script parity (zero tofu), and legal redistribution compliance over subjective trends.

---

## Code of Conduct & Core Principles

1. **Zero Hallucination Policy**: Never invent catalog fonts, weights, Unicode script coverage, or licensing permissions.
2. **Understand Before Choosing**: Font recommendations must be backed by project situation constraints, platform rendering requirements, and a clear typographic rationale explaining **WHY** the combination works.
3. **Single Canonical Truth**: All agent adapters and tools share the single canonical skill at [`.agents/skills/font-intelligence/SKILL.md`](file:///d:/font-intelligence/.agents/skills/font-intelligence/SKILL.md) and the single canonical catalog in `catalog/`. Never maintain duplicate font databases.

---

## How to Add New Fonts to the Catalog

To propose a new font family for inclusion in the Font Intelligence catalog, follow this structured workflow:

### Step 1: Verify Licensing & Commercial Redistribution
- Check the font's license document before copying files.
- Fonts must grant **Commercial Use** and **Redistribution Rights** (e.g., SIL Open Font License 1.1, Apache 2.0, MIT, Creative Commons Zero, or verified commercial distribution EULA).
- Demo cuts, non-commercial personal-use-only fonts, and fonts with unclear provenance will **not** be accepted into the core catalog.

### Step 2: Add Font Files & License
Place the font package in `All fonts/<family-id>/`:
```
All fonts/<family-id>/
  ├── <family-id>.ttf (or .otf, .woff2)
  ├── OFL.txt (or LICENSE.txt)
  └── README.txt (if provided by foundry)
```
> **Important**: Never delete original foundry license or readme files.

### Step 3: Run Binary Scanner
Extract OpenType technical tables, weights, styles, variable axes, and Unicode script blocks:
```bash
python scripts/scan_fonts.py --source "All fonts/<family-id>" --update-catalog
```

### Step 4: Curate Editorial Metadata
Edit the new font's entry in `catalog/fonts.json` to assign calibrated editorial metadata:
- **`curated.category`**: `sans-serif`, `serif`, `display`, `monospace`, or `handwriting`.
- **`curated.styles`**: Controlled style categories (`modern`, `luxury`, `editorial`, `technical`, `brutalist`, `minimal`, etc.).
- **`curated.roles`**: Permitted typography roles (`hero`, `heading`, `body`, `ui`, `number`, `code`, `logo`).
- **`curated.readability`**: Calibrated ratings from 1 to 10 for:
  - `body` (Continuous paragraphs; must have generous x-height and open apertures to score $\ge 7$)
  - `long_form` (Multi-page articles and reading endurance)
  - `ui` (Small button labels, navigation, and form inputs)
  - `small_text` (10–12px captions and microcopy)
  - `numbers` (Tabular alignment and numeral distinction)
- **`curated.fallback`**: Standard generic system fallback stacks.

---

## How to Add Use Cases & Pairings

### Adding a Use Case (`catalog/use-cases.json`)
Each project situation must define:
- `id`: Unique kebab-case identifier (e.g. `medical-portal`).
- `category`: `web`, `app`, `document`, or `marketing`.
- `primary_intent`: 1-sentence design goal.
- `key_requirements`: Readability priorities (1–10), ideal styles, forbidden styles.
- `platform_performance`: Payload budget (KB), preferred formats (`woff2`, `ttf`), variable font recommendation.

### Adding a Curated Pairing (`catalog/pairings.json`)
Each masterclass pairing must define:
- `id`: Kebab-case pairing identifier (e.g. `primary-secondary-style`).
- `primary_font` and `secondary_font`: Target confirmed weights and roles.
- `contrast_metrics`: Weight delta, classification contrast, stroke dynamic, x-height harmony.
- `rationale`: Exhaustive typographic rationale explaining the **WHY**, optical cadence, and role harmony.

---

## Required Pre-Commit Validation

Before submitting a Pull Request, run the complete validation and test suite locally:

```bash
# 1. Validate Catalog Schema, IDs, and File Paths
python scripts/validate_catalog.py

# 2. Audit Licensing & Redistribution Terms
python scripts/validate_licenses.py --filter issues-only

# 3. Run Automated Unit Test Suites (Domain & Engine)
python -m unittest discover -s tests -p "test_*.py"
python -m unittest discover -s scripts -p "test_*.py"

# 4. Run Real-User Evaluation Matrix (16 Cases + 8 Failure Cases)
python scripts/run_evaluation_matrix.py
```

All 4 commands must pass with **0 errors**.

---

## Pull Request Checklist

- [ ] All new font files exist on disk and are referenced in `catalog/fonts.json`.
- [ ] Original license files are preserved in the font directory.
- [ ] No duplicate IDs exist in `catalog/fonts.json` or `catalog/pairings.json`.
- [ ] Readability scores and role assignments are realistic (display fonts are not marked as body).
- [ ] Target scripts in `technical.scripts` match actual OpenType `cmap` character coverage.
- [ ] `validate_catalog.py`, `validate_licenses.py`, and test suites pass completely.
- [ ] PR description includes sample visual output or screenshot from `preview/index.html`.
