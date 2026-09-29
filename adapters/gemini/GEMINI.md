# GEMINI.md — Font Intelligence Thin Adapter

This repository uses the **Font Intelligence Typography Decision System**.

## Canonical Source of Truth
Read and follow:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

## When to Activate
Activate Font Intelligence when:
- Designing or coding front-end UI, styling components, or configuring design systems.
- Recommending, pairing, or configuring typefaces in CSS, Tailwind, Flutter, React Native, or slides.
- Establishing typographic scale, line-height, letter-spacing, or numerical figure alignment.
- Auditing font legibility, script coverage, or redistribution licensing.

## How to Execute
- **Recommend**: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <web|flutter|powerpoint>`
- **Search**: `python scripts/search_fonts.py --mood "<vibe>" --role <body> --min-readability 8`
- **Score Pair**: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
- **Offline / No Tool Access**: Read `catalog/fonts.json`, `catalog/use-cases.json`, and `catalog/pairings.json`.
- **Compact Fallback**: Use [`lite/font-intelligence-lite.md`](lite/font-intelligence-lite.md) for quick lookups.

## Key Rules
1. Never invent fonts, weights, or language scripts.
2. Never use decorative fonts for body text.
3. Respect explicit user font preferences.
4. Keep to maximum 2 primary families (plus monospace only when needed).
5. All full requirements: see [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md).
