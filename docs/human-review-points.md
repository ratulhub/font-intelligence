# Human Review & Editorial Governance Points

While Font Intelligence automates binary table extraction, file integrity hashing, and 10-dimensional mathematical contrast scoring, subjective aesthetic and legal dimensions strictly require human review.

---

## 1. Automated Facts vs. Human Review Fields

| Dimension | Type | Automation Engine | Human Review Responsibility |
| :--- | :---: | :--- | :--- |
| **Weights & Outlines** | Technical | `fontTools` binary parser (`OS/2.usWeightClass`) | Verify that synthesized bold is not masquerading as true bold. |
| **Variable Axes** | Technical | `fvar` table extraction (min/max/default) | Confirm continuous interpolation stability. |
| **Unicode Scripts** | Technical | `cmap` subtable character scanning | Audit contextual mark positioning (e.g. Bangla conjuncts). |
| **License EULA** | Legal | Pattern extraction from text files | **MANDATORY**: Human interpretation of redistribution clauses. |
| **Aesthetic Mood** | Editorial | Controlled style classifier | Human calibration of emotional cadence (`luxury` vs `playful`). |
| **Readability Tiers** | Editorial | Aperture & x-height heuristics | Visual verification of reading endurance at 14px–16px. |
| **Pairing Harmony** | Editorial | 10D scoring matrix | Evaluation of optical resonance and brand hierarchy. |
| **Logo Suitability** | Editorial | Silhouette heuristic | Memorability and vector outline customization potential. |

---

## 2. Specific Human Review Checkpoints

### Checkpoint 1: Legal Redistribution Interpretation
- Automated tools can detect keywords ("commercial", "free", "all rights reserved").
- **Human Reviewer Must**:
  1. Distinguish between *free for commercial client work* and *permission to re-host font binary on GitHub*.
  2. Verify marketplace receipt licenses (e.g., Creative Fabrica, Envato) which frequently forbid extracting raw `.ttf` binaries from project repositories.
  3. Classify ambiguous fonts as `NEEDS REVIEW` or `RESTRICTED` rather than guessing permissive status.

### Checkpoint 2: Optical Legibility vs. Display Classification
- Algorithms evaluate x-height and aperture ratios.
- **Human Reviewer Must**:
  1. Inspect the font in continuous paragraph reading at standard text sizes (15px/16px).
  2. Ensure decorative or distressed typefaces (e.g. `Castle Chunk`, `Achtung Bravo`) are never marked with `body` or `ui` roles.
  3. Ensure fonts scoring $< 7/10$ in readability are restricted to headline/accent roles.

### Checkpoint 3: Optical Cadence of Curated Pairings
- Mathematical contrast checks delta weights and serif/sans classifications.
- **Human Reviewer Must**:
  1. Test the combination in a live layout (via `preview/index.html`).
  2. Verify that the secondary font does not clash with the primary font's rhythm or personality.
  3. Write a deep, descriptive typographic rationale explaining **WHY** the pairing functions optically.

### Checkpoint 4: Non-Latin Script Quality Audit
- Binary parsing verifies whether Unicode code points exist in `cmap`.
- **Human Reviewer Must**:
  1. Verify complex shaping and OpenType layout rules (`GSUB`/`GPOS`).
  2. Check for missing conjuncts or broken vowel sign attachments (especially in Indic scripts like Bangla and Devanagari).
  3. If rendering is substandard, flag the font and recommend verified open-source companion fonts (`Hind Siliguri`, `Noto Sans Bengali`).
