# Typography Pairing Rules & Scoring Protocol

Pairing typefaces requires mathematical balance between visual contrast and structural harmony. A great pairing establishes immediate hierarchy without competing for attention.

---

## 1. Core Pairing Principles

### Principle 1: One Vocal Lead (Role Differentiation)
Every pairing must have a designated **Lead** (usually Heading/Display) and a **Support Workhorse** (Body/UI).
- **Heading**: Expresses brand personality, artistic tone, or cultural cadence.
- **Body**: Prioritizes optical endurance, high x-height, open apertures, and zero reader fatigue.
- **Never pair two novelty fonts**: Combining two expressive display fonts (e.g. `Ithaca` + `Castle Chunk`) creates severe visual discord (Anti-Pattern: Competing Display Fonts, -30 pts).

### Principle 2: Sufficient Weight Delta ($\ge 200$ Units)
Maintain an optical weight delta of at least 200–300 units between heading and body:
- **Heading**: 700 (Bold) or 800 (ExtraBold)
- **Body**: 400 (Regular)
- Setting both in 400 or near-identical weights flattens visual hierarchy (Anti-Pattern: Weak Contrast, -25 pts).

### Principle 3: Classification Dynamic (Serif + Sans)
The most reliable optical pairing leverages classification contrast:
- **Geometric Sans Display + Humanist Serif Body**: Modern, architectural, intellectual.
- **High-Contrast Editorial Serif Heading + Clean Neo-Grotesque Body**: Premium, luxury, editorial.
- **Technical Sans Heading + Tabular Sans/Mono Body**: Developer tools, fintech, dashboards.
- **Caution**: Pairing two near-identical neo-grotesques (e.g., Arial + Helvetica lookalikes) causes an "uncanny valley" mismatch (-15 pts).

### Principle 4: X-Height & Proportion Alignment
- If heading has a low x-height and body has a tall x-height, heading sizes must be scaled up to prevent body text from overpowering headlines.
- Avoid extreme width clashes: Do not pair an ultra-condensed headline with an expanded wide body typeface.

---

## 2. The 10-Dimensional Scoring Model

Every potential pairing is evaluated on a 100-point scale:

| # | Dimension | Weight | Target Metric |
| :-: | :--- | :-: | :--- |
| **1** | **Visual Contrast** | 15% | Weight delta $\ge 200$, distinct classification or optical weight. |
| **2** | **Serif/Sans Dynamic** | 12% | Harmonious skeleton relationship without competing details. |
| **3** | **Personality Resonance** | 12% | Emotional and cultural alignment with project vibe. |
| **4** | **Readability / Legibility** | 15% | Body font rating $\ge 7/10$, open apertures, generous counters. |
| **5** | **Proportional Width** | 8% | Balanced aspect ratios; optical cadence parity. |
| **6** | **Weight Availability** | 10% | Confirmed weights for hierarchy (Regular, Medium, Bold, Italic). |
| **7** | **Role Compatibility** | 10% | Display fonts reserved for headings; workhorses for body/UI. |
| **8** | **Project Style Fit** | 8% | Semantic match with use-case requirements. |
| **9** | **Language / Script Parity**| 5% | Zero tofu tolerance; full glyph support across target languages. |
| **10**| **Platform Suitability** | 5% | Web payload budget, mobile rendering, Office TrueType embedding. |

---

## 3. Ten Lethal Typography Anti-Patterns

1. **Decorative as Body (-45 pts)**: Setting continuous paragraph text in display, handwriting, or stencil typefaces.
2. **Script Mismatch / Zero Tofu (-45 pts)**: Missing glyphs producing tofu boxes on non-Latin scripts (Bangla, Arabic).
3. **Competing Display Fonts (-30 pts)**: Pairing two expressive novelty fonts in the same viewport.
4. **Weak Contrast / Flat Hierarchy (-25 pts)**: Using the same weight and style for title and body.
5. **Excessive Font Families (-25 pts)**: Using more than 2 primary families (3rd allowed only for monospace code).
6. **Personality Polar Clash (-25 pts)**: Combining contradictory emotional archetypes (e.g., Luxury Serif + Punk Stencil).
7. **Low x-Height in UI Microcopy (-20 pts)**: Using low x-height fonts for dense 11–13px button and form labels.
8. **Hairline Screen Fatigue (-20 pts)**: Using 100/200 ultra-light weights for digital body paragraphs.
9. **Monospace Longform Fatigue (-15 pts)**: Setting multi-paragraph articles in monospaced fonts.
10. **Uncanny Sans Mismatch (-15 pts)**: Pairing two nearly identical neo-grotesque sans typefaces with subtle conflicting curves.
