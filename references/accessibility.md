# Web & Mobile Typography Accessibility (WCAG 2.1 & 2.2)

Accessible digital typography ensures legibility and comprehension for users with low vision, cognitive differences, dyslexia, and varying viewing environments.

---

## 1. Contrast Ratios (WCAG AA & AAA)

- **Level AA (Minimum)**:
  - **Normal Body Text (< 18pt or < 14pt bold)**: Minimum contrast ratio of **4.5:1** against the background.
  - **Large Text ($\ge 18pt$ or $\ge 14pt$ bold / ~24px normal or ~18.5px bold)**: Minimum contrast ratio of **3.0:1**.
  - **Active UI Components & Graphical Objects**: Minimum contrast ratio of **3.0:1**.
- **Level AAA (Enhanced)**:
  - Normal text: **7.0:1**.
  - Large text: **4.5:1**.
- **Important**: Hairline and thin weights (100/200) often fail perceived contrast even when mathematical color ratios pass, because thin strokes render at sub-pixel levels. Enforce minimum weight 400 for continuous text.

---

## 2. Text Sizing, Line Length & Zoom Reflow

- **Minimum Body Font Size**:
  - Desktop: Minimum **16px** (`1rem`).
  - Mobile: Minimum **15px – 16px**. Microcopy must never drop below **12px**.
- **Line Length (Measure)**:
  - Optimal reading length: **45 to 75 characters per line** (including spaces). 66 characters (`66ch`) is considered optically optimal.
  - Lines longer than 85 characters cause ocular fatigue when tracking back to the next line.
  - Lines shorter than 35 characters fragment reading rhythm.
- **200% Zoom & Responsive Reflow**:
  - Typography must scale cleanly up to 200% without horizontal scrolling or text clipping (WCAG 1.4.10 Reflow).
  - Use relative CSS units (`rem`, `em`, `ch`, `%`) rather than fixed pixels (`px`) for font sizes and line heights where possible.

---

## 3. Paragraph Spacing & Line Height

- **Line Height**: Minimum **1.5 times the font size** for continuous body text (WCAG 1.4.12 Text Spacing).
- **Paragraph Spacing**: At least **1.5 to 2.0 times the line height** to visually separate paragraphs without relying solely on indentation.
- **Letter Spacing**: Ensure letter spacing can be expanded to at least **0.12 times the font size** without clipping or breaking layout.
- **Word Spacing**: Ensure word spacing can be expanded to at least **0.16 times the font size**.

---

## 4. Dyslexia & Cognitive Considerations

- **Open Apertures**: Typefaces with open apertures (such as `c`, `e`, `s`, `a`) are significantly easier to distinguish than closed grotesque letterforms.
- **Distinguishable Characters**: Verify that ambiguous glyph pairs are distinctly shaped:
  - Capital `I` (with serifs/bars) vs Lowercase `l` vs Number `1`.
  - Capital `O` vs Number `0` (slashed or dotted).
  - Capital `B` vs Number `8`.
- **Avoid Justified Text**: Never use full justification (`text-align: justify`) on the web. It creates uneven word spacing ("rivers of white space") that disrupt reading flow for dyslexic readers.

---

## 5. Non-Reliance on Color Alone

Typography must never rely exclusively on font color to communicate critical state:
- Hyperlinks inside body text must have an underline or distinct structural indicator, not just a color change.
- Form error messages must include explicit text labels and icons, not just red text.
