# Font Intelligence Lite — Compact Typography Decision Fallback

> **Compact Cheatsheet**: Use this lightweight guide when operating under constrained context windows, offline environments without Python execution, or when rapid font recommendations are needed without loading the full 413-font catalog.
>
> **Canonical Source of Truth**: For dynamic scoring algorithms, licensing audits, and full technical metadata, always consult [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md).

---

## 1. Top Curated Masterclass Pairings

All typefaces below are verified with confirmed OpenType weights, licensed redistribution terms, and calibrated typographic metrics.

| Use Case / Vibe | Primary (Heading / Hero) | Secondary (Body / UI) | Accent / Code | Weight Delta | Why It Works |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SaaS & Modern Tech** | `Chillax` (SemiBold 600) | `General Sans` (Regular 400) | `Ubuntu Mono` (400) | 200 | Avant-garde geometric display meets ultra-clean neo-grotesque legibility. |
| **Fintech & Enterprise** | `General Sans` (SemiBold 600) | `Ubuntu` (Regular 400) | `Ubuntu Mono` (400) | 200 | Maximum reading clarity, robust UI apertures, unambiguous tabular numbers. |
| **Luxury & High Fashion** | `Ithaca` (Medium 500) | `General Sans` (Regular 400) | — | 100 | Haute-couture Didone display hairline contrast anchored by quiet modern sans. |
| **Editorial & Publishing** | `Credit Valley` (Bold 700) | `Credit Valley` (Regular 400) | `General Sans` (500 UI) | 300 | Classical bookish authority with true companion italics + crisp sans navigation. |
| **Industrial Brutalism** | `Reckoner` (Bold 700) | `Ubuntu` (Regular 400) | `Ubuntu Mono` (400) | 300 | Monolithic condensed uppercase headlines counterbalanced by warm, open body copy. |
| **Minimalist Product** | `Oligopoly` (Bold 700) | `Gudea` (Regular 400) | — | 300 | Sculpted Braun-style geometric precision paired with screen-optimized humanist prose. |
| **Developer Hub & Docs** | `General Sans` (SemiBold 600) | `Ubuntu` (Regular 400) | `Ubuntu Mono` (400) | 200 | Zero cognitive friction; top readability ratings (10/10) for deep technical docs. |
| **Breaking Journalism** | `Zt Shago` (ExtraBold 800) | `Credit Valley` (Regular 400) | `General Sans` (500 UI) | 400 | Front-page newspaper gravity coupled with literary immersion and true italics. |
| **Fashion Magazine** | `Kingsbridge` (Bold 700) | `Chillax` (Regular 400) | — | 300 | 44-weight architectural grotesque versatility paired with soft geometric modernism. |
| **Futuristic & Sci-Fi** | `Neuropol` (Regular 400) | `General Sans` (Regular 400) | `Unispace` (Bold 700) | 0 (Style shift) | Cyberpunk HUD silhouette without sacrificing dialogue/lore readability. |
| **Playful & Community** | `Alphakind` (Regular 400) | `Simply Sans` (Regular 400) | — | 0 (Style shift) | Approachable hand-lettered cheer in titles grounded by disciplined geometric body. |
| **Global Bilingual (KR)** | `BM DoHyeon` (Regular 400) | `General Sans` (Regular 400) | `Ubuntu` (400) | 0 (Script parity) | Seoul acrylic signboard Hangul craftsmanship aligned with clean Latin neo-grotesque. |

---

## 2. Style Archetype Decoder (Vibe Translator)

Translate colloquial design prompts into formal typography:

- **"Expensive / Luxury"**: High stroke contrast (Didone serif or sculpted display sans) + light/medium headline weights + wide all-caps tracking (`+0.05em`) + neutral sans body.
- **"Clean / Minimalist"**: Unadorned neo-grotesque + open apertures + consistent monoline strokes + generous line-height (`1.6+`) + generous whitespace.
- **"Not AI-Looking / Distinctive"**: Eliminate generic Inter/Roboto defaults. Pair character-rich display cuts (`Ithaca`, `Chillax`, `Reckoner`, `Credit Valley`) with a 200–300 weight delta and optical tracking.
- **"Modern / Tech"**: Geometric sans + contemporary circular geometry + tight headline tracking (`-0.02em`) + multi-weight superfamily.
- **"Technical / Dense"**: High x-height sans + tabular figures (`font-variant-numeric: tabular-nums`) + unambiguous code font (`Ubuntu Mono`).
- **"Editorial / Literary"**: Transitional serif with true companion italics for continuous reading + crisp sans metadata badges.

---

## 3. Ten Anti-Patterns Checklist (Lethal Mistakes)

Avoid these 10 lethal typographic pitfalls (deductions from 100 pt score):

1. ❌ **Decorative as Body** (-45 pts): Never use display, script, or novelty fonts for multi-paragraph body text.
2. ❌ **Competing Display Fonts** (-30 pts): Never use two expressive display fonts in the same layout. One vocal lead only.
3. ❌ **Weak Heading-to-Body Contrast** (-25 pts): Maintain at least a 200-unit weight delta (e.g. 700 vs 400) or clear category contrast.
4. ❌ **Excessive Font Families** (-25 pts): Maximum 2 primary families (heading + body), plus monospace only when code/telemetry is present.
5. ❌ **Script Mismatch / Zero Tofu** (-45 pts): Never assume Latin fonts support non-Latin scripts (Bangla, Arabic, Devanagari). Audit Unicode blocks first.
6. ❌ **Low x-Height in UI Microcopy** (-20 pts): Do not use low x-height display serifs for 11–13px button labels, tooltips, or badges.
7. ❌ **Hairline Screen Fatigue** (-20 pts): Never use 100/200 weights for continuous text on digital screens; 1px strokes break on pixels.
8. ❌ **Monospace Longform Fatigue** (-15 pts): Never set articles in monospace; uniform character widths cause ocular fatigue and slow reading by 20%.
9. ❌ **Uncanny Sans Mismatch** (-15 pts): Never pair two nearly identical neo-grotesque sans families without deliberate contrast.
10. ❌ **Personality Polar Clash** (-25 pts): Never pair conflicting emotional archetypes (e.g. luxury Didone serif + distressed graffiti marker).

---

## 4. Calibrated CSS Tokens Template

```css
:root {
  /* Font Families with Calibrated Fallbacks */
  --font-heading: 'Chillax', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-body: 'General Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-code: 'Ubuntu Mono', 'SF Mono', Consolas, Monaco, monospace;

  /* Font Weights (Only Confirmed Integer Weights) */
  --weight-heading: 600;
  --weight-subheading: 500;
  --weight-body: 400;
  --weight-bold: 700;

  /* Calibrated Tracking (Letter-Spacing) */
  --tracking-hero: -0.03em;
  --tracking-heading: -0.015em;
  --tracking-body: 0em;
  --tracking-ui: 0.015em;
  --tracking-caps: 0.06em;

  /* Line Heights */
  --leading-hero: 1.1;
  --leading-heading: 1.25;
  --leading-body: 1.6;
  --leading-ui: 1.35;
}

/* Base Typographic Hierarchy */
h1, h2, h3 {
  font-family: var(--font-heading);
  font-weight: var(--weight-heading);
  line-height: var(--leading-heading);
  letter-spacing: var(--tracking-heading);
}

body, p {
  font-family: var(--font-body);
  font-weight: var(--weight-body);
  line-height: var(--leading-body);
  letter-spacing: var(--tracking-body);
}

button, .ui-label {
  font-family: var(--font-body);
  font-weight: var(--weight-subheading);
  line-height: var(--leading-ui);
  letter-spacing: var(--tracking-ui);
}

code, pre, .tabular-stat {
  font-family: var(--font-code);
  font-variant-numeric: tabular-nums;
}
```

---

## 5. Non-Negotiable Hard Rules

1. **Never invent catalog fonts**: Only recommend real, verified fonts.
2. **Never invent weights**: Only use weights confirmed in font binaries (e.g. 400, 600, 700).
3. **Never invent language support**: Zero tofu tolerance. For Bangla, Arabic, etc., recommend verified external companion fonts (`Hind Siliguri`, `Noto Sans Bengali`, `Amiri`).
4. **Respect explicit user font choices**: If the user asks for a font, keep it and pair around it.
5. **No decorative fonts for body text**: Display/handwriting fonts are strictly prohibited from paragraphs.
6. **Maximum 2 primary families**: 1 heading + 1 body, plus monospace only for telemetry/code.
7. **Readability first**: Body/UI fonts must score $\ge 7/10$ with open apertures.
8. **Platform performance**: Web payloads < 100 KB (WOFF2); TrueType (`.ttf`) outlines for PowerPoint/Word.
9. **Zero-bloat delivery**: Leave only used font files in user projects; prune unneeded fonts and remove temporary skill folders upon completion.

---

> For dynamic scoring, licensing verification, and the complete 413-font catalog, see the canonical [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md).
