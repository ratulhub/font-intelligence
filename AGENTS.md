# AGENTS.md — Font Intelligence Decision System

This repository contains the **Font Intelligence Typography Decision System**.

The **canonical source of truth** for all agent instructions, rules, and decision protocols is:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

### Agent Adapter Architecture
All coding agents share a single core skill, identical catalog, and unified rules:
```
CORE SKILL (.agents/skills/font-intelligence/SKILL.md)
  ├── Thin Adapters:
  │   ├── Antigravity   → .agents/skills/font-intelligence/ & .agents/rules/font-intelligence.md
  │   ├── Claude Code   → CLAUDE.md
  │   ├── Codex         → AGENTS.md & .codex/instructions.md
  │   ├── Cursor        → .cursorrules & .cursor/rules/font-intelligence.mdc
  │   ├── Windsurf      → .windsurfrules
  │   ├── Cline         → .clinerules
  │   ├── GitHub Copilot→ .github/copilot-instructions.md
  │   └── Gemini CLI    → GEMINI.md
  ├── Compact Fallback  → lite/font-intelligence-lite.md
  └── Canonical Data    → catalog/ (fonts, use-cases, pairings, scoring, anti-patterns)
```
No separate font databases or duplicate schemas are maintained across agents.

---

## 1. When to Activate This Skill

Activate Font Intelligence whenever a user request involves:
- Designing or coding UI/UX, landing pages, SaaS dashboards, or mobile apps.
- Selecting, pairing, or styling fonts in CSS, Tailwind, Flutter, React Native, or slide decks (PowerPoint/Keynote).
- Branding, editorial design, or typography hierarchy decisions.
- Evaluating font legibility, performance budgets, or commercial/redistribution licenses.

---

## 2. Core Protocol: Understand Before Choosing

> **Mandate**: **NEVER** default to generic, popular fonts (e.g., Inter, Roboto, Arial, Helvetica).
> Every font choice must be backed by verified catalog metrics, project situation constraints, verified script coverage, platform rendering requirements, and a clear typographic explanation of **WHY** the combination works.

### Quick Workflow
1. **Diagnose Project**: Identify use case (`catalog/use-cases.json`), platform (Web, Flutter, React Native, PowerPoint), and audience.
2. **Translate Style Vibes**: Map colloquial requests ("expensive", "clean", "not AI-looking") to formal typographic categories using `catalog/use-cases.json#style_interpretations`.
3. **Respect Explicit User Choices**: If the user specifies a font, anchor it and pair around it. Never override unprompted.
4. **Strict Script Audit**: Verify OpenType script support. If unsupported (e.g. Bangla, Arabic), report 0 catalog fonts and provide verified open-source companion recommendations (`Hind Siliguri`, `Noto Sans Bengali`, `Amiri`).
5. **Score & Check Anti-Patterns**: Evaluate across 10 dimensions (`catalog/scoring.json`) and audit against the 10 typography anti-patterns (`catalog/anti-patterns.json`).
6. **Provide Code Tokens**: Output calibrated CSS custom properties, Flutter `pubspec.yaml`, or PowerPoint TrueType embedding instructions.
7. **Zero-Bloat Delivery**: Export only chosen fonts (`python scripts/copy_fonts.py --fonts "..." --dest "<project>/fonts" --prune-unused`) and clean project workspace (`python scripts/clean_project.py --project-dir <path>`) so only used font files stay in the user's project.

---

## 3. Fast CLI Execution

Run supporting tools from the workspace root:

```bash
# 1. Recommend Pairings from Project Brief
python scripts/recommend.py --use-case fintech --style "expensive, not AI-looking" --platform web

# 2. Search Catalog by Mood, Role & Readability
python scripts/search_fonts.py --mood "clean" --role body --min-readability 8

# 3. Score a Specific Font Pair (10 Dimensions + Anti-Patterns)
python scripts/score_pair.py --primary chillax --secondary general-sans --style luxury

# 4. Export Fonts & Copy Licenses
python scripts/copy_fonts.py --fonts "chillax,general-sans" --dest "dist/fonts" --snippets all

# 5. Clean User Project (Keep Only Used Fonts, Prune Skill Folder)
python scripts/clean_project.py --project-dir path/to/project --keep-fonts "chillax,general-sans"

# 6. Audit Licensing & Redistribution Terms
python scripts/validate_licenses.py --filter office-embeddable
```

---

## 4. Offline / Direct JSON Mode (No Python)

If Python execution is unavailable, inspect catalog JSON files directly:
- **`catalog/fonts.json`**: 413 verified families with roles, readability (1–10), and technical tables.
- **`catalog/use-cases.json`**: 29 project situations, performance budgets, and style mappings.
- **`catalog/pairings.json`**: Curated masterclass pairings.
- **`catalog/anti-patterns.json`**: 10 typography anti-patterns with point deductions.
- **`catalog/scoring.json`**: 10-dimensional scoring model.

---

## 5. Hard Rules

1. Never invent catalog fonts when making autonomous recommendations.
2. Never invent weights (only use confirmed weights in `technical.weights`).
3. Never invent language support (zero tofu policy; never guess script coverage).
4. Do NOT assume "free for commercial use" = "allowed to redistribute on GitHub". Refer to [`docs/redistribution-review.md`](docs/redistribution-review.md).
5. Respect explicit user font choices.
6. Do not replace an existing project's typography system unprompted.
7. Never use decorative fonts for continuous body text.
8. Maximum of 2 primary families (heading + body/UI), with monospace only when needed.
9. Enforce readability scores $\ge 7/10$ for body and UI.
10. Consider platform and performance (Core Web Vitals < 100 KB; TrueType `.ttf` outlines for PowerPoint/Word).
11. Always generate robust generic fallbacks.
12. Zero-bloat project delivery: Never leave unused font files, unneeded weights, or temporary skill folders inside the user's project repository upon completion. Only the used font binaries must remain.

For the complete specification, read [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md).
