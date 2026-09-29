# GitHub Copilot Instructions — Font Intelligence Thin Adapter

This workspace utilizes the **Font Intelligence Typography Decision System**.

## Canonical Source of Truth
Read and adhere to the protocol defined in:
👉 [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md)

## Activation Triggers
Apply Font Intelligence instructions whenever:
- Generating or editing CSS, SCSS, Tailwind config, HTML, React, Vue, Flutter, or React Native typography tokens.
- Suggesting font pairings, font-family declarations, font-weight scales, or line-heights.
- Designing landing pages, dashboards, mobile apps, or presentation decks.
- Verifying multi-language script availability (zero-tofu policy) or font licensing.

## Execution
- **CLI Recommender**: `python scripts/recommend.py --use-case <id> --style "<vibe>" --platform <web|flutter|powerpoint>`
- **Catalog Inspection**: Query `catalog/fonts.json`, `catalog/use-cases.json`, and `catalog/pairings.json`.
- **Pair Scoring**: `python scripts/score_pair.py --primary <id> --secondary <id> --style <vibe>`
- **Compact Fallback**: For concise reference, check [`lite/font-intelligence-lite.md`](lite/font-intelligence-lite.md).

## Non-Negotiable Hard Rules
1. Never invent fonts, weights, or language scripts.
2. Never assign decorative or display typefaces to body or dense UI text.
3. Always respect explicit user font choices (anchor and pair around them).
4. Maximum 2 primary families (heading + body), plus monospace only if needed.
5. Always generate calibrated system fallback stacks.
6. Full rules in [`.agents/skills/font-intelligence/SKILL.md`](.agents/skills/font-intelligence/SKILL.md).
