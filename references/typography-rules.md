# Typography System, Scale & Spacing Rules

A complete typography system provides calibrated mathematical rules for hierarchy, modular scale, letter-spacing, line-height, and numerical data presentation.

---

## 1. Typography Hierarchy Matrix

| Role | Weight | Desktop Size | Mobile Size | Line-Height | Letter-Spacing | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero / Display** | 700 / 800 | 56px – 72px | 36px – 44px | 1.08 – 1.15 | `-0.03em` | Massive hero headlines and banners |
| **H1 (Page Title)** | 700 | 40px – 48px | 30px – 34px | 1.15 – 1.20 | `-0.02em` | Primary page headings |
| **H2 (Section Lead)** | 600 / 700 | 28px – 32px | 24px – 26px | 1.25 – 1.30 | `-0.015em` | Major content sections |
| **H3 (Subsection)** | 600 | 20px – 24px | 18px – 20px | 1.30 – 1.35 | `-0.01em` | Card titles and subsections |
| **H4 / Subhead** | 500 / 600 | 16px – 18px | 15px – 16px | 1.40 | `0` | Small headers and module titles |
| **Body (Normal)** | 400 | 16px | 15px – 16px | 1.55 – 1.65 | `0` | Continuous multi-paragraph reading |
| **Body-Large** | 400 / 500 | 18px – 20px | 16px – 18px | 1.50 – 1.60 | `0` | Introductory paragraphs and lead-ins |
| **Body-Small** | 400 | 13px – 14px | 12px – 13px | 1.45 – 1.50 | `+0.005em` | Secondary descriptions and metadata |
| **UI / Button** | 500 / 600 | 14px – 15px | 14px – 15px | 1.10 – 1.20 | `+0.015em` | Interactive buttons and controls |
| **Label / Eyebrow** | 600 | 11px – 12px | 11px – 12px | 1.20 | `+0.05em` | Uppercase category eyebrows |
| **Caption / Meta** | 400 | 12px | 11px – 12px | 1.40 | `+0.01em` | Timestamps, figure captions, tags |
| **Number / Price** | 600 / 700 | Contextual | Contextual | 1.10 | `-0.01em` | Metrics, prices, financial tables |
| **Code / Mono** | 400 / 500 | 13px – 14px | 12px – 13px | 1.50 | `0` | Code blocks, hashes, terminal data |

---

## 2. Responsive Type Scale Ratios

Use modular geometric scales to maintain proportional balance across viewports:

- **Major Third (1.250)**: Standard for web SaaS, dashboards, and mobile applications. Balanced contrast without overwhelming screen height.
- **Perfect Fourth (1.333)**: Editorial websites, blogs, and marketing landing pages. Provides noticeable jump between headings and text.
- **Augmented Fourth (1.414)**: High-impact portfolio, fashion, and luxury websites with massive headline contrast.
- **Major Second (1.125)**: Dense technical dashboards, financial spreadsheets, and compact mobile interfaces.

---

## 3. Letter-Spacing (Tracking) Intelligence

Tracking directly influences legibility depending on size and case:

1. **Large Display Text ($\ge 32px$)**: Apply **negative tracking** (`-0.01em` to `-0.03em`). Large characters have wider intrinsic side-bearings that visually disconnect words without negative tracking.
2. **Body Text ($15px - 18px$)**: Keep tracking at **zero** (`0`). Font foundries optimize side-bearings for body sizes; manual tracking often harms rhythmic reading flow.
3. **Microcopy & UI ($11px - 13px$)**: Apply **subtle positive tracking** (`+0.01em` to `+0.025em`) to prevent adjacent strokes from bleeding together at low screen resolutions.
4. **All-Caps Text**: **Always apply generous positive tracking** (`+0.05em` to `+0.12em`). Uppercase letterforms lack ascenders and descenders; extra spacing allows readers to recognize individual letter silhouettes.

---

## 4. Line-Height (Leading) Intelligence

- **Display & Headings**: Tighter leading (`1.05` to `1.25`). Large glyphs have significant intrinsic vertical space; excessive leading makes headlines look disjointed.
- **Body Paragraphs**: Comfortable leading (`1.55` to `1.65`). Ensures the eye easily returns to the start of the next line without losing place.
- **Complex Scripts (e.g. Bangla)**: Increase body leading to `1.65` to `1.80` to accommodate matras (top horizontal lines) and below-baseline conjunct vowel markers without clipping.
- **Dense UI Elements**: Compact leading (`1.15` to `1.25`) within bounded containers like buttons and badges.

---

## 5. Number Typography & Financial Figures

Numbers require specialized typographic treatment for data-heavy applications:
- **Tabular Figures (`tnum`)**: Essential for financial tables, price lists, and dashboards. All numerals share identical optical widths so decimal columns align vertically.
- **Proportional Figures (`pnum`)**: Best for numbers embedded inside narrative body text (e.g. "In 1994, 45 people arrived").
- **Lining Figures (`lnum`)**: Uniform cap-height numerals matching uppercase letters. Standard for modern corporate and fintech interfaces.
- **Disambiguation Testing**: In developer tools and crypto wallets, verify distinct glyph shapes for `0` vs `O`, `1` vs `l` vs `I`, and `8` vs `B`.
