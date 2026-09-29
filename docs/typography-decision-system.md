# Typography Decision System Specification & Architecture

## Overview

The **Font Intelligence Typography Decision System** elevates font pairing from subjective visual intuition into an algorithmic, multi-criteria decision framework. Rather than simply returning popular or default fonts, the system evaluates typeface pairings based on structural contrast, role specialization, verified readability ratings, historical synergy, and technical performance.

---

## 1. Controlled Taxonomy & Ontologies

### 1.1 Controlled Style Categories
All 103 typographic families in the repository catalog (`catalog/fonts.json`) have been enriched with normalized, controlled style categories:
- `modern`
- `premium`
- `luxury`
- `editorial`
- `fashion`
- `technical`
- `corporate`
- `playful`
- `classic`
- `futuristic`
- `minimal`
- `brutalist`
- `industrial`
- `geometric`
- `humanist`
- `retro`
- `vintage`
- `organic`
- `grunge`
- `art-deco`
- `decorative`
- `handwritten`

### 1.2 Functional Typography Roles
Typefaces are mapped to specific roles based on optical structure and design intent:
- `display`: Expressive pull-quotes, posters, section banners (32px+)
- `hero`: Monumental page headers, high-impact titles (40px+)
- `heading`: Structural document titles (H1–H3)
- `body`: Primary running paragraphs and prose (15–18px)
- `ui`: Navigation labels, controls, modals, tabs, form inputs
- `button`: Interactive action triggers and call-to-actions
- `number`: Dashboard figures, pricing tables, data visualizations
- `caption`: Footnotes, image credits, microcopy, legal text (11–13px)
- `code`: Monospaced syntax, terminal blocks, telemetry, API payloads
- `logo` / `branding`: Visual trademarks and brand marks
- `accent`: Stylistic flourishes, stickers, badge labels

### 1.3 Readability & Legibility Properties (1–10 Scale)
Every typeface features verified optical ratings across 5 distinct reading contexts:
1. `body`: Reading rhythm, counter balance, and eye fatigue resistance.
2. `long_form`: Saccadic scanning ease over multi-page documents.
3. `ui`: Distinct glyph shapes, horizontal density, and interface contrast.
4. `small_text`: Legibility at 10–13px subpixel screen rendering.
5. `numbers`: Tabular alignment, distinct digit shapes (0 vs O, 1 vs l vs I).

---

## 2. The 10-Dimensional Scoring Model (`catalog/scoring.json`)

Pairings are evaluated using a formal 10-dimensional weighted rubric:

$$ \text{Composite Score} = \sum_{i=1}^{10} (\text{Dimension Score}_i \times \text{Weight}_i) - \text{AntiPattern Penalties} $$

| Dimension | Weight | Primary Factors Evaluated |
| :--- | :--- | :--- |
| **1. Visual Contrast** | `15%` | Weight delta ($\ge 300$ units optimal), stroke modulation contrast, structural divergence. |
| **2. Serif / Sans Relationship** | `12%` | Cross-classification harmony (Serif + Sans, Superfamily, or distinct Sans subfamilies). |
| **3. Personality Resonance** | `12%` | Emotional resonance; eliminates unintended tonal friction between fonts. |
| **4. Readability / Legibility** | `15%` | Secondary font's verified rating in its assigned role (must be $8+$ for body/UI). |
| **5. Width & Proportions** | `8%` | Horizontal rhythm, x-height parity, intentional vs accidental condensed/extended pairing. |
| **6. Weight Availability** | `10%` | Breadth of weight ladder, variable font support, presence of true companion italics. |
| **7. Role Compatibility** | `10%` | Verification that each font is engineered and curated for its assigned role. |
| **8. Project Style Alignment** | `8%` | Degree of intersection between fonts and the requested brand aesthetic. |
| **9. Language & Script Parity** | `5%` | Unicode block and language support overlap (prevents missing glyphs and tofu boxes). |
| **10. Platform Suitability** | `5%` | Web format availability (WOFF2/variable), rasterization performance, file payload size. |

### Grade Tiers
- **95–100**: `Masterclass` (Exemplary synergy, optimal hierarchy and effortless legibility)
- **88–94**:  `Exceptional` (Highly recommended, production-ready, distinct character)
- **80–87**:  `Good` (Solid workhorse pair, dependable contrast)
- **70–79**:  `Acceptable` (Viable, requires deliberate sizing or weight management)
- **55–69**:  `Marginal` (Suboptimal contrast or slight stylistic discord)
- **< 55**:   `Incompatible` (Anti-pattern triggered; fails fundamental readability or hierarchy)

---

## 3. Typographic Anti-Patterns (`catalog/anti-patterns.json`)

The engine enforces strict guardrails against common typography mistakes:

1. **`decorative-as-body`** (`CRITICAL`, `-45` pts):
   - Using display, handwriting, or low-readability fonts (< 6/10) for body/UI copy.
2. **`two-similar-display-fonts`** (`HIGH`, `-30` pts):
   - Pairing two distinct display, condensed, or expressive fonts simultaneously.
3. **`weak-heading-body-contrast`** (`HIGH`, `-25` pts):
   - Heading and body sharing the same weight (e.g. 400 vs 400) and classification with flat hierarchy.
4. **`excessive-font-families`** (`HIGH`, `-25` pts):
   - Loading 4 or more distinct font families in a single application.
5. **`language-script-mismatch`** (`CRITICAL`, `-45` pts):
   - Primary or secondary font lacks glyphs for required target languages.
6. **`low-x-height-ui`** (`HIGH`, `-20` pts):
   - Fonts with compact x-heights or closed apertures used in 11–13px UI microcopy.
7. **`hairline-screen-fatigue`** (`HIGH`, `-20` pts):
   - Setting body text in weight 100 or 200 on digital screens.
8. **`monospace-longform-fatigue`** (`MEDIUM`, `-15` pts):
   - Using monospace fonts for multi-paragraph continuous prose.
9. **`uncanny-sans-mismatch`** (`MEDIUM`, `-15` pts):
   - Mixing two slightly different neo-grotesques from different foundries.
10. **`personality-polar-clash`** (`HIGH`, `-25` pts):
    - Incongruous pairing of clashing emotional genres (e.g. street graffiti with luxury corporate serif).

---

## 4. Curated Masterclass Pairings (`catalog/pairings.json`)

The catalog contains 12 pre-calibrated masterclass pairs covering diverse aesthetic and functional domains:

1. **Tech Luxury & SaaS**: `Chillax` (Hero 600) + `General Sans` (Body 400) + `Ubuntu Mono` (Code) — *Score: 98*
2. **Editorial Luxury & Fashion**: `Ithaca` (Hero 500) + `General Sans` (Body 400) — *Score: 97*
3. **Classical Publishing**: `Credit Valley` (Hero 700) + `Credit Valley` (Body 400) + `General Sans` (UI) — *Score: 96*
4. **Industrial Brutalism**: `Reckoner` (Hero 700) + `Ubuntu` (Body 400) + `Ubuntu Mono` (Code) — *Score: 95*
5. **Cyberpunk & Sci-Fi**: `Neuropol` (Hero 400) + `General Sans` (Body 400) + `Unispace` (HUD/Data) — *Score: 93*
6. **High Fashion**: `Kingsbridge` (Hero 700) + `Chillax` (Body 400) — *Score: 95*
7. **Minimalist Product**: `Oligopoly` (Hero 700) + `Gudea` (Body 400) — *Score: 94*
8. **Developer Platform**: `General Sans` (H1 600) + `Ubuntu` (Body 400) + `Ubuntu Mono` (Code) — *Score: 97*
9. **Heavy Journalism**: `Zt Shago` (Hero 800) + `Credit Valley` (Body 400) + `General Sans` (Caption) — *Score: 96*
10. **Playful Community**: `Alphakind` (Hero 400) + `Simply Sans` (Body 400) — *Score: 92*
11. **Retro 8-Bit Gaming**: `Raster Forge` (Hero 400) + `General Sans` (Body 400) + `Raster Forge` (Number) — *Score: 91*
12. **Multilingual Korean**: `BM DoHyeon` (Hero 400) + `General Sans` (Body 400) + `Ubuntu` (Caption) — *Score: 94*

---

## 5. Dynamic Pairing Engine (`scripts/typography_engine.py`)

The dynamic pairing engine evaluates any two fonts (including arbitrary or unlisted typefaces) and dynamically recommends pairings across the entire catalog.

### CLI Usage Examples:

```bash
# 1. Evaluate a specific pairing
python scripts/typography_engine.py evaluate --primary chillax --secondary general-sans --style luxury

# 2. Dynamically recommend pairings for an aesthetic style
python scripts/typography_engine.py recommend --style brutalist --limit 3

# 3. Dynamically find optimal partners for a specific primary font
python scripts/typography_engine.py recommend --primary ithaca --style luxury --limit 3

# 4. List curated masterclass pairings
python scripts/typography_engine.py curated

# 5. Inspect anti-pattern rules
python scripts/typography_engine.py anti-patterns
```
