<div align="center">

# FONT INTELLIGENCE

### Typography Decision System

**Scored pairings. Verified weights. Zero tofu.**
An algorithmic typography decision system and font pairing engine for AI coding agents, UI/UX designers, and developers.<br>Replaces generic defaults with scored, anti-pattern-checked pairings and copy-pasteable tokens.

<br>

[![CI](https://img.shields.io/badge/CI-Passing-000000?style=flat-square&labelColor=555555)](.github/workflows/validate.yml)
[![Catalog](https://img.shields.io/badge/Catalog-413%20Families%20%7C%201%2C083%20Binaries-000000?style=flat-square&labelColor=555555)](catalog/fonts.json)
[![Public Assets](https://img.shields.io/badge/Public%20Assets-112%20Permissive%20Families-000000?style=flat-square&labelColor=555555)](docs/public-assets-manifest.md)
[![Tests](https://img.shields.io/badge/Tests-81%2F81%20Passed-000000?style=flat-square&labelColor=555555)](docs/v1-release-audit.md)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-000000?style=flat-square&labelColor=555555)](#quick-start)
[![Agents](https://img.shields.io/badge/Agents-8%20Platforms-000000?style=flat-square&labelColor=555555)](#agent-support)

[Quick Start](#quick-start) · [CLI](#cli) · [Scoring](#scoring-engine) · [Rules](#hard-rules) · [Agents](#agent-support) · [Licensing](#licensing) · [Contributing](#validate--contribute)

</div>

---

## Problem → Solution

| Agents and developers usually… | Font Intelligence… |
| :--- | :--- |
| Default to `Inter`, `Roboto`, `Arial` for every brand | Diagnoses the project across **29 use cases** and decodes vibe prompts ("expensive", "not AI-looking") |
| Request weights a font does not ship (e.g. `500` on a 700-only face) | Emits only weights listed in `technical.weights` |
| Guess script coverage and ship missing-glyph boxes (**tofu**) | Audits OpenType tables; reports 0 local fonts when unsupported and names verified companions |
| Set body text in display or distressed faces | Applies **10 anti-pattern penalties** (−15 to −45 pts) |
| Assume "free for commercial use" means redistributable | Tracks license and redistribution status per font |

---

## Features

| Capability | Detail |
| :--- | :--- |
| **10-dimension scoring** | Weighted pair evaluation from contrast to platform suitability |
| **Script audit** | Zero-tofu policy. Bangla and Arabic map to `Hind Siliguri`, `Noto Sans Bengali`, `Amiri` |
| **Public asset separation** | Permissive fonts in `assets/fonts/`; non-distributable packages stay `catalog-only` |
| **Code tokens** | CSS Custom Properties, Flutter `pubspec.yaml`, React Native `StyleSheet`, Microsoft Office TrueType embedding |
| **Non-destructive integration** | Works with existing design-system fonts; never overwrites them |
| **Interactive studio** | Zero-dependency preview to filter and test all 413 families |

---

## Quick Start

**Requirements:** Python 3.10 – 3.12 · Optional: `fonttools` for binary inspection

```bash
git clone https://github.com/ratulhub/font-intelligence.git
cd font-intelligence

pip install fonttools          # optional

./install.sh all               # Linux / macOS
.\install.ps1 -Target all      # Windows (PowerShell)
```

**Launch the preview studio**

```bash
python -m http.server 8080
# open http://localhost:8080/preview/index.html
```

---

## CLI

| Task | Command |
| :--- | :--- |
| Recommend pairings | `python scripts/recommend.py --use-case fintech --style "expensive, not AI-looking" --platform web` |
| Anchor on a chosen font | `python scripts/recommend.py --use-case saas --anchor "Chillax"` |
| Keep existing fonts | `python scripts/recommend.py --use-case ecommerce --existing-fonts "Inter, Roboto"` |
| Search the catalog | `python scripts/search_fonts.py --mood "clean" --role body --min-readability 8 --script Latin` |
| Score a pair | `python scripts/score_pair.py --primary chillax --secondary general-sans --style luxury` |
| Export fonts and snippets | `python scripts/copy_fonts.py --fonts "chillax,general-sans" --dest "dist/fonts" --snippets all` |
| Validate catalog | `python scripts/validate_catalog.py` |
| Audit licenses | `python scripts/validate_licenses.py --filter issues-only` |

---

## How It Works

```
Brief
  │
  ├─ 1. Diagnose project ............ catalog/use-cases.json
  ├─ 2. Translate vibe .............. style_interpretations
  ├─ 3. Explicit font given? ........ yes → anchor it (Rule 5)
  ├─ 4. Filter candidates ........... Rule 1
  ├─ 5. Script audit ................ zero tofu
  ├─ 6. Score 10 dimensions ......... catalog/scoring.json
  ├─ 7. Audit 10 anti-patterns ...... catalog/anti-patterns.json
  ├─ 8. Select confirmed weights .... Rule 2
  └─ 9. Output rationale + tokens
```

**Vibe decoder**

| Prompt | Typographic translation |
| :--- | :--- |
| **Expensive / Luxury** | High-contrast Didone serif or sculpted display sans, light-to-medium headlines, wide caps tracking (`+0.05em`), neutral sans body |
| **Clean / Minimalist** | Unadorned neo-grotesque, open apertures, monoline strokes, line-height `1.6+` |
| **Not AI-looking** | Character-rich display (`Ithaca`, `Chillax`, `Credit Valley`, `Reckoner`) with a 200–300 weight delta |
| **Technical / Developer** | High x-height sans, tabular figures (`tnum`), unambiguous mono (`Ubuntu Mono`) |

---

## Scoring Engine

| # | Dimension | Weight | Criteria |
| :-: | :--- | :-: | :--- |
| 1 | Visual Contrast | 15% | Weight delta ≥ 200 units; serif + sans classification contrast |
| 2 | Serif / Sans Dynamic | 12% | Harmony of structure and optical cadence |
| 3 | Personality Resonance | 12% | Cultural, historical, emotional alignment |
| 4 | Readability | 15% | x-height, aperture openness, reading endurance ≥ 7/10 |
| 5 | Proportional Width | 8% | Optical balance between headline and body widths |
| 6 | Weight Availability | 10% | Family depth, variable axes, confirmed true italics |
| 7 | Role Compatibility | 10% | Fit for the assigned role (display ≠ body) |
| 8 | Project Style Fit | 8% | Alignment with use-case design goals |
| 9 | Language Parity | 5% | Full glyph coverage for all target scripts |
| 10 | Platform Suitability | 5% | Web payload < 100 KB, Flutter rendering, PowerPoint TrueType outlines |

**Anti-pattern penalties**

| Anti-pattern | Penalty | Rule |
| :--- | :-: | :--- |
| Decorative as Body | −45 | No display or handwriting faces for paragraphs |
| Script Mismatch / Tofu | −45 | Unverified scripts are refused |
| Competing Display Fonts | −30 | One vocal lead per hierarchy |
| Weak Contrast / Flat Hierarchy | −25 | Weight delta ≥ 200 required |
| Excessive Font Families | −25 | Max 2 primary families (+ mono for code) |
| Personality Polar Clash | −25 | No conflicting tones (Luxury Serif + Graffiti) |
| Low x-Height in UI Microcopy | −20 | Open apertures for 11–13 px UI text |
| Hairline Screen Fatigue | −20 | No 100/200 weights for continuous body text |
| Monospace Longform Fatigue | −15 | Mono for code and tabular data only |
| Uncanny Sans Mismatch | −15 | No two near-identical neo-grotesques |

---

## Hard Rules

1. **Never invent** catalog fonts, weights, or language support.
2. **Never equate** commercial use with GitHub redistribution. Verify the license grant first ([`docs/redistribution-review.md`](docs/redistribution-review.md)).
3. **Respect explicit user fonts.** Adopt and pair around them.
4. **Do not replace** existing typography systems.
5. **No decorative fonts** in `body` or `ui` roles.
6. **Maximum 2 primary families**: 1 heading + 1 body/UI (+ mono when code or data is present).
7. **Readability ≥ 7/10** for body and UI.
8. **Respect platform limits**: WOFF2 < 100 KB for web; `.ttf` outlines for Microsoft Office.
9. **Always generate** calibrated system fallbacks.

---

## Agent Support

One canonical skill. Every adapter is a pointer, never a copy.

```
.agents/skills/font-intelligence/SKILL.md   ← single source of truth
catalog/                                    ← fonts · use-cases · pairings · scoring · anti-patterns
lite/font-intelligence-lite.md              ← compact fallback for tight contexts
```

| Platform | Adapter |
| :--- | :--- |
| Antigravity | `.agents/skills/font-intelligence/` · `.agents/rules/font-intelligence.md` |
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md` · `.codex/instructions.md` |
| Cursor | `.cursorrules` · `.cursor/rules/font-intelligence.mdc` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` |

---

## Reference Guides

| Area | Guides |
| :--- | :--- |
| Typography | [`typography-rules`](references/typography-rules.md) · [`pairing-rules`](references/pairing-rules.md) · [`accessibility`](references/accessibility.md) |
| Web | [`web`](references/web.md) · [`react`](references/react.md) · [`nextjs`](references/nextjs.md) · [`tailwind`](references/tailwind.md) |
| Mobile | [`flutter`](references/flutter.md) · [`react-native`](references/react-native.md) · [`android`](references/android.md) · [`ios`](references/ios.md) |
| Documents and slides | [`presentations`](references/presentations.md) · [`documents`](references/documents.md) · [`branding`](references/branding.md) |

---

## Licensing

Each font keeps its original license. All 413 families are cataloged with verified terms in [`catalog/fonts.json`](catalog/fonts.json).

| Tier | Families | Terms |
| :--- | :-: | :--- |
| **Open Source** | 108 | OFL 1.1, Apache 2.0, MIT, Ubuntu Font License, CC0 |
| **Free for Commercial Use** | 390 | Explicitly approved for commercial projects |
| **Redistributable Public Assets** | 112 | Verified packages in `assets/fonts/`, safe for repository redistribution |
| **Personal Use Only** | 23 | Preserved for local design evaluation |

Records: [`docs/redistribution-review.md`](docs/redistribution-review.md) · [`docs/public-assets-manifest.md`](docs/public-assets-manifest.md)

---

## Validate & Contribute

Run before every push:

```bash
python scripts/validate_catalog.py                              # schema, IDs, file paths
python scripts/validate_licenses.py --filter issues-only        # licensing audit
python -m unittest discover -s tests -p "test_*.py"             # 58 domain tests
python -m unittest discover -s scripts -p "test_*.py"           # 23 CLI and engine tests
python scripts/run_evaluation_matrix.py                         # 24/24 real-user evaluation
```

Adding fonts, use cases, or pairings? Read [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## License

Engine, scripts, decision models, and agent skill files: [MIT](LICENSE).
Font binaries in `All fonts/` retain their original foundry licenses (OFL, Apache, CC0, Freeware) as documented in `catalog/fonts.json`.
