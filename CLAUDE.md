# CLAUDE.md — Font Intelligence Thin Adapter

This repository uses the **Font Intelligence Typography Decision System**.

## Canonical Source of Truth
Read and follow:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

## When to Activate
Activate Font Intelligence when handling:
- UI/UX design, front-end styling, or typography in CSS, Tailwind, HTML, React, Vue, Svelte, Flutter, React Native, or presentation decks.
- Font selection, pairings, typographic hierarchy, letter-spacing, or line-height calculations.
- Readability audits, platform suitability checks, or licensing/redistribution compliance.

## How to Execute
- **Recommend Pairings**: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <web|flutter|powerpoint>`
- **Search Catalog**: `python scripts/search_fonts.py --mood "<vibe>" --role <body> --min-readability 8`
- **Score a Pair**: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
- **Direct Catalog Inspection**: When scripts cannot run, inspect `catalog/fonts.json`, `catalog/use-cases.json`, and `catalog/pairings.json`.
- **Compact Fallback**: For constrained context, consult [`lite/font-intelligence-lite.md`](lite/font-intelligence-lite.md).

## Non-Negotiable Rules
1. Never invent fonts, weights, or language script support.
2. Never assign decorative or display fonts to continuous body/UI text.
3. Respect explicit user font choices (anchor and pair around them).
4. Maximum 2 primary families (heading + body), monospace only if needed.
5. Refer to [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md) for full protocol.
