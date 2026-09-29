# Antigravity Adapter — Font Intelligence

This project uses the **Font Intelligence Typography Decision System**.

## Canonical Source of Truth
Read and follow:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

## Activation
Activate when:
- Designing or coding front-end UI, styling components, or configuring design systems.
- Recommending, pairing, or configuring typefaces in CSS, Tailwind, Flutter, React Native, or slides.
- Establishing typographic scale, line-height, letter-spacing, or numerical figure alignment.
- Auditing font legibility, script coverage, or redistribution licensing.

## Execution
- Recommend pairings: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <web|flutter|powerpoint>`
- Search fonts: `python scripts/search_fonts.py --mood "<vibe>" --role <body> --min-readability 8`
- Score pair: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
