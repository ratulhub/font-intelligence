# Font Intelligence: Typography Decision System

[![CI Status](https://img.shields.io/badge/CI-Passing-success?style=flat-square)](file:///.github/workflows/validate.yml)
[![Verified Fonts](https://img.shields.io/badge/Catalog-103%20Families%20(475%20Files)-blue?style=flat-square)](file:///catalog/fonts.json)
[![Evaluation Matrix](https://img.shields.io/badge/Evaluation-24%2F24%20Tests%20Passed-brightgreen?style=flat-square)](file:///docs/evaluation-report.md)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square)](#installation)
[![Multi-Agent Portable](https://img.shields.io/badge/Agents-8%20Platforms%20Supported-purple?style=flat-square)](#supported-agent-architecture)

An engineering-grade typography decision engine and font intelligence system for modern AI coding agents and human designers. Replaces generic defaults (Inter, Roboto, Arial) with mathematically scored, anti-pattern-checked typeface pairings backed by deep typographic rationales and copy-pasteable implementation tokens.

---

## 1. What Font Intelligence Is

Coding agents and developers frequently struggle with digital typography:
- They default to the same 3 bland fonts (`Inter`, `Roboto`, `Arial`) regardless of brand tone or use case.
- They hallucinate weights that don't exist in font binaries (e.g., requesting `weight: 500` for a font that only has 700).
- They guess language script coverage, resulting in missing character boxes (**tofu**) on international scripts like Bangla or Arabic.
- They commit catastrophic typography anti-patterns, such as setting multi-paragraph body text in distressed display fonts or pairing competing novelty fonts.
- They assume "free for commercial use" allows redistribution on GitHub without checking license terms.

**Font Intelligence solves this.**

Font Intelligence operates as an algorithmic design partner:
1. **Diagnoses the Project**: Understands 29 use cases (SaaS, Fintech, Crypto, Fashion, Dashboards, Mobile, Pitch Decks, Resumes).
2. **Decodes Aesthetic Vibes**: Translates colloquial prompts ("expensive", "clean", "not AI-looking") into formal typographic classifications.
3. **Audits Language Scripts (Zero Tofu)**: Verifies OpenType binary tables. If an international script is unsupported locally, it strictly reports 0 local fonts and recommends verified open-source companion fonts (`Hind Siliguri`, `Noto Sans Bengali`, `Amiri`).
4. **Evaluates 10 Mathematical Dimensions**: Scores candidate pairs across Visual Contrast, Serif/Sans Dynamic, Personality Resonance, Readability, Width, Weight Availability, Role Compatibility, Project Style Fit, Language Parity, and Platform Suitability.
5. **Audits 10 Lethal Anti-Patterns**: Deducts severe penalties (-15 to -45 pts) for unreadable body text, uncanny sans mismatches, or weight starvation.
6. **Delivers Calibrated Code Tokens**: Emits production-ready CSS Custom Properties, Flutter `pubspec.yaml`, React Native `StyleSheet`, and Microsoft Office TrueType embedding instructions.

---

## 2. Supported Agent Architecture

Font Intelligence follows a **single canonical truth** architecture. All coding agents share the exact same rules, catalog, and scoring engine:

```
CORE SKILL (.agents/skills/font-intelligence/SKILL.md)
  ├── Universal Entry   → AGENTS.md
  ├── Thin Adapters (Pointers only; never duplicate the skill):
  │   ├── Antigravity   → .agents/skills/font-intelligence/ & .agents/rules/font-intelligence.md
  │   ├── Claude Code   → CLAUDE.md
  │   ├── Codex         → AGENTS.md & .codex/instructions.md
  │   ├── Cursor        → .cursorrules & .cursor/rules/font-intelligence.mdc
  │   ├── Windsurf      → .windsurfrules
  │   ├── Cline         → .clinerules
  │   ├── GitHub Copilot→ .github/copilot-instructions.md
  │   └── Gemini CLI    → GEMINI.md
  ├── Compact Fallback  → lite/font-intelligence-lite.md (Cheatsheet for tight contexts)
  └── Canonical Data    → catalog/ (fonts, use-cases, pairings, scoring, anti-patterns)
```

No separate font databases or duplicate schemas are maintained across agents.

---

## 3. Installation & Getting Started

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Optional: `fonttools` (for binary scanning tools)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/font-intelligence.git
cd font-intelligence

# 2. (Optional) Install fonttools for binary inspection
pip install fonttools

# 3. Install platform adapters (Antigravity, Cursor, Claude, Windsurf, Cline, Copilot, Codex, Gemini)
# Bash (Linux/macOS):
./install.sh all
# PowerShell (Windows):
.\install.ps1 -Target all
```

### Comprehensive Platform & Typography Manuals
Explore deep reference guides in [`references/`](file:///references/):
- **Typography & Scale**: [`typography-rules.md`](file:///references/typography-rules.md), [`pairing-rules.md`](file:///references/pairing-rules.md), [`accessibility.md`](file:///references/accessibility.md)
- **Web & Frameworks**: [`web.md`](file:///references/web.md), [`react.md`](file:///references/react.md), [`nextjs.md`](file:///references/nextjs.md), [`tailwind.md`](file:///references/tailwind.md)
- **Mobile**: [`flutter.md`](file:///references/flutter.md), [`react-native.md`](file:///references/react-native.md), [`android.md`](file:///references/android.md), [`ios.md`](file:///references/ios.md)
- **Documents & Slides**: [`presentations.md`](file:///references/presentations.md), [`documents.md`](file:///references/documents.md), [`branding.md`](file:///references/branding.md)

### Launch Interactive Visual Studio
Font Intelligence includes an interactive, zero-dependency typography preview studio:
```bash
python -m http.server 8080
```
Open **`http://localhost:8080/preview/index.html`** in your browser to inspect all 103 families, filter by role/readability/style, and test interactive type specimens.

---

## 4. How Font Selection Works

Font Intelligence follows a strict 10-step protocol:

```mermaid
graph TD
    A["User Request / Brief"] --> B["1. Diagnose Project (use-cases.json)"]
    B --> C["2. Translate Vibe (style_interpretations)"]
    C --> D{"3. Explicit Font Specified?"}
    D -- "Yes" --> E["Anchor User Font (Rule 5)"]
    D -- "No" --> F["Filter Candidates (Rule 1)"]
    E --> F
    F --> G["4. Strict Script Audit (Zero Tofu)"]
    G --> H["5. Score 10 Dimensions (scoring.json)"]
    H --> I["6. Audit 10 Anti-Patterns (anti-patterns.json)"]
    I --> J["7. Select Confirmed Weights (Rule 2)"]
    J --> K["8. Generate Typographic 'WHY' & Tokens"]
```

### Colloquial Style Decoder
- **"Expensive / Luxury"**: High stroke contrast (Didone serif or sculpted display sans) + light/medium headline weights + wide all-caps tracking (`+0.05em`) + neutral sans body.
- **"Clean / Minimalist"**: Unadorned neo-grotesque + open apertures + consistent monoline strokes + generous line-height (`1.6+`).
- **"Not AI-Looking / Distinctive"**: Eliminates flat Inter defaults. Pairs character-rich display cuts (`Ithaca`, `Chillax`, `Credit Valley`, `Reckoner`) with a 200–300 weight delta and optical tracking.
- **"Technical / Developer"**: High x-height sans + tabular figures (`tnum`) + unambiguous monospaced glyphs (`Ubuntu Mono`).

---

## 5. How Pairing Works: 10-Dimensional Scoring Engine

Every combination is evaluated across 10 mathematical dimensions with weighted scoring:

| # | Dimension | Weight | Evaluation Criteria |
| :-: | :--- | :-: | :--- |
| **1** | **Visual Contrast** | 15% | Stroke weight delta ($\ge 200$ units), classification contrast (Serif + Sans). |
| **2** | **Serif/Sans Dynamic** | 12% | Harmony between structural skeleton and optical cadence. |
| **3** | **Personality Resonance**| 12% | Alignment of cultural, historical, and emotional archetypes. |
| **4** | **Readability / Legibility**| 15% | X-height, aperture openness, and continuous reading endurance ($\ge 7/10$). |
| **5** | **Proportional Width** | 8% | Aspect ratio optical balance; prevents cramped headlines over wide body. |
| **6** | **Weight Availability**| 10% | Superfamily depth, variable axes, confirmed true italics. |
| **7** | **Role Compatibility** | 10% | Suitability for designated typographic role (Display $\neq$ Body). |
| **8** | **Project Style Fit** | 8% | Direct semantic alignment with use-case design goals. |
| **9** | **Language / Script Parity**| 5% | Zero tofu tolerance; full glyph parity across all target languages. |
| **10**| **Platform Suitability**| 5% | Web payload (< 100 KB), Flutter rendering, PowerPoint TrueType outline checks. |

### Anti-Pattern Prevention (Penalties)
Combinations triggering anti-patterns receive severe point deductions:
- ❌ **Decorative as Body** (-45 pts): Never use display or handwriting fonts for paragraphs.
- ❌ **Competing Display Fonts** (-30 pts): Only one vocal visual lead in a hierarchy.
- ❌ **Weak Contrast / Flat Hierarchy** (-25 pts): Requires $\ge 200$-unit weight delta.
- ❌ **Excessive Font Families** (-25 pts): Maximum 2 primary families (plus monospace only for code).
- ❌ **Script Mismatch / Zero Tofu** (-45 pts): Refuses to guess unverified scripts.
- ❌ **Low x-Height in UI Microcopy** (-20 pts): Enforces open apertures for 11–13px buttons/badges.
- ❌ **Hairline Screen Fatigue** (-20 pts): Prohibits 100/200 weights for continuous screen body text.
- ❌ **Monospace Longform Fatigue** (-15 pts): Restricts monospace to code snippets and tabular data.
- ❌ **Uncanny Sans Mismatch** (-15 pts): Prevents pairing two near-identical neo-grotesques.
- ❌ **Personality Polar Clash** (-25 pts): Forbids conflicting tones (e.g. Luxury Serif + Street Graffiti).

---

## 6. Fast CLI Execution

Run supporting tools directly from your terminal:

```bash
# 1. Recommend Pairings from Project Brief
python scripts/recommend.py --use-case fintech --style "expensive, not AI-looking" --platform web

# 2. Anchor Around an Explicit User Font Choice (Hard Rule 5)
python scripts/recommend.py --use-case saas --anchor "Chillax"

# 3. Integrate Non-Destructively with an Existing Design System (Hard Rule 6)
python scripts/recommend.py --use-case ecommerce --existing-fonts "Inter, Roboto"

# 4. Search Catalog by Mood, Role, and Script
python scripts/search_fonts.py --mood "clean" --role body --min-readability 8 --script Latin

# 5. Score a Specific Font Pair (10 Dimensions + Anti-Patterns)
python scripts/score_pair.py --primary chillax --secondary general-sans --style luxury

# 6. Export Selected Font Binaries and Generate CSS / Flutter Snippets
python scripts/copy_fonts.py --fonts "chillax,general-sans" --dest "dist/fonts" --snippets all

# 7. Validate Entire Catalog Schema & References
python scripts/validate_catalog.py

# 8. Audit Licensing, Commercial Terms, and PowerPoint Embeddability
python scripts/validate_licenses.py --filter issues-only
```

---

## 7. Hard Non-Negotiable Rules

1. **Never invent catalog fonts**: Only recommend real, verified fonts from `catalog/fonts.json`.
2. **Never invent weights**: Only specify weights listed in `technical.weights`.
3. **Never invent language support**: Zero tofu tolerance. For Bangla, Arabic, etc., recommend verified external companion fonts (`Hind Siliguri`, `Noto Sans Bengali`, `Amiri`).
4. **Never assume commercial use = GitHub redistribution**: Verify license grants before redistributing font files. See [`docs/redistribution-review.md`](file:///d:/font-intelligence/docs/redistribution-review.md).
5. **Respect explicit user font choices**: If the user asks for a font, adopt it and pair around it. Never override user selections.
6. **Do not replace existing typography systems**: Integrate with existing fonts; never overwrite unprompted.
7. **No decorative fonts for body text**: Display, script, and decorative typefaces must never be assigned to `body` or `ui` roles.
8. **Maximum of 2 primary families**: 1 heading + 1 body/UI (plus monospace only when code/data is present).
9. **Enforce readability scores $\ge 7/10$** for body and UI.
10. **Respect platform constraints**: Payloads < 100 KB for Web (WOFF2); TrueType (`.ttf`) outlines for Microsoft Office to avoid substitution bugs.
11. **Always generate calibrated system fallbacks**.

---

## 8. Licensing & Redistribution Terms

All 103 font families in Font Intelligence are cataloged with their exact legal licensing terms. Refer to [`docs/redistribution-review.md`](file:///d:/font-intelligence/docs/redistribution-review.md) for the complete legal review.

- **Permissive Open Source (57 Families)**: Distributed under SIL Open Font License (OFL 1.1), Apache 2.0, MIT, Ubuntu Font License, or Creative Commons Zero (CC0). Fully redistributable.
- **Freeware Commercial (20 Families)**: Commercial use granted by author/foundry.
- **Proof Needed (13 Families)**: Commercial license granted via marketplace receipts; redistribution on public repositories requires proof of purchase.
- **Restricted / Demo Cuts (13 Families)**: Evaluation cuts requiring commercial upgrades for production deployment. The system warns developers before exporting.

---

## 9. How to Validate & Contribute

### Pre-Push Validation Checklist
Before pushing code or publishing updates, run the complete validation suite:
```bash
# 1. Schema, ID, and File Path Validation
python scripts/validate_catalog.py

# 2. Licensing Audit
python scripts/validate_licenses.py --filter issues-only

# 3. Comprehensive Domain Test Suites (58 tests: catalog, licensing, languages, 20 projects, 17 negative cases)
python -m unittest discover -s tests -p "test_*.py"

# 4. CLI Tools & Engine Test Suites (23 tests)
python -m unittest discover -s scripts -p "test_*.py"

# 5. Real-User Evaluation Matrix (24/24 tests)
python scripts/run_evaluation_matrix.py
```

For guidelines on adding new fonts, project use cases, or curated pairings, please read [`CONTRIBUTING.md`](file:///d:/font-intelligence/CONTRIBUTING.md).

---

## 10. License

The Font Intelligence software engine, scripts, decision models, and agent skill files are licensed under the [MIT License](LICENSE). Individual font binaries in `All fonts/` retain their original respective foundry licenses (OFL, Apache, CC0, Freeware) as documented in `catalog/fonts.json`.
